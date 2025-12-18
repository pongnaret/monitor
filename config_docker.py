# Configuration file for PC Monitor & Chat System - Docker Version
import os

# Server Configuration (from environment variables)
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

# Database Configuration
DB_TYPE = os.getenv("DB_TYPE", "mysql")
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "monitor_db")
DB_USER = os.getenv("DB_USER", "monitor_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "monitor_password")

# Build DATABASE_URL based on DB_TYPE
if DB_TYPE == "mysql":
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
elif DB_TYPE == "sqlite":
    DATABASE_URL = "sqlite:///./monitor.db"
else:
    # Default to MySQL
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# Agent Configuration (not used in server, but kept for compatibility)
AGENT_NAME = ""
SERVER_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"
UPDATE_INTERVAL = 30

# Thresholds for alerts
CPU_THRESHOLD = int(os.getenv("CPU_THRESHOLD", "90"))
RAM_THRESHOLD = int(os.getenv("RAM_THRESHOLD", "90"))
DISK_THRESHOLD = int(os.getenv("DISK_THRESHOLD", "90"))

# Alert settings
ENABLE_ALERTS = os.getenv("ENABLE_ALERTS", "True").lower() == "true"
AUTO_REPORT_ISSUES = os.getenv("AUTO_REPORT_ISSUES", "True").lower() == "true"

# Chat settings
CHAT_HISTORY_LIMIT = int(os.getenv("CHAT_HISTORY_LIMIT", "100"))
