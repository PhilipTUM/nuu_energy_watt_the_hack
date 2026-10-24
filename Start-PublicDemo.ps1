param([int]$Port = 8012)
$ErrorActionPreference = 'Stop'
$projectPath = $PSScriptRoot
$runtimePath = Join-Path $projectPath '.runtime'
$statePath = Join-Path $runtimePath 'public-demo.json'
New-Item -ItemType Directory -Path $runtimePath -Force | Out-Null
if (Test-Path -LiteralPath $statePath) {
    $saved = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
    $alive = @($saved.processes | Where-Object {
        $p = Get-Process -Id $_.id -ErrorAction SilentlyContinue
        $p -and $p.StartTime.ToUniversalTime().Ticks.ToString() -eq $_.startTicks
    })
    if ($alive.Count -eq 2) { Write-Output $saved.url; return }
    & (Join-Path $projectPath 'Stop-PublicDemo.ps1')
}
if ($Port -lt 1024 -or $Port -gt 65535) { throw 'Invalid port.' }
$listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, $Port)
try { $listener.Start() } finally { $listener.Stop() }
$cloudflared = Join-Path $runtimePath 'cloudflared.exe'
if (-not (Test-Path -LiteralPath $cloudflared)) {
    Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile $cloudflared -UseBasicParsing
}
$pythonCandidates = @(
    (Join-Path $projectPath '.venv\Scripts\python.exe'),
    (Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'),
    (Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe')
)
$pythonPath = $pythonCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $pythonPath) { throw 'Python not found. Create a .venv in this project first.' }
$tunnelLog = Join-Path $runtimePath 'tunnel-error.log'
$tunnelOut = Join-Path $runtimePath 'tunnel-output.log'
$processes = @()
function Record-Process($process, $executable) {
    @{ id=$process.Id; startTicks=$process.StartTime.ToUniversalTime().Ticks.ToString(); executable=$executable }
}
try {
    $tunnel = Start-Process -FilePath $cloudflared -ArgumentList @('tunnel','--no-autoupdate','--protocol','http2','--url',"http://127.0.0.1:$Port") -WorkingDirectory $projectPath -WindowStyle Hidden -RedirectStandardOutput $tunnelOut -RedirectStandardError $tunnelLog -PassThru
    $processes += Record-Process $tunnel $cloudflared
    $deadline = [DateTime]::UtcNow.AddSeconds(60)
    $publicUrl = $null
    while ([DateTime]::UtcNow -lt $deadline) {
        if ($tunnel.HasExited) { throw "Tunnel stopped. See $tunnelLog" }
        if (Test-Path -LiteralPath $tunnelLog) {
            $text = Get-Content -LiteralPath $tunnelLog -Raw
            if ($text -match 'https://[a-z0-9-]+\.trycloudflare\.com') { $publicUrl=$Matches[0]; break }
        }
        Start-Sleep -Milliseconds 500
    }
    if (-not $publicUrl) { throw "No public URL received. See $tunnelLog" }
    $server = Start-Process -FilePath $pythonPath -ArgumentList @('-B','-m','heat_pump_ready','--runner','disabled','--port',"$Port",'--public-origin',$publicUrl) -WorkingDirectory $projectPath -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runtimePath 'server-output.log') -RedirectStandardError (Join-Path $runtimePath 'server-error.log') -PassThru
    $processes += Record-Process $server $pythonPath
    $deadline = [DateTime]::UtcNow.AddSeconds(15)
    $ready = $false
    while ([DateTime]::UtcNow -lt $deadline) {
        if ($server.HasExited) { throw 'Server stopped. See .runtime/server-error.log.' }
        try {
            $health = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/api/health" -TimeoutSec 2
            if ($health.status -eq 'ready') { $ready=$true; break }
        } catch { Start-Sleep -Milliseconds 500 }
    }
    if (-not $ready) { throw 'Local demo server did not become ready.' }
    @{url=$publicUrl; port=$Port; created=[DateTime]::UtcNow.ToString('o'); processes=$processes} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $statePath -Encoding UTF8
    Set-Content -LiteralPath (Join-Path $runtimePath 'public-url.txt') -Value $publicUrl -Encoding UTF8
    Write-Output $publicUrl
    Write-Output 'Demo running. Stop with .\Stop-PublicDemo.ps1. Keep this laptop online.'
} catch {
    foreach ($entry in $processes) {
        $p=Get-Process -Id $entry.id -ErrorAction SilentlyContinue
        if ($p -and $p.StartTime.ToUniversalTime().Ticks.ToString() -eq $entry.startTicks) { Stop-Process -Id $p.Id }
    }
    throw
}
