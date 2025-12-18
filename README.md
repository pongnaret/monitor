# 🖥️ PC Monitor & Chat System

[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal.svg)](https://fastapi.tiangolo.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

ระบบ Monitoring เครื่องคอมพิวเตอร์ในเครือข่าย LAN พร้อม Chat Real-time ระหว่าง Admin และเครื่องลูกข่าย

[English](#english) | [ไทย](#thai)

---

## ✨ Features

### 📊 Real-time Monitoring
- ✅ CPU, RAM, Disk usage tracking
- ✅ Network statistics
- ✅ System uptime monitoring
- ✅ Online/Offline status detection
- ✅ Automatic alerts when thresholds exceeded

### 💬 Chat System
- ✅ Real-time messaging between admin and clients
- ✅ WebSocket-based instant updates
- ✅ Automatic issue notifications
- ✅ Message history storage

### 🐳 Docker Ready
- ✅ Complete Docker Compose setup
- ✅ MySQL database with persistent storage
- ✅ Production-ready configuration
- ✅ Easy deployment and scaling

### 🎨 Modern Dashboard
- ✅ Beautiful, responsive web interface
- ✅ Real-time metrics visualization
- ✅ One-click chat interface
- ✅ Alert notifications

---

## 🚀 Quick Start

### For Server (Docker)

```bash
# 1. Clone repository
git clone https://github.com/pongnaret/monitor.git
cd monitor

# 2. Setup environment
cp .env.example .env
# Edit .env and set secure passwords

# 3. Start with Docker
docker-compose up -d

# 4. Access Dashboard
# http://localhost:8000
```

### For Client Computers

1. Copy agent files: `agent.py`, `config.py`, `requirements.txt`
2. Edit `config.py`:
   ```python
   SERVER_URL = "http://YOUR_SERVER_IP:8000"
   ```
3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Run agent:
   ```bash
   python agent.py
   ```

---

## 📸 Screenshots

### Dashboard
![Dashboard](docs/images/dashboard.png)

### Chat Interface
![Chat](docs/images/chat.png)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│         Docker Host                 │
│  ┌───────────────────────────────┐ │
│  │  monitor_server (FastAPI)     │ │
│  │  Port: 8000                   │ │
│  └─────────────┬─────────────────┘ │
│                │                    │
│                ▼                    │
│  ┌───────────────────────────────┐ │
│  │  monitor_mysql (MySQL 8.0)    │ │
│  │  Volume: mysql_data           │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
         ▲
         │ HTTP/WebSocket
         │
    ┌────┴─────┐
    │          │
┌───▼──┐   ┌──▼───┐
│Agent │   │Agent │  ... (Client PCs)
└──────┘   └──────┘
```

---

## 📁 Project Structure

```
monitor/
├── 🐳 Docker Setup
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .dockerignore
│   ├── .env.example
│   └── config_docker.py
│
├── 🖥️ Server
│   ├── server.py              # FastAPI application
│   ├── database.py            # SQLAlchemy models
│   └── templates/
│       └── dashboard.html     # Admin dashboard
│
├── 📱 Agent (Client)
│   ├── agent.py               # Client monitoring agent
│   ├── config_agent_template.py
│   └── install_agent.bat      # Auto-installer
│
├── 📚 Documentation
│   ├── README.md
│   ├── DOCKER_DEPLOYMENT.md
│   ├── INSTALL_AGENT.md
│   └── QUICK_START.md
│
└── 🔧 Configuration
    ├── config.py
    └── requirements.txt
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **MySQL** - Production database
- **WebSocket** - Real-time communication

### Frontend
- **HTML/CSS/JavaScript** - Dashboard UI
- **WebSocket API** - Real-time updates

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

### Agent
- **psutil** - System monitoring
- **requests** - HTTP client

---

## 📊 Monitored Metrics

| Metric | Description |
|--------|-------------|
| CPU Usage | Percentage and core count |
| RAM Usage | Total, used, and percentage |
| Disk Usage | Total, used, and percentage |
| Network | Bytes sent/received |
| Uptime | System uptime in seconds |
| Status | Online/Offline detection |

---

## 🔔 Alert System

Automatic alerts when:
- CPU usage > 90%
- RAM usage > 90%
- Disk usage > 90%
- Computer goes offline

Configurable thresholds in `config.py`

---

## 💬 Chat Features

- **Admin → Agent**: Send commands, ask status
- **Agent → Admin**: Report issues, ask for help
- **Automatic**: System alerts sent as chat messages
- **History**: All messages stored in database

---

## 🐳 Docker Commands

```bash
# Start system
docker-compose up -d

# Stop system
docker-compose stop

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Remove (with data)
docker-compose down -v

# Backup database
docker-compose exec mysql mysqldump -u root -p monitor_db > backup.sql
```

---

## 🔒 Security

### Production Checklist
- [ ] Change all passwords in `.env`
- [ ] Use HTTPS with reverse proxy
- [ ] Don't expose MySQL port externally
- [ ] Configure firewall rules
- [ ] Enable automatic backups
- [ ] Use Docker secrets for sensitive data

---

## 📖 Documentation

- [Quick Start](QUICK_START.md) - Get started in 3 steps
- [Docker Deployment](DOCKER_DEPLOYMENT.md) - Complete Docker guide
- [Agent Installation](INSTALL_AGENT.md) - Client setup guide
- [Package Distribution](PACKAGE_FOR_AGENTS.md) - Deploy to multiple PCs

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 TODO / Roadmap

- [ ] Add user authentication for admin
- [ ] Export reports to PDF/Excel
- [ ] Real-time charts and graphs
- [ ] Email notifications
- [ ] Mobile app for admin
- [ ] Remote control features
- [ ] Screenshot capability
- [ ] Multi-admin support
- [ ] Advanced alerting rules

---

## 🐛 Known Issues

- WebSocket may disconnect on slow networks (auto-reconnect enabled)
- Large deployments (100+ agents) may need connection pool tuning

See [Issues](https://github.com/pongnaret/monitor/issues) for more.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**pongnaret**

- GitHub: [@pongnaret](https://github.com/pongnaret)
- Repository: [monitor](https://github.com/pongnaret/monitor)

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI inspired by modern admin dashboards
- Generated with assistance from [Claude Code](https://claude.com/claude-code)

---

## 📞 Support

- 📧 Create an [Issue](https://github.com/pongnaret/monitor/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/pongnaret/monitor/discussions)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ for IT administrators everywhere

</div>

---

<a name="thai"></a>
# 🇹🇭 คู่มือภาษาไทย

[ดูคู่มือฉบับเต็มภาษาไทย](README.md)

## เริ่มต้นใช้งาน

### สำหรับ Server (Docker)
```bash
git clone https://github.com/pongnaret/monitor.git
cd monitor
copy .env.example .env
# แก้ไขรหัสผ่านใน .env
docker-compose up -d
# เปิด http://localhost:8000
```

### สำหรับเครื่องลูกข่าย
```bash
# แก้ไข config.py
SERVER_URL = "http://192.168.1.100:8000"

# ติดตั้ง
python -m pip install -r requirements.txt

# รัน
python agent.py
```

---

<div align="center">

**Built with 🤖 Claude Code**

</div>
