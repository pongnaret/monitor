# 🖥️ PC Monitor & Chat System

ระบบ Monitor เครื่องคอมพิวเตอร์ใน LAN พร้อมระบบ Chat Real-time ระหว่าง Admin และเครื่องลูกข่าย

## ✨ คุณสมบัติหลัก

### 📊 Monitoring
- ✅ ตรวจสอบสถานะ Online/Offline แบบ Real-time
- ✅ แสดงข้อมูล CPU, RAM, Disk Usage
- ✅ บันทึกประวัติการใช้งาน
- ✅ แจ้งเตือนอัตโนมัติเมื่อทรัพยากรเกินกำหนด
- ✅ แสดง Network usage และ Uptime

### 💬 Chat System
- ✅ Chat Real-time ระหว่าง Admin และเครื่องลูกข่าย
- ✅ แจ้งเตือนข้อความใหม่
- ✅ ส่งข้อความแจ้งปัญหาอัตโนมัติ
- ✅ ประวัติการแชทเก็บใน Database

### 🎨 Dashboard
- ✅ ดูภาพรวมเครื่องทั้งหมด
- ✅ แสดงสถานะแบบ Real-time ด้วย WebSocket
- ✅ UI สวยงามใช้งานง่าย
- ✅ รองรับการใช้งานบน Web Browser

## 📋 ความต้องการของระบบ

- Python 3.8+
- SQLite (มีมาใน Python แล้ว)
- Browser ที่รองรับ WebSocket (Chrome, Firefox, Edge)

## 🚀 การติดตั้ง

### 0. ติดตั้ง Python (ถ้ายังไม่มี)

