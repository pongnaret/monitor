@echo off
chcp 65001 >nul
echo ========================================
echo   PC Monitor Server - Docker
echo ========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo ⚠️  ไม่พบไฟล์ .env
    echo กำลังสร้างจากไฟล์ตัวอย่าง...
    copy .env.example .env
    echo.
    echo ✅ สร้างไฟล์ .env แล้ว
    echo ⚠️  กรุณาแก้ไขไฟล์ .env ให้รหัสผ่านปลอดภัยก่อนใช้งานจริง!
    echo.
    pause
)

echo กำลังเริ่มต้น Docker containers...
echo.

docker-compose up -d

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   ✅ เริ่มต้นสำเร็จ!
    echo ========================================
    echo.
    echo 📊 Dashboard: http://localhost:8000
    echo 🗄️  MySQL: localhost:3306
    echo.
    echo คำสั่งที่เป็นประโยชน์:
    echo   - ดู logs:        docker-compose logs -f
    echo   - ดู logs server: docker-compose logs -f server
    echo   - หยุดระบบ:       docker-compose stop
    echo   - ลบระบบ:         docker-compose down
    echo.
    echo กำลังแสดง logs...
    echo กด Ctrl+C เพื่อหยุดดู logs (container ยังทำงานอยู่)
    echo.
    timeout /t 3 >nul
    docker-compose logs -f server
) else (
    echo.
    echo ❌ เกิดข้อผิดพลาด!
    echo กรุณาตรวจสอบว่า Docker Desktop กำลังทำงานอยู่
    pause
)
