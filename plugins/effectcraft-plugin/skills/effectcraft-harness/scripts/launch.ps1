# 使用 Windows 内置 PowerShell/.NET 准备隔离 Python，不依赖 PATH 中的解释器。
param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Arguments)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [Console]::OutputEncoding
$scriptRoot = $PSScriptRoot
function Assert-PythonReceipt([string]$root,[string]$receiptVersion=$lockData.version,[string]$receiptPlatform=$key,[string]$receiptArchive=$entry.archiveSha256) {
    try {
        $receipt = Join-Path $root 'installation.json'
        $item = Get-Item -LiteralPath $receipt
        if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $item.Length -gt 4096) { throw 'invalid receipt file' }
        $raw = [Text.UTF8Encoding]::new($false,$true).GetString([IO.File]::ReadAllBytes($receipt))
        $compact = [Text.StringBuilder]::new(); $quoted = $false
        foreach ($character in $raw.ToCharArray()) {
            if ($character -eq '\') { throw 'escaped receipt field' }
            if ($character -eq '"') { $quoted = -not $quoted }
            if ($quoted -or [int]$character -notin @(32,9,13,10)) { [void]$compact.Append($character) }
            if ($quoted -and ($character -eq "`n" -or $character -eq "`r")) { throw 'multiline receipt field' }
        }
        if ($quoted) { throw 'unclosed receipt field' }
        $fields = @(('"version":"'+$receiptVersion+'"'),('"platform":"'+$receiptPlatform+'"'),('"archiveSha256":"'+$receiptArchive+'"'))
        $valid = $false
        for ($i=0; $i -lt 3; $i++) { for ($j=0; $j -lt 3; $j++) { for ($k=0; $k -lt 3; $k++) {
            if ($i -ne $j -and $j -ne $k -and $i -ne $k -and [String]::Equals($compact.ToString(),('{'+$fields[$i]+','+$fields[$j]+','+$fields[$k]+'}'),[StringComparison]::Ordinal)) { $valid = $true }
        } } }
        if (-not $valid) { throw 'receipt identity mismatch' }
    } catch { throw 'python_installation_receipt_invalid' }
}
. (Join-Path $scriptRoot 'task_entry.ps1')
Invoke-BoundTask -Arguments $Arguments
$arch = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString().ToLowerInvariant()
$arch = @{x64='x86_64'; x86='x86'; arm64='arm64'}[$arch]
if (-not $arch) { throw 'unsupported_python_platform' }
$key = "windows-$arch"
$lockData = Get-Content -LiteralPath (Join-Path $scriptRoot 'python.lock.json') -Raw | ConvertFrom-Json
$entry = $lockData.artifacts.$key
if (-not $entry) { throw 'unsupported_python_platform' }
if ($env:OS -ne 'Windows_NT') { throw 'windows_host_required' }
if ([Environment]::OSVersion.Version -lt [version]$entry.minimumSystem.windows) { throw 'minimum_windows_required' }
$base = if ($env:CRAFT_PYTHON_HOME) { $env:CRAFT_PYTHON_HOME } else { Join-Path $env:LOCALAPPDATA 'craft-runtimes/python' }
$base = [IO.Path]::GetFullPath($base)
if ($base.StartsWith($scriptRoot, [StringComparison]::OrdinalIgnoreCase)) { throw 'python_home_inside_skill' }
$readOnly = $Arguments -contains 'doctor'
if ($readOnly -and -not (Test-Path -LiteralPath (Join-Path $base "$($lockData.version)-$key"))) {
    @{platform=$key; python=@{version=$lockData.version; installed=$false}; runtimeAcceptance='NOT_RUN'; recovery='launch run prepares the pinned isolated Python'; recoveryActions=@(@{id='prepare_pinned_python'; argv=@('powershell.exe','-NoProfile','-NonInteractive','-File',(Join-Path $scriptRoot 'launch.ps1'),'--python-version'); automatic=$false})} | ConvertTo-Json -Depth 8 -Compress
    exit 0
}
if (-not $readOnly) { [IO.Directory]::CreateDirectory($base) | Out-Null }
$destination = Join-Path $base "$($lockData.version)-$key"
$mutex = $null; $stage = $null; $deadline = [DateTime]::UtcNow.AddSeconds(120)
while (-not $mutex -and -not $readOnly) {
    try { $mutex = [IO.File]::Open("$destination.lock", 'OpenOrCreate', 'ReadWrite', 'None') }
    catch [IO.IOException] { if ([DateTime]::UtcNow -ge $deadline) { throw 'python_install_busy' }; Start-Sleep -Milliseconds 100 }
}
function Assert-Tree([string]$root) {
    $manifest = Join-Path $scriptRoot $entry.integrityFile
    if ((Get-FileHash -LiteralPath $manifest -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.integritySha256) { throw 'python_manifest_checksum_mismatch' }
    $items = @(Get-ChildItem -LiteralPath $root -Recurse -Force)
    if (@($items | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) { throw 'python_runtime_symlink' }
    $files = @($items | Where-Object { -not $_.PSIsContainer -and $_.FullName -ne (Join-Path $root 'installation.json') })
    if ($files.Count -ne [IO.File]::ReadAllLines($manifest).Count) { throw 'python_runtime_inventory_changed' }
    foreach ($line in [IO.File]::ReadAllLines($manifest)) {
        $parts = $line.Split("`t"); $file = Join-Path $root $parts[2]
        if ($parts[0] -ne 'f' -or $parts[2] -match '(^/|\.\.|:)') { throw 'unsafe_python_manifest' }
        $item = Get-Item -LiteralPath $file
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'python_runtime_symlink' }
        if ((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLowerInvariant() -ne $parts[1]) { throw 'python_installed_checksum_mismatch' }
    }
}

try {
    if (-not (Test-Path -LiteralPath $destination)) {
        $stage = Join-Path $base ('.python-' + [Guid]::NewGuid().ToString('N'))
        [IO.Directory]::CreateDirectory($stage) | Out-Null
        $archive = if ($env:CRAFT_PYTHON_ARCHIVE) { $env:CRAFT_PYTHON_ARCHIVE } else { Join-Path $stage 'python.zip' }
        if (-not $env:CRAFT_PYTHON_ARCHIVE) {
            [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
            Invoke-WebRequest -UseBasicParsing -Uri $entry.url -OutFile $archive -TimeoutSec 240
        }
        if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.archiveSha256) { throw 'python_archive_checksum_mismatch' }
        $payload = Join-Path $stage 'payload'
        Expand-Archive -LiteralPath $archive -DestinationPath $payload
        Assert-Tree $payload
        @{version=$lockData.version;platform=$key;archiveSha256=$entry.archiveSha256} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $payload 'installation.json')
        Assert-PythonReceipt $payload
        [IO.Directory]::Move($payload, $destination)
    } else {
        if ((Get-Item -LiteralPath $destination).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'python_runtime_symlink' }
        Assert-PythonReceipt $destination
        Assert-Tree $destination
    }
} finally {
    if ($stage -and (Test-Path -LiteralPath $stage)) { Remove-Item -LiteralPath $stage -Recurse -Force }
    if ($mutex) { $mutex.Dispose() }
}
$python = Join-Path $destination $entry.executable
if ($Arguments.Count -eq 1 -and $Arguments[0] -eq '--python-version') { & $python -I -B --version }
else { & $python -I -B (Join-Path $scriptRoot 'managed.py') @Arguments }
exit $LASTEXITCODE
