"""
Database models and connection setup
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
import config
import sys
import os

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Get database URL from config or environment
database_url = os.getenv('DATABASE_URL', config.DATABASE_URL)

# Configure connection arguments based on database type
connect_args = {}
if database_url.startswith('sqlite'):
    connect_args = {"check_same_thread": False}

# Database setup
engine = create_engine(
    database_url,
    connect_args=connect_args,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
    echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Computer(Base):
    """เก็บข้อมูลเครื่องคอมพิวเตอร์"""
    __tablename__ = "computers"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String(255), unique=True, index=True)
    ip_address = Column(String(45))  # IPv6 max length
    os_info = Column(String(255))
    is_online = Column(Boolean, default=False)
    last_seen = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    metrics = relationship("Metric", back_populates="computer", cascade="all, delete-orphan")
    messages = relationship("ChatMessage", back_populates="computer", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="computer", cascade="all, delete-orphan")


class Metric(Base):
    """เก็บข้อมูล metrics ของแต่ละเครื่อง"""
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    computer_id = Column(Integer, ForeignKey("computers.id"))
    timestamp = Column(DateTime, default=datetime.now, index=True)

    # CPU metrics
    cpu_percent = Column(Float)
    cpu_count = Column(Integer)

    # Memory metrics
    ram_total = Column(Float)  # GB
    ram_used = Column(Float)   # GB
    ram_percent = Column(Float)

    # Disk metrics
    disk_total = Column(Float)  # GB
    disk_used = Column(Float)   # GB
    disk_percent = Column(Float)

    # Network
    network_sent = Column(Float)  # MB
    network_recv = Column(Float)  # MB

    # System uptime
    uptime_seconds = Column(Integer)

    # Relationship
    computer = relationship("Computer", back_populates="metrics")


class ChatMessage(Base):
    """เก็บข้อความ chat ระหว่าง agent และ admin"""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    computer_id = Column(Integer, ForeignKey("computers.id"))
    sender = Column(String(50))  # "agent" or "admin"
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    is_read = Column(Boolean, default=False)

    # Relationship
    computer = relationship("Computer", back_populates="messages")


class Alert(Base):
    """เก็บประวัติการแจ้งเตือน"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    computer_id = Column(Integer, ForeignKey("computers.id"))
    alert_type = Column(String(50))  # "cpu", "ram", "disk", "offline"
    message = Column(Text)
    value = Column(Float, nullable=True)
    threshold = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    is_resolved = Column(Boolean, default=False)

    # Relationship
    computer = relationship("Computer", back_populates="alerts")


def init_db():
    """สร้าง database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
