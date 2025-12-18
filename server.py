"""
Server API สำหรับระบบ Monitor & Chat
- รับข้อมูล monitoring จาก agents
- จัดการ chat ระหว่าง agent และ admin
- ให้บริการ dashboard แก่ admin
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict
import json
import uvicorn

import config
from database import get_db, init_db, Computer, Metric, ChatMessage, Alert

app = FastAPI(title="PC Monitor & Chat System")
templates = Jinja2Templates(directory="templates")

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"✅ WebSocket connected: {client_id}")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            print(f"❌ WebSocket disconnected: {client_id}")

    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)


manager = ConnectionManager()


# ================== API Endpoints ==================

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("🚀 Server started successfully!")


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Admin Dashboard"""
    computers = db.query(Computer).all()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "computers": computers
    })


@app.post("/api/register")
async def register_computer(data: dict, db: Session = Depends(get_db)):
    """ลงทะเบียนเครื่องคอมพิวเตอร์"""
    hostname = data.get("hostname")
    ip_address = data.get("ip_address")
    os_info = data.get("os_info")

    # ตรวจสอบว่ามีเครื่องนี้อยู่แล้วหรือไม่
    computer = db.query(Computer).filter(Computer.hostname == hostname).first()

    if computer:
        # อัพเดทข้อมูล
        computer.ip_address = ip_address
        computer.os_info = os_info
        computer.is_online = True
        computer.last_seen = datetime.now()
    else:
        # สร้างใหม่
        computer = Computer(
            hostname=hostname,
            ip_address=ip_address,
            os_info=os_info,
            is_online=True,
            last_seen=datetime.now()
        )
        db.add(computer)

    db.commit()
    db.refresh(computer)

    return {"status": "success", "computer_id": computer.id, "hostname": hostname}


@app.post("/api/metrics")
async def receive_metrics(data: dict, db: Session = Depends(get_db)):
    """รับข้อมูล metrics จาก agent"""
    computer_id = data.get("computer_id")

    # อัพเดทสถานะเครื่อง
    computer = db.query(Computer).filter(Computer.id == computer_id).first()
    if computer:
        computer.is_online = True
        computer.last_seen = datetime.now()

        # บันทึก metrics
        metric = Metric(
            computer_id=computer_id,
            cpu_percent=data.get("cpu_percent"),
            cpu_count=data.get("cpu_count"),
            ram_total=data.get("ram_total"),
            ram_used=data.get("ram_used"),
            ram_percent=data.get("ram_percent"),
            disk_total=data.get("disk_total"),
            disk_used=data.get("disk_used"),
            disk_percent=data.get("disk_percent"),
            network_sent=data.get("network_sent"),
            network_recv=data.get("network_recv"),
            uptime_seconds=data.get("uptime_seconds")
        )
        db.add(metric)

        # ตรวจสอบและสร้าง alerts
        create_alerts_if_needed(db, computer_id, data)

        db.commit()

        # แจ้งเตือน dashboard แบบ real-time
        await manager.broadcast(json.dumps({
            "type": "metrics_update",
            "computer_id": computer_id,
            "hostname": computer.hostname,
            "data": data
        }))

        return {"status": "success"}

    return {"status": "error", "message": "Computer not found"}


def create_alerts_if_needed(db: Session, computer_id: int, metrics: dict):
    """สร้าง alert ถ้าเกินค่ากำหนด"""
    alerts_to_create = []

    if metrics["cpu_percent"] > config.CPU_THRESHOLD:
        alerts_to_create.append({
            "type": "cpu",
            "message": f"CPU usage is high: {metrics['cpu_percent']}%",
            "value": metrics["cpu_percent"],
            "threshold": config.CPU_THRESHOLD
        })

    if metrics["ram_percent"] > config.RAM_THRESHOLD:
        alerts_to_create.append({
            "type": "ram",
            "message": f"RAM usage is high: {metrics['ram_percent']}%",
            "value": metrics["ram_percent"],
            "threshold": config.RAM_THRESHOLD
        })

    if metrics["disk_percent"] > config.DISK_THRESHOLD:
        alerts_to_create.append({
            "type": "disk",
            "message": f"Disk usage is high: {metrics['disk_percent']}%",
            "value": metrics["disk_percent"],
            "threshold": config.DISK_THRESHOLD
        })

    for alert_data in alerts_to_create:
        # ตรวจสอบว่ามี alert แบบเดียวกันที่ยังไม่ resolved หรือไม่
        existing_alert = db.query(Alert).filter(
            Alert.computer_id == computer_id,
            Alert.alert_type == alert_data["type"],
            Alert.is_resolved == False
        ).first()

        if not existing_alert:
            alert = Alert(
                computer_id=computer_id,
                alert_type=alert_data["type"],
                message=alert_data["message"],
                value=alert_data["value"],
                threshold=alert_data["threshold"]
            )
            db.add(alert)


