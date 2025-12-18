@echo off
chcp 65001 >nul
echo ========================================
echo   ติดตั้ง Monitor Agent
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% equ 0 goto :python_found

py --version >nul 2>&1
if %errorlevel% equ 0 goto :py_found

:no_python
echo ❌ ERROR: ไม่พบ Python ในระบบ
echo.
echo กรุณาติดตั้ง Python ก่อน:
echo 1. ไปที่ https://www.python.org/downloads/
echo 2. ดาวน์โหลดและติดตั้ง Python
echo 3. ติ๊กถูก "Add Python to PATH" ตอนติดตั้ง
echo 4. เปิด Command Prompt ใหม่และรันไฟล์นี้อีกครั้ง
echo.
pause
exit /b 1

:python_found
set PYTHON_CMD=python
goto :install

:py_found
set PYTHON_CMD=py
goto :install

:install
echo ✅ พบ Python แล้ว
%PYTHON_CMD% --version
echo.

REM Check if config.py exists
if not exist config.py (
    echo ❌ ERROR: ไม่พบไฟล์ config.py
    echo กรุณาคัดลอกไฟล์ config.py มาไว้ในโฟลเดอร์นี้
    pause
    exit /b 1
)

REM Check if agent.py exists
if not exist agent.py (
    echo ❌ ERROR: ไม่พบไฟล์ agent.py
    echo กรุณาคัดลอกไฟล์ agent.py มาไว้ในโฟลเดอร์นี้
    pause
    exit /b 1
)

REM Check if requirements.txt exists
if not exist requirements.txt (
    echo ❌ ERROR: ไม่พบไฟล์ requirements.txt
    echo กรุณาคัดลอกไฟล์ requirements.txt มาไว้ในโฟลเดอร์นี้
    pause
    exit /b 1
)

echo ========================================
echo   กำลังติดตั้ง Python Libraries...
echo ========================================
echo.

%PYTHON_CMD% -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: ติดตั้ง libraries ล้มเหลว
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ติดตั้งเสร็จสมบูรณ์!
echo ========================================
echo.
echo ✅ Agent พร้อมใช้งานแล้ว
echo.
echo วิธีเริ่มใช้งาน:
echo   1. แก้ไขไฟล์ config.py (ใส่ IP ของ Server)
echo   2. รันคำสั่ง: %PYTHON_CMD% agent.py
echo   3. หรือดับเบิลคลิก start_agent.bat
echo.
echo หมายเหตุ:
echo   - ตรวจสอบว่า Server กำลังทำงานอยู่
echo   - ตรวจสอบว่า SERVER_URL ใน config.py ถูกต้อง
echo.
pause
