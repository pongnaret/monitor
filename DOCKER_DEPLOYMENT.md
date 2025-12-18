# 🐳 Docker Deployment Guide

คู่มือการติดตั้งและใช้งาน PC Monitor Server ด้วย Docker

---

## 📋 ความต้องการของระบบ

- Docker Desktop (Windows/Mac) หรือ Docker Engine (Linux)
- Docker Compose v2.0+
- RAM อย่างน้อย 2GB
- Disk space อย่างน้อย 5GB

---

## 🚀 การติดตั้ง

### **ขั้นตอนที่ 1: ติดตั้ง Docker**

#### สำหรับ Windows:
1. ดาวน์โหลด Docker Desktop: https://www.docker.com/products/docker-desktop/
2. ติดตั้งและเปิดโปรแกรม
3. ตรวจสอบการติดตั้ง:
   ```bash
   docker --version
   docker-compose --version
   ```

#### สำหรับ Linux:
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker
```

---

### **ขั้นตอนที่ 2: เตรียมไฟล์ Environment**

1. สร้างไฟล์ `.env` จาก template:
   ```bash
   copy .env.example .env
   ```
   หรือบน Linux:
   ```bash
   cp .env.example .env
   ```

2. แก้ไขไฟล์ `.env`:
   ```env
   # MySQL Configuration
   MYSQL_ROOT_PASSWORD=your_secure_root_password_here
   MYSQL_DATABASE=monitor_db
   MYSQL_USER=monitor_user
   MYSQL_PASSWORD=your_secure_password_here
   ```

   **⚠️ สำคัญ: เปลี่ยนรหัสผ่านทั้งหมดก่อนใช้งานจริง!**

---

### **ขั้นตอนที่ 3: เริ่มใช้งาน**

#### วิธีที่ 1: ใช้ Batch Script (Windows)

```bash
docker-start.bat
```

#### วิธีที่ 2: ใช้ Docker Compose โดยตรง

```bash
docker-compose up -d
```

รอสักครู่ให้ Docker build image และเริ่มต้น containers

---

## 🌐 เข้าใช้งานระบบ

เมื่อเริ่มต้นสำเร็จ:

- **Dashboard**: http://localhost:8000
- **MySQL**: localhost:3306

จากเครื่องอื่นใน LAN:
- **Dashboard**: http://[SERVER_IP]:8000

---

## 🛠️ คำสั่งที่ใช้บ่อย

### เริ่มต้นระบบ
```bash
docker-compose up -d
```
หรือ
```bash
docker-start.bat
```

### หยุดระบบ
```bash
docker-compose stop
```
หรือ
```bash
docker-stop.bat
```

### Restart ระบบ
```bash
docker-compose restart
```
หรือ
```bash
docker-restart.bat
```

### ดู Logs
```bash
docker-compose logs -f
```
หรือดูเฉพาะ server:
```bash
docker-compose logs -f server
```
หรือ
```bash
docker-logs.bat
```

### ตรวจสอบสถานะ
```bash
docker-compose ps
```

### เข้าไปใน Container
```bash
docker-compose exec server bash
```

### ลบระบบทั้งหมด (รวมข้อมูล)
```bash
docker-compose down -v
```

---

## 📊 โครงสร้าง Docker

```
┌─────────────────────────────────┐
│      Docker Compose             │
│                                 │
│  ┌──────────────────────────┐  │
│  │   monitor_server         │  │
│  │   (Python/FastAPI)       │  │
│  │   Port: 8000             │  │
│  └──────────┬───────────────┘  │
│             │                   │
│             │ connects to       │
│             ▼                   │
│  ┌──────────────────────────┐  │
│  │   monitor_mysql          │  │
│  │   (MySQL 8.0)            │  │
│  │   Port: 3306             │  │
│  │   Volume: mysql_data     │  │
│  └──────────────────────────┘  │
│                                 │
│  Network: monitor_network       │
└─────────────────────────────────┘
```

---

## 🔒 ความปลอดภัย

### ในสภาพแวดล้อม Production:

1. **เปลี่ยนรหัสผ่านทั้งหมด:**
   - MYSQL_ROOT_PASSWORD
   - MYSQL_PASSWORD
   - ใช้รหัสผ่านที่ซับซ้อนและยาว

2. **ใช้ HTTPS:**
   - ตั้งค่า Reverse Proxy (Nginx/Traefik)
   - ใช้ Let's Encrypt SSL Certificate

3. **จำกัดการเข้าถึง:**
   - ใช้ Firewall
   - จำกัด IP ที่เข้าถึงได้
   - ไม่เปิด MySQL port (3306) ต่อภายนอก

4. **Backup ข้อมูล:**
   - Backup MySQL volume ทุกวัน
   - เก็บ backup นอกเครื่อง

---

## 💾 การ Backup และ Restore

### Backup Database

```bash
# Export ข้อมูลทั้งหมด
docker-compose exec mysql mysqldump -u root -p monitor_db > backup.sql

