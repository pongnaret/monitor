# Configuration file for PC Monitor & Chat System - AGENT ONLY

# ⚠️ สำคัญ: แก้ไข SERVER_URL ให้ตรงกับ IP ของเครื่อง Server
SERVER_URL = "http://10.31.112.155:8000"  # <-- เปลี่ยนที่นี่!

# Agent Configuration
AGENT_NAME = ""  # เว้นว่างไว้จะใช้ชื่อเครื่องอัตโนมัติ
UPDATE_INTERVAL = 30  # วินาที - ส่งข้อมูลทุกกี่วินาที

# ค่าเกินกำหนดสำหรับการแจ้งเตือนอัตโนมัติ
CPU_THRESHOLD = 90  # เปอร์เซ็นต์
RAM_THRESHOLD = 90  # เปอร์เซ็นต์
DISK_THRESHOLD = 90  # เปอร์เซ็นต์

# การตั้งค่าการแจ้งเตือน
ENABLE_ALERTS = True
AUTO_REPORT_ISSUES = True  # แจ้ง Admin อัตโนมัติเมื่อเกินค่ากำหนด

# Chat settings
CHAT_HISTORY_LIMIT = 100  # จำนวนข้อความที่เก็บ

# หมายเหตุ:
# - SERVER_URL ต้องขึ้นต้นด้วย http:// และลงท้ายด้วย :8000
# - ตัวอย่าง: "http://192.168.1.100:8000"
# - ตรวจสอบให้แน่ใจว่า Server กำลังทำงานอยู่
# - ถ้า ping Server ไม่ผ่าน = ปัญหาเครือข่าย
