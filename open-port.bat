@echo off
echo ========================================
echo   Open Firewall Port 8090
echo ========================================
echo.
echo Please run this script as Administrator!
echo.
pause

echo Opening port 8090...
netsh advfirewall firewall add rule name="Earthquake-App-8090" dir=in action=allow protocol=tcp localport=8090

if %errorlevel% equ 0 (
    echo.
    echo Success! Port 8090 is now open.
    echo.
    echo You can now access from other devices:
    echo http://192.168.1.42:8090
) else (
    echo.
    echo Failed! Please run as Administrator.
)

echo.
pause
