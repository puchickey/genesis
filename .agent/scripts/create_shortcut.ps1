$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path -Path $DesktopPath -ChildPath "Antigravity CDP Mode.lnk"
$TargetPath = "C:\my_tools\Antigravity\_\Antigravity.exe"

$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.Arguments = "--remote-debugging-port=9224 --remote-allow-origins=*"
$Shortcut.Save()

Write-Output "Shortcut recreated successfully."
