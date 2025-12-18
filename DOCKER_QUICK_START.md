# 🚀 Docker Quick Start - 3 ขั้นตอน

## สำหรับ Server (Admin)

### 1️⃣ ติดตั้ง Docker
- Windows/Mac: ดาวน์โหลด [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Linux: `curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh`

### 2️⃣ ตั้งค่าและเริ่มใช้งาน

```bash
# 1. สร้างไฟล์ .env
copy .env.example .env

# 2. แก้ไขรหัสผ่านใน .env (สำคัญ!)
notepad .env

# 3. เริ่มต้นระบบ
docker-start.bat
```

หรือใช้คำสั่งโดยตรง:
```bash
docker-compose up -d
```

### 3️⃣ เข้าใช้งาน Dashboard

เปิด Browser: **http://localhost:8000**

---

## 📱 สำหรับเครื่องลูกข่าย (Agent)

Agent **ไม่ต้องใช้ Docker** - ติดตั้งแบบปกติตามคู่มือ [INSTALL_AGENT.md](INSTALL_AGENT.md)

แค่แก้ไข `SERVER_URL` ให้ชี้มาที่ IP ของเครื่อง Server:
```python
SERVER_URL = "http://192.168.1.100:8000"  # <-- IP ของเครื่อง Docker
```

---

## 🛠️ คำสั่งที่ใช้บ่อย

| คำสั่ง | ความหมาย |
|--------|----------|
| `docker-start.bat` | เริ่มต้นระบบ |
| `docker-stop.bat` | หยุดระบบ |
| `docker-logs.bat` | ดู logs |
| `docker-restart.bat` | Restart ระบบ |
| `docker-compose ps` | ดูสถานะ |
| `docker-compose down` | ลบระบบ |

---

## ✅ ตรวจสอบว่าทำงาน

### ตรวจสอบ Containers:
```bash
docker-compose ps
```

ควรเห็น:
```
NAME                STATUS
monitor_server      Up
monitor_mysql       Up (healthy)
```

### ทดสอบ API:
```bash
curl http://localhost:8000/api/computers
```

---

## 🆘 แก้ปัญหาด่วน

### Port ถูกใช้แล้ว:
แก้ไข `docker-compose.yml` เปลี่ยน port:
```yaml
ports:
  - "8080:8000"  # เปลี่ยนจาก 8000 เป็น 8080
```

### MySQL ไม่ทำงาน:
```bash
docker-compose restart mysql
docker-compose logs mysql
```

### ลืมรหัสผ่าน MySQL:
ดูใน `.env` file

---

**อ่านเพิ่มเติม:** [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)
