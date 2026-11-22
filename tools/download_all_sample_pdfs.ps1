param(
    [string]$outputDir = "$PSScriptRoot\..\knowledge_base\sample_pdfs",
    [int]$threads = 10
)

# Load environment configuration from .env.local
$envFile = Join-Path (Split-Path $PSScriptRoot -Parent) ".env.local"
if (-not (Test-Path $envFile)) {
    $envFile = Join-Path (Get-Location) ".env.local"
}
if (-not (Test-Path $envFile)) {
    throw "Không tìm thấy file .env.local chứa cấu hình kết nối CSDL."
}

$envVars = @{}
Get-Content $envFile | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
        $parts = $line.Split("=", 2)
        $envVars[$parts[0].Trim()] = $parts[1].Trim()
    }
}

$server = $envVars["MYSQL_SERVER"]
$port = if ($envVars["MYSQL_PORT"]) { $envVars["MYSQL_PORT"] } else { "3306" }
$user = $envVars["MYSQL_USER"]
$pass = $envVars["MYSQL_PASSWORD"]
$db = $envVars["MYSQL_DATABASE"]

if (-not $server -or -not $user -or -not $pass -or -not $db) {
    throw "Thiếu thông tin kết nối CSDL trong file .env.local."
}

$dllPath = Join-Path $PSScriptRoot "MySql.Data.dll"
[System.Reflection.Assembly]::Load([System.IO.File]::ReadAllBytes($dllPath)) | Out-Null

$connStr = "server=$server; port=$port; userid=$user; password=$pass; database=$db; pooling=false; Character Set=utf8; convert zero datetime=True"
$conn = New-Object MySql.Data.MySqlClient.MySqlConnection($connStr)
$conn.Open()

$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT DISTINCT so_di, nam, ngay_vanban, tenloai_trichyeu, url FROM cv_di_qlvb WHERE faculty='YTCC' AND url LIKE '%/file/d/%' ORDER BY so_di ASC"
$reader = $cmd.ExecuteReader()

$items = @()
while ($reader.Read()) {
    $items += [PSCustomObject]@{
        SoDi = $reader["so_di"]
        Nam = $reader["nam"]
        Ngay = [DateTime]$reader["ngay_vanban"]
        TrichYeu = $reader["tenloai_trichyeu"].ToString()
        Url = $reader["url"].ToString()
    }
}
$reader.Close()
$conn.Close()

Write-Host "Total unique files to download: $($items.Count)"

if (-not (Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir -Force | Out-Null }

$pool = [RunspaceFactory]::CreateRunspacePool(1, $threads)
$pool.Open()

$scriptBlock = {
    param($item, $outDir)
    if ($item.Url -match "/file/d/([^/]+)") {
        $fileId = $matches[1]
        $downloadUrl = "https://drive.usercontent.google.com/download?id=$fileId&export=download"
        
        $safeTrichYeu = ($item.TrichYeu -replace '[\\/:*?"<>|]', '_').Trim()
        if ($safeTrichYeu.Length -gt 60) { $safeTrichYeu = $safeTrichYeu.Substring(0, 60) }
        $fileName = ("CVDi_{0}_SoDi_{1}_{2}.pdf" -f $item.Nam, $item.SoDi, $safeTrichYeu)
        $destPath = Join-Path $outDir $fileName

        if (-not (Test-Path $destPath) -or (Get-Item $destPath).Length -lt 1000) {
            try {
                $wc = New-Object System.Net.WebClient
                $wc.DownloadFile($downloadUrl, $destPath)
                return "OK: SoDi $($item.SoDi)"
            } catch {
                return "FAIL: SoDi $($item.SoDi) - $($_.Exception.Message)"
            }
        } else {
            return "EXISTS: SoDi $($item.SoDi)"
        }
    }
    return "SKIP"
}

$tasks = @()
foreach ($item in $items) {
    $ps = [PowerShell]::Create().AddScript($scriptBlock).AddArgument($item).AddArgument($outputDir)
    $ps.RunspacePool = $pool
    $tasks += [PSCustomObject]@{
        Pipe = $ps
        Async = $ps.BeginInvoke()
        SoDi = $item.SoDi
    }
}

Write-Host "Dispatched $($tasks.Count) download tasks to $threads threads..."

$done = 0
$ok = 0
$fail = 0
$exists = 0

foreach ($t in $tasks) {
    $res = $t.Pipe.EndInvoke($t.Async)
    $t.Pipe.Dispose()
    $done++
    if ($res -like "OK*") { $ok++ }
    elseif ($res -like "EXISTS*") { $exists++ }
    else { $fail++ }

    if ($done % 50 -eq 0 -or $done -eq $tasks.Count) {
        Write-Host ("Progress: {0}/{1} (New: {2}, Exists: {3}, Fail: {4})" -f $done, $tasks.Count, $ok, $exists, $fail)
    }
}

$pool.Close()
$pool.Dispose()

Write-Host "=== DOWNLOAD COMPLETED ==="
Write-Host "Total: $($tasks.Count) | Downloaded: $ok | Already existed: $exists | Failed: $fail"
