@echo off
chcp 65001 >nul
echo ========================================
echo   หยุด PC Monitor Server
echo ========================================
echo.

docker-compose stop

if %errorlevel% equ 0 (
    echo ✅ หยุดระบบเรียบร้อยแล้ว
) else (
    echo ❌ เกิดข้อผิดพลาด
)

pause
