@echo off
chcp 65001 >nul
echo ========================================
echo   Restart PC Monitor Server
echo ========================================
echo.

echo กำลัง restart...
docker-compose restart

if %errorlevel% equ 0 (
    echo ✅ Restart สำเร็จ
    echo.
    echo กำลังแสดง logs...
    timeout /t 2 >nul
    docker-compose logs -f server
) else (
    echo ❌ เกิดข้อผิดพลาด
    pause
)
