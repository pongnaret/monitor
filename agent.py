"""
Agent สำหรับติดตั้งบนเครื่องลูกข่าย
- ส่งข้อมูล monitoring ไปที่ server
- รับ-ส่งข้อความ chat กับ admin
- แจ้งเตือนอัตโนมัติเมื่อเกิดปัญหา
"""
import psutil
import platform
import socket
import time
import requests
from datetime import datetime
import threading
import config
import sys


class MonitorAgent:
    def __init__(self):
        self.hostname = config.AGENT_NAME or socket.gethostname()
        self.server_url = config.SERVER_URL
        self.is_running = True
        self.computer_id = None

        # ลงทะเบียนเครื่องกับ server
        self.register()

    def register(self):
        """ลงทะเบียนเครื่องกับ server"""
        try:
            data = {
                "hostname": self.hostname,
                "ip_address": self.get_ip_address(),
                "os_info": f"{platform.system()} {platform.release()}"
            }
            response = requests.post(f"{self.server_url}/api/register", json=data, timeout=5)
            if response.status_code == 200:
                result = response.json()
                self.computer_id = result.get("computer_id")
                print(f"✅ ลงทะเบียนสำเร็จ: {self.hostname} (ID: {self.computer_id})")
            else:
                print(f"❌ ลงทะเบียนล้มเหลว: {response.status_code}")
        except Exception as e:
            print(f"❌ ไม่สามารถเชื่อมต่อ server: {e}")
            sys.exit(1)

    def get_ip_address(self):
        """ดึง IP address ของเครื่อง"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def collect_metrics(self):
        """เก็บข้อมูล metrics ของเครื่อง"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()

            # Memory
            memory = psutil.virtual_memory()
            ram_total = memory.total / (1024 ** 3)  # Convert to GB
            ram_used = memory.used / (1024 ** 3)
            ram_percent = memory.percent

            # Disk
            disk = psutil.disk_usage('/')
            disk_total = disk.total / (1024 ** 3)  # Convert to GB
            disk_used = disk.used / (1024 ** 3)
            disk_percent = disk.percent

            # Network
            net_io = psutil.net_io_counters()
            network_sent = net_io.bytes_sent / (1024 ** 2)  # Convert to MB
            network_recv = net_io.bytes_recv / (1024 ** 2)

            # Uptime
            uptime_seconds = int(time.time() - psutil.boot_time())

            metrics = {
                "computer_id": self.computer_id,
                "cpu_percent": cpu_percent,
                "cpu_count": cpu_count,
                "ram_total": round(ram_total, 2),
                "ram_used": round(ram_used, 2),
                "ram_percent": ram_percent,
                "disk_total": round(disk_total, 2),
                "disk_used": round(disk_used, 2),
                "disk_percent": disk_percent,
                "network_sent": round(network_sent, 2),
                "network_recv": round(network_recv, 2),
                "uptime_seconds": uptime_seconds
            }

            return metrics
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการเก็บข้อมูล: {e}")
            return None

    def send_metrics(self):
        """ส่งข้อมูล metrics ไปที่ server"""
        metrics = self.collect_metrics()
        if metrics:
            try:
                response = requests.post(
                    f"{self.server_url}/api/metrics",
                    json=metrics,
                    timeout=5
                )

                if response.status_code == 200:
                    print(f"📊 ส่งข้อมูล metrics สำเร็จ - CPU: {metrics['cpu_percent']}% | RAM: {metrics['ram_percent']}%")

                    # ตรวจสอบและแจ้งเตือนอัตโนมัติ
                    self.check_alerts(metrics)
                else:
                    print(f"⚠️ ส่งข้อมูลล้มเหลว: {response.status_code}")
            except Exception as e:
                print(f"❌ ไม่สามารถส่งข้อมูล: {e}")

    def check_alerts(self, metrics):
        """ตรวจสอบและส่งการแจ้งเตือนอัตโนมัติ"""
        if not config.AUTO_REPORT_ISSUES:
            return

        alerts = []

        if metrics['cpu_percent'] > config.CPU_THRESHOLD:
            alerts.append(f"⚠️ CPU สูงเกินกำหนด: {metrics['cpu_percent']}%")

        if metrics['ram_percent'] > config.RAM_THRESHOLD:
            alerts.append(f"⚠️ RAM สูงเกินกำหนด: {metrics['ram_percent']}%")

        if metrics['disk_percent'] > config.DISK_THRESHOLD:
            alerts.append(f"⚠️ Disk เต็มเกินกำหนด: {metrics['disk_percent']}%")

        # ส่งการแจ้งเตือนไปที่ admin ผ่าน chat
        for alert in alerts:
            self.send_chat_message(alert)

    def send_chat_message(self, message):
        """ส่งข้อความ chat ไปที่ admin"""
        try:
            data = {
                "computer_id": self.computer_id,
                "sender": "agent",
                "message": message
            }
            response = requests.post(
                f"{self.server_url}/api/chat/send",
                json=data,
                timeout=5
            )
            if response.status_code == 200:
                print(f"💬 ส่งข้อความ: {message}")
        except Exception as e:
            print(f"❌ ส่งข้อความล้มเหลว: {e}")

    def check_new_messages(self):
        """ตรวจสอบข้อความใหม่จาก admin"""
        try:
            response = requests.get(
                f"{self.server_url}/api/chat/messages/{self.computer_id}",
                timeout=5
            )
            if response.status_code == 200:
                messages = response.json()
                unread_messages = [msg for msg in messages if not msg.get('is_read') and msg.get('sender') == 'admin']

                for msg in unread_messages:
                    print(f"\n💬 ข้อความจาก Admin: {msg['message']}")
                    print(f"   เวลา: {msg['timestamp']}\n")

                    # ทำเครื่องหมายว่าอ่านแล้ว
                    self.mark_message_read(msg['id'])
        except Exception as e:
            pass  # Silent fail for message checking

    def mark_message_read(self, message_id):
        """ทำเครื่องหมายว่าอ่านข้อความแล้ว"""
        try:
            requests.put(
                f"{self.server_url}/api/chat/read/{message_id}",
                timeout=5
            )
        except:
            pass

    def interactive_chat(self):
        """โหมด chat แบบ interactive"""
        print("\n" + "="*50)
        print("💬 โหมด Chat กับ Admin")
        print("พิมพ์ 'exit' เพื่อออกจากโหมด chat")
        print("="*50 + "\n")

        while True:
            try:
                message = input("คุณ: ").strip()
                if message.lower() == 'exit':
                    break
                if message:
                    self.send_chat_message(message)
            except KeyboardInterrupt:
                break

        print("\n✅ ออกจากโหมด chat\n")

    def run(self):
        """รันโปรแกรม agent"""
        print(f"\n🚀 เริ่มต้น Monitoring Agent")
        print(f"📡 Server: {self.server_url}")
        print(f"🖥️  เครื่อง: {self.hostname}")
        print(f"⏱️  อัพเดตทุก {config.UPDATE_INTERVAL} วินาที\n")
        print("กด Ctrl+C เพื่อหยุด หรือพิมพ์ 'chat' เพื่อเข้าโหมด chat\n")

        # สร้าง thread สำหรับตรวจสอบข้อความ
        def message_checker():
            while self.is_running:
                self.check_new_messages()
                time.sleep(10)  # Check every 10 seconds

        msg_thread = threading.Thread(target=message_checker, daemon=True)
        msg_thread.start()

        try:
            while self.is_running:
                self.send_metrics()

                # รอหรือรับคำสั่ง
                for _ in range(config.UPDATE_INTERVAL):
                    time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n⏹️  หยุดการทำงาน...")
            self.is_running = False


def main():
    """Main function"""
    agent = MonitorAgent()

    # ตรวจสอบ command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == 'chat':
        agent.interactive_chat()
    else:
        agent.run()


if __name__ == "__main__":
    main()