@app.post("/api/chat/send")
async def send_chat_message(data: dict, db: Session = Depends(get_db)):
    """ส่งข้อความ chat"""
    computer_id = data.get("computer_id")
    sender = data.get("sender")  # "agent" or "admin"
    message = data.get("message")

    chat_msg = ChatMessage(
        computer_id=computer_id,
        sender=sender,
        message=message
    )
    db.add(chat_msg)
    db.commit()
    db.refresh(chat_msg)

    # ส่งข้อความแบบ real-time ผ่าน WebSocket
    computer = db.query(Computer).filter(Computer.id == computer_id).first()
    await manager.broadcast(json.dumps({
        "type": "chat_message",
        "computer_id": computer_id,
        "hostname": computer.hostname if computer else "Unknown",
        "sender": sender,
        "message": message,
        "timestamp": chat_msg.timestamp.isoformat(),
        "id": chat_msg.id
    }))

    return {"status": "success", "message_id": chat_msg.id}


@app.get("/api/chat/messages/{computer_id}")
async def get_chat_messages(computer_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """ดึงข้อความ chat"""
    messages = db.query(ChatMessage).filter(
        ChatMessage.computer_id == computer_id
    ).order_by(ChatMessage.timestamp.desc()).limit(limit).all()

    return [{
        "id": msg.id,
        "sender": msg.sender,
        "message": msg.message,
        "timestamp": msg.timestamp.isoformat(),
        "is_read": msg.is_read
    } for msg in reversed(messages)]


@app.put("/api/chat/read/{message_id}")
async def mark_message_read(message_id: int, db: Session = Depends(get_db)):
    """ทำเครื่องหมายว่าอ่านข้อความแล้ว"""
    message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    if message:
        message.is_read = True
        db.commit()
        return {"status": "success"}
    return {"status": "error", "message": "Message not found"}


@app.get("/api/computers")
async def get_computers(db: Session = Depends(get_db)):
    """ดึงรายการเครื่องทั้งหมด"""
    computers = db.query(Computer).all()

    result = []
    for comp in computers:
        # ดึง metrics ล่าสุด
        latest_metric = db.query(Metric).filter(
            Metric.computer_id == comp.id
        ).order_by(Metric.timestamp.desc()).first()

        # นับข้อความที่ยังไม่ได้อ่าน
        unread_count = db.query(ChatMessage).filter(
            ChatMessage.computer_id == comp.id,
            ChatMessage.is_read == False,
            ChatMessage.sender == "agent"
        ).count()

        # ดึง alerts ที่ยังไม่ resolved
        active_alerts = db.query(Alert).filter(
            Alert.computer_id == comp.id,
            Alert.is_resolved == False
        ).count()

        result.append({
            "id": comp.id,
            "hostname": comp.hostname,
            "ip_address": comp.ip_address,
            "os_info": comp.os_info,
            "is_online": comp.is_online,
            "last_seen": comp.last_seen.isoformat(),
            "latest_metric": {
                "cpu_percent": latest_metric.cpu_percent if latest_metric else 0,
                "ram_percent": latest_metric.ram_percent if latest_metric else 0,
                "disk_percent": latest_metric.disk_percent if latest_metric else 0,
            } if latest_metric else None,
            "unread_messages": unread_count,
            "active_alerts": active_alerts
        })

    return result


@app.get("/api/metrics/{computer_id}")
async def get_metrics_history(
    computer_id: int,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """ดึงประวัติ metrics"""
    since = datetime.now() - timedelta(hours=hours)

    metrics = db.query(Metric).filter(
        Metric.computer_id == computer_id,
        Metric.timestamp >= since
    ).order_by(Metric.timestamp.asc()).all()

    return [{
        "timestamp": m.timestamp.isoformat(),
        "cpu_percent": m.cpu_percent,
        "ram_percent": m.ram_percent,
        "disk_percent": m.disk_percent,
    } for m in metrics]


@app.get("/api/alerts")
async def get_alerts(resolved: bool = False, db: Session = Depends(get_db)):
    """ดึงรายการ alerts"""
    query = db.query(Alert).filter(Alert.is_resolved == resolved)
    alerts = query.order_by(Alert.timestamp.desc()).limit(100).all()

    result = []
    for alert in alerts:
        computer = db.query(Computer).filter(Computer.id == alert.computer_id).first()
        result.append({
            "id": alert.id,
            "computer_id": alert.computer_id,
            "hostname": computer.hostname if computer else "Unknown",
            "alert_type": alert.alert_type,
            "message": alert.message,
            "value": alert.value,
            "threshold": alert.threshold,
            "timestamp": alert.timestamp.isoformat(),
            "is_resolved": alert.is_resolved
        })

    return result


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint สำหรับ real-time updates"""
    await manager.connect(websocket, "admin_dashboard")
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket messages if needed
    except WebSocketDisconnect:
        manager.disconnect("admin_dashboard")


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=True
    )
