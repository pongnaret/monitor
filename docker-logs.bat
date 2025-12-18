@echo off
chcp 65001 >nul
echo ========================================
echo   PC Monitor Server - Logs
echo ========================================
echo.
echo กด Ctrl+C เพื่อหยุดดู logs
echo.

docker-compose logs -f server
