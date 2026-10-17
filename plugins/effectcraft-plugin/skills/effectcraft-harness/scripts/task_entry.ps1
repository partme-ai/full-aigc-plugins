# 安装前仅验证固定任务描述；不执行任务目录中的Shell代码。
$ErrorActionPreference='Stop'
function Fail-Entry([string]$reason) { throw "bound_entry_invalid: $reason" }
function Read-EntryText([string]$path,[long]$limit) {
    try { $item=Get-Item -LiteralPath $path -ErrorAction Stop }
    catch { Fail-Entry 'file_unavailable' }
    if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $item.Length -gt $limit) { Fail-Entry 'file' }
    return [Text.UTF8Encoding]::new($false,$true).GetString([IO.File]::ReadAllBytes($path))
}
function Hash-EntryText([string]$text) {
    $hash=[Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($hash.ComputeHash([Text.Encoding]::UTF8.GetBytes($text)))).Replace('-','').ToLowerInvariant() }
    finally { $hash.Dispose() }
}
function Assert-EntryIdentity([string]$state,[string]$identity,[string]$sha) {
    # 深度和字符串转义防止计划里的同名字段冒充顶层身份。
    $depth=0;$quoted=$false;$escaped=$false;$identities=0;$hashes=0;$token='"identity":';$hashToken='"identityHash":"'+$sha+'"'
    for ($i=0;$i -lt $state.Length;$i++) {
        $c=$state[$i]
        if (-not $quoted -and $depth -eq 1) {
            if ($state.Substring($i).StartsWith($token,[StringComparison]::Ordinal)) {
                $identities++;$start=$i+$token.Length
                if ($state.Length -le $start+$identity.Length -or -not [String]::Equals($state.Substring($start,$identity.Length),$identity,[StringComparison]::Ordinal) -or $state[$start+$identity.Length] -ne ',') { Fail-Entry 'identity_mismatch' }
            }
            if ($state.Substring($i).StartsWith('"identityHash":',[StringComparison]::Ordinal)) {
                $hashes++;if (-not $state.Substring($i).StartsWith($hashToken,[StringComparison]::Ordinal)) { Fail-Entry 'identity_mismatch' }
            }
        }
        if ($quoted) {
            if ($escaped) { $escaped=$false } elseif ($c -eq '\') { $escaped=$true } elseif ($c -eq '"') { $quoted=$false }
        } else {
            if ($c -eq '"') { $quoted=$true } elseif ($c -eq '{' -or $c -eq '[') { $depth++ } elseif ($c -eq '}' -or $c -eq ']') { $depth-- }
            if ($depth -lt 0) { Fail-Entry 'state_shape' }
        }
    }
    if ($quoted -or $depth -ne 0 -or $identities -ne 1 -or $hashes -ne 1 -or -not $state.StartsWith('{') -or -not $state.EndsWith('}')) { Fail-Entry 'state_shape' }
}
function Invoke-BoundTask {
param([string[]]$Arguments)
$state=if ($env:CRAFT_STATE_HOME) { $env:CRAFT_STATE_HOME } else { Join-Path $env:USERPROFILE '.local/share/craft-tasks/effectcraft' }
$action='';$task='';$expect=''
foreach ($item in $Arguments) {
    if ($expect) {
        switch ($expect) { state {$state=$item};task {if ($task) {Fail-Entry 'duplicate_task'};$task=$item};runtime {} }
        $expect='';continue
    }
    if (-not $action) {
        if ($item -eq '--state-root') {$expect='state'} elseif ($item.StartsWith('--state-root=')) {$state=$item.Substring(13)}
        elseif ($item -eq '--runtime-home') {$expect='runtime'} elseif ($item.StartsWith('--runtime-home=')) {}
        elseif ($item -in @('resume','reconcile','review','revise','inspect','cancel')) {$action=$item} else {return}
    } else {
        if ($item -eq '--task') {$expect='task'} elseif ($item.StartsWith('--task=')) {if ($task) {Fail-Entry 'duplicate_task'};$task=$item.Substring(7)}
    }
}
if (-not $action) {return}
if ($expect -or $task -cnotmatch '^[a-zA-Z0-9][a-zA-Z0-9_-]{0,95}$') {Fail-Entry 'task_id'}
if ($state.StartsWith('~/') -or $state.StartsWith('~\')) {$state=Join-Path $env:USERPROFILE $state.Substring(2)}
$state=[IO.Path]::GetFullPath($state);$taskRoot=Join-Path (Join-Path $state 'tasks') $task;$execution=Join-Path $taskRoot 'execution'
foreach ($path in @($state,(Join-Path $state 'tasks'),$taskRoot,$execution)) {
    try { $item=Get-Item -LiteralPath $path -ErrorAction Stop }
    catch { Fail-Entry 'file_unavailable' }
    if (-not $item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {Fail-Entry 'symlink'}
}
$identity=(Read-EntryText (Join-Path $execution 'identity.json') 16777216).TrimEnd("`n")
$rawState=(Read-EntryText (Join-Path $taskRoot 'state.json') 16777216).TrimEnd("`n")
Assert-EntryIdentity $rawState $identity (Hash-EntryText $identity)
$descriptor=Join-Path $execution 'entry.tsv';$text=Read-EntryText $descriptor 16384
$descriptorSha=(Get-FileHash -LiteralPath $descriptor -Algorithm SHA256).Hash.ToLowerInvariant()
if ([regex]::Matches($identity,('"entrySha256":"'+$descriptorSha+'"')).Count -ne 1) {Fail-Entry 'descriptor_mismatch'}
$rows=$text.Split("`n");$keys=@('schema','mode','executable','executableSha256','root','platform','version','manifest','manifestSha256','archiveSha256','minimumSystem');$values=@{}
if ($rows.Count -ne 12 -or $rows[11] -ne '') {Fail-Entry 'descriptor_shape'}
for ($i=0;$i -lt 11;$i++) {
    $parts=$rows[$i].Split("`t")
    if ($parts.Count -ne 2 -or -not [String]::Equals($parts[0],$keys[$i],[StringComparison]::Ordinal)) {Fail-Entry 'descriptor_shape'}
    $values[$keys[$i]]=$parts[1]
}
if ($values.schema -cne 'effectcraft-task-entry/v1' -or $env:OS -ne 'Windows_NT') {Fail-Entry 'platform'}
$arch=[System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString().ToLowerInvariant();$arch=@{x64='x86_64';x86='x86';arm64='arm64'}[$arch]
if ($values.platform -cne "windows-$arch") {Fail-Entry 'platform'}
$python=$values.executable;$binary=Get-Item -LiteralPath $python
if (-not [IO.Path]::IsPathRooted($python) -or $binary.PSIsContainer -or ($binary.Attributes -band [IO.FileAttributes]::ReparsePoint) -or (Get-FileHash -LiteralPath $python -Algorithm SHA256).Hash.ToLowerInvariant() -cne $values.executableSha256) {Fail-Entry 'python_changed'}
if ($values.mode -ceq 'locked') {
    $root=$values.root;$directory=Get-Item -LiteralPath $root
    if (-not [IO.Path]::IsPathRooted($root) -or -not $directory.PSIsContainer -or ($directory.Attributes -band [IO.FileAttributes]::ReparsePoint) -or -not $python.StartsWith($root+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) {Fail-Entry 'python_root'}
    if ($values.manifest -cnotmatch '^python-integrity/[a-z0-9_-]+\.tsv$') {Fail-Entry 'manifest_path'}
    $manifest=Join-Path (Join-Path $execution 'skill/scripts') $values.manifest
    [void](Read-EntryText $manifest 16777216)
    if ((Get-FileHash -LiteralPath $manifest -Algorithm SHA256).Hash.ToLowerInvariant() -cne $values.manifestSha256) {Fail-Entry 'manifest_changed'}
    if ([Environment]::OSVersion.Version -lt [version]$values.minimumSystem) {Fail-Entry 'minimum_system'}
    Assert-PythonReceipt $root $values.version $values.platform $values.archiveSha256
    $items=@(Get-ChildItem -LiteralPath $root -Recurse -Force)
    if (@($items|Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}).Count) {Fail-Entry 'python_symlink'}
    $files=@($items|Where-Object {-not $_.PSIsContainer -and $_.FullName -ne (Join-Path $root 'installation.json')});$lines=[IO.File]::ReadAllLines($manifest)
    if ($files.Count -ne $lines.Count) {Fail-Entry 'python_inventory'}
    foreach ($line in $lines) {
        $parts=$line.Split("`t")
        if ($parts.Count -ne 3 -or $parts[0] -cne 'f' -or $parts[2] -match '(^/|\.\.|:|\\)') {Fail-Entry 'python_manifest'}
        if ((Get-FileHash -LiteralPath (Join-Path $root $parts[2]) -Algorithm SHA256).Hash.ToLowerInvariant() -cne $parts[1]) {Fail-Entry 'python_changed'}
    }
} elseif ($values.mode -cne 'external' -or $values.root -cne '-' -or $values.manifest -cne '-') {Fail-Entry 'mode'}
& $python -I -B (Join-Path $PSScriptRoot 'task_entry.py') @Arguments
exit $LASTEXITCODE

}
