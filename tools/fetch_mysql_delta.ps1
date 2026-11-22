param(
    [string]$outputJson = "$PSScriptRoot\..\knowledge_base\metadata_index\mysql_delta.json",
    [int]$maxSoDi = 0
)

try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
} catch {}

Write-Host "=== KIỂM TRA ĐỒNG BỘ TĂNG DẦN TỪ MYSQL (FETCH DELTA) ==="

# Load environment configuration from .env.local
$envFile = Join-Path (Split-Path $PSScriptRoot -Parent) ".env.local"
if (-not (Test-Path $envFile)) {
    $envFile = Join-Path (Get-Location) ".env.local"
}

if (-not (Test-Path $envFile)) {
    Write-Host "Thông báo: Không tìm thấy file .env.local, bỏ qua đồng bộ từ MySQL."
    exit 0
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
    Write-Host "Thông báo: Thiếu cấu hình kết nối trong .env.local, bỏ qua đồng bộ MySQL."
    exit 0
}

$dllPath = Join-Path $PSScriptRoot "MySql.Data.dll"
if (-not (Test-Path $dllPath)) {
    Write-Error "Không tìm thấy thư viện MySql.Data.dll tại: $dllPath"
    exit 1
}

try {
    [System.Reflection.Assembly]::Load([System.IO.File]::ReadAllBytes($dllPath)) | Out-Null
    $connStr = "server=$server; port=$port; userid=$user; password=$pass; database=$db; pooling=false; Character Set=utf8; convert zero datetime=True"
    $conn = New-Object MySql.Data.MySqlClient.MySqlConnection($connStr)
    $conn.Open()

    $cmd = $conn.CreateCommand()
    $cmd.CommandText = "SELECT so_di, nam, ngay_vanban, tenloai_trichyeu, nguoi_ky, noi_nhan, url FROM cv_di_qlvb WHERE faculty='YTCC' AND so_di > @max_so ORDER BY so_di ASC LIMIT 100"
    $p = $cmd.Parameters.AddWithValue("@max_so", $maxSoDi)

    $reader = $cmd.ExecuteReader()
    $deltaItems = @()
    while ($reader.Read()) {
        $deltaItems += [PSCustomObject]@{
            so_di = $reader["so_di"]
            nam = $reader["nam"]
            ngay_vanban = $reader["ngay_vanban"].ToString()
            tenloai_trichyeu = $reader["tenloai_trichyeu"].ToString()
            nguoi_ky = $reader["nguoi_ky"].ToString()
            noi_nhan = $reader["noi_nhan"].ToString()
            url = $reader["url"].ToString()
        }
    }
    $reader.Close()
    $conn.Close()

    Write-Host "Tìm thấy $($deltaItems.Count) bản ghi mới từ MySQL."
    if ($deltaItems.Count -gt 0) {
        $deltaItems | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath $outputJson -Encoding UTF8
        Write-Host "Đã lưu bản ghi delta vào: $outputJson"
    }
} catch {
    Write-Warning "Không thể kết nối hoặc truy vấn MySQL: $($_.Exception.Message)"
}
exit 0
