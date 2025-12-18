# Configuration file for PC Monitor & Chat System

# Server Configuration
SERVER_HOST = "10.31.112.155"
SERVER_PORT = 8000
DATABASE_URL = "sqlite:///./monitor.db"

# Agent Configuration
AGENT_NAME = ""  # Leave empty to auto-detect hostname
SERVER_URL = "http://localhost:8000"  # Update this to your server IP address
UPDATE_INTERVAL = 30  # seconds - how often to send monitoring data

# Thresholds for alerts
CPU_THRESHOLD = 90  # percent
RAM_THRESHOLD = 90  # percent
DISK_THRESHOLD = 90  # percent

# Alert settings
ENABLE_ALERTS = True
AUTO_REPORT_ISSUES = True  # Automatically notify admin when threshold exceeded

# Chat settings
CHAT_HISTORY_LIMIT = 100  # Number of messages to keep in memory