# หรือใช้ environment variable
docker-compose exec mysql mysqldump -u monitor_user -p[PASSWORD] monitor_db > backup_$(date +%Y%m%d).sql
```

### Restore Database

```bash
# Import ข้อมูล
docker-compose exec -T mysql mysql -u root -p monitor_db < backup.sql
```

### Backup Volume

```bash
# Backup MySQL volume
docker run --rm -v moniter_mysql_data:/data -v $(pwd):/backup ubuntu tar czf /backup/mysql_backup.tar.gz /data
```

---

## 🔧 การแก้ปัญหา

### ❌ Container ไม่เริ่ม

**ตรวจสอบ logs:**
```bash
docker-compose logs
```

**สาเหตุที่พบบ่อย:**
1. Port 8000 หรือ 3306 ถูกใช้งานแล้ว
   - เปลี่ยน port ใน docker-compose.yml
2. Docker Desktop ไม่ทำงาน
   - เปิด Docker Desktop
3. ไฟล์ .env ไม่ถูกต้อง
   - ตรวจสอบ syntax

---

### ❌ เชื่อมต่อ MySQL ไม่ได้

**ตรวจสอบว่า MySQL พร้อมใช้งาน:**
```bash
docker-compose exec mysql mysql -u root -p -e "SELECT 1"
```

**Restart MySQL:**
```bash
docker-compose restart mysql
```

---

### ❌ Server เชื่อมต่อ Database ไม่ได้

**ตรวจสอบ environment variables:**
```bash
docker-compose exec server env | grep DB
```

**Restart server:**
```bash
docker-compose restart server
```

---

### ❌ Agent เชื่อมต่อ Server ไม่ได้

1. **ตรวจสอบว่า Server ทำงาน:**
   ```bash
   curl http://localhost:8000/api/computers
   ```

2. **ตรวจสอบ Firewall:**
   - เปิด port 8000
   - Windows: Windows Defender Firewall
   - Linux: `sudo ufw allow 8000`

3. **ตรวจสอบ SERVER_URL ใน agent:**
   - ต้องเป็น IP ของเครื่อง Server
   - ตัวอย่าง: `http://192.168.1.100:8000`

---

## 📈 การ Scale และ Performance

### เพิ่ม Resource ให้ MySQL

แก้ไข `docker-compose.yml`:
```yaml
mysql:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 2G
      reservations:
        cpus: '1'
        memory: 1G
```

### เพิ่ม Connection Pool

แก้ไข `config_docker.py`:
```python
# เพิ่มใน database.py
engine = create_engine(
    database_url,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

---

## 🌍 Production Deployment

### ตัวอย่าง docker-compose.prod.yml

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - monitor_network
    # ไม่เปิด port ออกภายนอก

  server:
    build: .
    restart: always
    environment:
      DB_HOST: mysql
      DB_NAME: ${MYSQL_DATABASE}
      DB_USER: ${MYSQL_USER}
      DB_PASSWORD: ${MYSQL_PASSWORD}
    depends_on:
      - mysql
    networks:
      - monitor_network
    # ไม่เปิด port ออกภายนอก
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.monitor.rule=Host(`monitor.yourdomain.com`)"
      - "traefik.http.routers.monitor.tls=true"
      - "traefik.http.routers.monitor.tls.certresolver=letsencrypt"

  traefik:
    image: traefik:v2.10
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./traefik/acme.json:/acme.json
    networks:
      - monitor_network

networks:
  monitor_network:
    driver: bridge

volumes:
  mysql_data:
```

---

## 📝 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| MYSQL_ROOT_PASSWORD | - | รหัสผ่าน root ของ MySQL |
| MYSQL_DATABASE | monitor_db | ชื่อ database |
| MYSQL_USER | monitor_user | MySQL username |
| MYSQL_PASSWORD | - | MySQL password |
| SERVER_HOST | 0.0.0.0 | IP ที่ Server listen |
| SERVER_PORT | 8000 | Port ของ Server |
| CPU_THRESHOLD | 90 | CPU alert threshold (%) |
| RAM_THRESHOLD | 90 | RAM alert threshold (%) |
| DISK_THRESHOLD | 90 | Disk alert threshold (%) |

---

## 🎯 Next Steps

หลังจากติดตั้ง Server ด้วย Docker แล้ว:

1. ทดสอบเข้า Dashboard: http://localhost:8000
2. ติดตั้ง Agent บนเครื่องลูกข่าย (ดู INSTALL_AGENT.md)
3. แก้ไข `config.py` ของ Agent ให้ `SERVER_URL` ชี้มาที่ Server
4. ตั้งค่า Backup อัตโนมัติ
5. ตั้งค่า Monitoring สำหรับ Server เอง

---

## ✅ Checklist การ Deploy

- [ ] ติดตั้ง Docker Desktop/Engine
- [ ] สร้างไฟล์ .env และตั้งรหัสผ่านที่ปลอดภัย
- [ ] Build และเริ่มต้น containers
- [ ] ทดสอบเข้า Dashboard
- [ ] ตั้งค่า Firewall เปิด port 8000
- [ ] ติดตั้ง Agent บนเครื่องทดสอบ
- [ ] ทดสอบ Chat system
- [ ] ตั้งค่า Backup อัตโนมัติ
- [ ] ตั้งค่า HTTPS (Production)
- [ ] จำกัดการเข้าถึง (Production)

---

**เอกสารเพิ่มเติม:**
- [README.md](README.md) - คู่มือทั่วไป
- [INSTALL_AGENT.md](INSTALL_AGENT.md) - การติดตั้ง Agent
- [QUICK_START.md](QUICK_START.md) - คู่มือเริ่มต้นด่วน