**สำหรับ Windows:**
1. ดาวน์โหลด Python จาก [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. เลือก Python 3.8 ขึ้นไป (แนะนำ 3.11+)
3. ติดตั้ง และ **ต้องติ๊กถูก "Add Python to PATH"** ด้วยนะครับ
4. ทดสอบว่าติดตั้งสำเร็จ:
   ```bash
   python --version
   ```

### 1. ติดตั้ง Python Libraries

เปิด PowerShell หรือ Command Prompt แล้วรันคำสั่ง:

**วิธีที่ 1 (แนะนำ):**
```bash
python -m pip install -r requirements.txt
```

**วิธีที่ 2:**
```bash
pip install -r requirements.txt
```

**วิธีที่ 3 (ถ้า Python Launcher ติดตั้งแล้ว):**
```bash
py -m pip install -r requirements.txt
```

### 2. กำหนดค่าระบบ

แก้ไขไฟล์ `config.py`:

```python
# สำหรับ Server
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000

# สำหรับ Agent (แก้ SERVER_URL เป็น IP ของ Server)
SERVER_URL = "http://192.168.1.100:8000"  # เปลี่ยนเป็น IP ของ Server
UPDATE_INTERVAL = 30  # วินาที

# ค่าเกณฑ์การแจ้งเตือน
CPU_THRESHOLD = 90  # เปอร์เซ็นต์
RAM_THRESHOLD = 90
DISK_THRESHOLD = 90
```

### 3. สร้าง Database

```bash
python database.py
```

## 💻 การใช้งาน

### เริ่มต้น Server (บนเครื่อง Admin)

```bash
python server.py
```

เปิด Browser ไปที่: `http://localhost:8000`

### เริ่มต้น Agent (บนเครื่องลูกข่าย)

**โหมดปกติ - Monitor อัตโนมัติ:**
```bash
python agent.py
```

**โหมด Chat:**
```bash
python agent.py chat
```

## 📁 โครงสร้างโปรเจค

```
moniter/
├── config.py              # ไฟล์กำหนดค่า
├── database.py            # Database models และ setup
├── server.py              # Server API (FastAPI)
├── agent.py               # Agent สำหรับเครื่องลูกข่าย
├── requirements.txt       # Python dependencies
├── templates/
│   └── dashboard.html     # Dashboard UI สำหรับ Admin
├── monitor.db             # SQLite database (สร้างอัตโนมัติ)
└── README.md              # คู่มือนี้
```

## 🔧 การทำงานของระบบ

### สถาปัตยกรรม

```
┌─────────────────┐
│  Admin Browser  │
│   (Dashboard)   │
└────────┬────────┘
         │ WebSocket + HTTP
         │
┌────────▼────────┐
│     Server      │
│   (FastAPI)     │
│   + Database    │
└────────┬────────┘
         │ HTTP
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼───┐
│Agent1│  │Agent2│  ... (เครื่องลูกข่าย)
└──────┘  └──────┘
```

### Agent ส่งข้อมูล

1. Agent ลงทะเบียนกับ Server
2. เก็บข้อมูล metrics ทุก 30 วินาที (ตาม config)
3. ส่งข้อมูลไปที่ Server
4. ตรวจสอบค่าเกินกำหนด → แจ้งเตือน Admin อัตโนมัติ
5. ตรวจสอบข้อความใหม่จาก Admin

### Server จัดการข้อมูล

1. รับข้อมูลจาก Agents
2. บันทึกลง Database
3. สร้าง Alerts ถ้าจำเป็น
4. ส่งข้อมูล Real-time ไปที่ Dashboard ผ่าน WebSocket

### Dashboard แสดงผล

1. แสดงรายการเครื่องทั้งหมด
2. อัพเดท Real-time ผ่าน WebSocket
3. Admin สามารถคลิก Chat กับเครื่องได้ทันที

## 📊 ข้อมูลที่ Monitor

- **CPU**: เปอร์เซ็นต์การใช้งาน, จำนวน cores
- **RAM**: ขนาดรวม, ใช้ไป, เปอร์เซ็นต์
- **Disk**: ขนาดรวม, ใช้ไป, เปอร์เซ็นต์
- **Network**: ข้อมูลส่ง/รับ (MB)
- **Uptime**: เวลาที่เครื่องทำงานต่อเนื่อง
- **Status**: Online/Offline, Last seen

## 💬 การใช้งาน Chat

### จาก Admin (Dashboard)
1. คลิกปุ่ม "💬 Chat" ที่การ์ดเครื่อง
2. พิมพ์ข้อความและกด Enter หรือคลิก "ส่ง"
3. รับข้อความตอบกลับแบบ Real-time

### จากเครื่องลูกข่าย (Agent)
1. รันคำสั่ง: `python agent.py chat`
2. พิมพ์ข้อความและกด Enter
3. พิมพ์ `exit` เพื่อออกจากโหมด Chat

### แจ้งเตือนอัตโนมัติ
เมื่อ CPU/RAM/Disk เกินค่ากำหนด Agent จะส่งข้อความแจ้งเตือนไปหา Admin อัตโนมัติ

## 🔔 ระบบ Alert

ระบบจะสร้าง Alert อัตโนมัติเมื่อ:
- CPU > 90% (หรือตามที่กำหนดใน config)
- RAM > 90%
- Disk > 90%
- เครื่อง Offline

Alert จะแสดงใน Dashboard และส่งข้อความ Chat

## 🐛 การแก้ปัญหา

### Agent เชื่อมต่อ Server ไม่ได้
- ตรวจสอบ `SERVER_URL` ใน config.py
- ตรวจสอบว่า Server กำลังทำงานอยู่
- ตรวจสอบ Firewall (เปิด port 8000)

### Dashboard ไม่แสดงข้อมูล Real-time
- ตรวจสอบ WebSocket connection ใน Browser Console
- ลอง Refresh หน้าเว็บ
- ตรวจสอบว่า Server รันด้วย uvicorn

### Agent ส่งข้อมูลไม่ครบ
- ตรวจสอบ Python version (ต้อง 3.8+)
- ตรวจสอบว่าติดตั้ง `psutil` แล้ว
- ดู error logs ใน console

## 🔒 ความปลอดภัย

⚠️ **คำเตือน**: ระบบนี้ออกแบบสำหรับใช้ใน LAN เท่านั้น

สำหรับการใช้งานในระบบจริง แนะนำให้:
- เพิ่ม Authentication/Authorization
- ใช้ HTTPS แทน HTTP
- เข้ารหัสข้อมูลใน Database
- จำกัดการเข้าถึง API endpoints
- ใช้ Environment Variables สำหรับ sensitive data

## 📝 การพัฒนาเพิ่มเติม

ไอเดียสำหรับพัฒนาต่อ:
- [ ] เพิ่มระบบ Login สำหรับ Admin
- [ ] Export รายงานเป็น PDF/Excel
- [ ] แสดงกราฟแบบ Real-time
- [ ] รองรับ Email notifications
- [ ] รองรับหลาย Admin พร้อมกัน
- [ ] Mobile App สำหรับ Admin
- [ ] Remote Control เครื่องลูกข่าย
- [ ] Screenshot จากระยะไกล

## 📞 การติดต่อ

หากมีปัญหาหรือข้อเสนอแนะ:
- สร้าง Issue ใน GitHub
- หรือติดต่อผู้พัฒนาโดยตรง

## 📜 License

MIT License - ใช้งานได้อย่างอิสระ

---

**สร้างด้วย ❤️ เพื่อการ Monitor เครื่องคอมพิวเตอร์ใน LAN**
