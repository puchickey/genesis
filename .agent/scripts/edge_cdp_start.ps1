Write-Output "Stopping all Edge instances to release the debugger port..."
Stop-Process -Name msedge -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3

Write-Output "Starting Edge with Remote Debugging (Port 9223)..."
Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" -ArgumentList "--remote-debugging-port=9223","--remote-debugging-address=127.0.0.1","--remote-allow-origins=*"

Write-Output "Edge has been launched in CDP-ready mode."
Write-Output "You can now execute cdp_browser.py to manipulate the session."
