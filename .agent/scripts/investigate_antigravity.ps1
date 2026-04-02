$ErrorActionPreference = "SilentlyContinue"

Write-Output "========================================"
Write-Output "AntiGravity / Genesis Environment Scanner"
Write-Output "========================================"

# 1. Locate relevant processes
Write-Output "`n[1] Scanning Processes..."
$targetProcesses = Get-CimInstance Win32_Process | Where-Object { $_.Name -match "antigravity|gemini|electron|node|code" }
foreach ($p in $targetProcesses) {
    Write-Output "PID: $($p.ProcessId) | Name: $($p.Name)"
    Write-Output "Command: $($p.CommandLine)"
    Write-Output "---"
}

# 2. Check Open Ports
Write-Output "`n[2] Scanning Network Ports for target processes..."
$netstat = netstat -ano
foreach ($p in $targetProcesses) {
    $matches = $netstat | Select-String " $($p.ProcessId)$"
    if ($matches) {
        Write-Output "-> Network Activity found for PID $($p.ProcessId) ($($p.Name)):"
        $matches | ForEach-Object { Write-Output "   $($_)" }
    }
}

# 3. Check Named Pipes
Write-Output "`n[3] Scanning Named Pipes..."
$pipes = Get-ChildItem \\.\pipe\ | Where-Object { $_.Name -match "antigravity|gemini|vscode|cursor|cline|mcp|ipc" }
if ($pipes) {
    $pipes | Select-Object Name | ForEach-Object { Write-Output "Found Pipe: $($_.Name)" }
} else {
    Write-Output "No matching named pipes found."
}

# 4. Registry / URI Handlers
Write-Output "`n[4] Scanning URL Protocol Handlers..."
$handlers = Get-Item "HKCR:\*" | Where-Object { $_.GetValue("URL Protocol") -ne $null }
$targetHandlers = $handlers | Where-Object { $_.Name -match "antigravity|gemini|vscode" }
if ($targetHandlers) {
    foreach ($h in $targetHandlers) {
        $cmd = (Get-ItemProperty "$($h.PSPath)\shell\open\command" -ErrorAction SilentlyContinue).'(default)'
        Write-Output "Protocol: $($h.PSChildName) -> Command: $cmd"
    }
} else {
    Write-Output "No distinct custom URL protocols found."
}

Write-Output "`n========================================"
Write-Output "Scan Complete."
