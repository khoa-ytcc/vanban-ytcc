$dllPath = Join-Path $PSScriptRoot "MySql.Data.dll"
[System.Reflection.Assembly]::Load([System.IO.File]::ReadAllBytes($dllPath)) | Out-Null

$connStr = "server=45.117.169.194; port=3306; userid=dvdung_user; password=D0.4nhuy; database=dvdung_dbase; pooling=false; Character Set=utf8; convert zero datetime=True"
$conn = New-Object MySql.Data.MySqlClient.MySqlConnection($connStr)
$conn.Open()

$targetDir = "D:\TH\vanban-ytcc\knowledge_base\sample_pdfs"
if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir -Force | Out-Null }

$queries = @(
    @{ Type = "To_trinh"; Sql = "SELECT DISTINCT so_di, ngay_vanban, tenloai_trichyeu, url FROM cv_di_qlvb WHERE faculty='YTCC' AND tenloai_trichyeu LIKE 'Tờ trình%' AND url LIKE '%/file/d/%' ORDER BY so_di DESC LIMIT 10" },
    @{ Type = "Cong_van"; Sql = "SELECT DISTINCT so_di, ngay_vanban, tenloai_trichyeu, url FROM cv_di_qlvb WHERE faculty='YTCC' AND tenloai_trichyeu LIKE 'Công văn%' AND url LIKE '%/file/d/%' ORDER BY so_di DESC LIMIT 10" },
    @{ Type = "Giay_gioi_thieu"; Sql = "SELECT DISTINCT so_di, ngay_vanban, tenloai_trichyeu, url FROM cv_di_qlvb WHERE faculty='YTCC' AND (tenloai_trichyeu LIKE 'Giấy giới thiệu%' OR tenloai_trichyeu LIKE 'GGT%') AND url LIKE '%/file/d/%' ORDER BY so_di DESC LIMIT 5" },
    @{ Type = "Ke_hoach"; Sql = "SELECT DISTINCT so_di, ngay_vanban, tenloai_trichyeu, url FROM cv_di_qlvb WHERE faculty='YTCC' AND (tenloai_trichyeu LIKE 'Kế hoạch%' OR tenloai_trichyeu LIKE 'KH%') AND url LIKE '%/file/d/%' ORDER BY so_di DESC LIMIT 5" },
    @{ Type = "Quyet_dinh"; Sql = "SELECT DISTINCT so_di, ngay_vanban, tenloai_trichyeu, url FROM cv_di_qlvb WHERE faculty='YTCC' AND (tenloai_trichyeu LIKE 'Quyết định%' OR tenloai_trichyeu LIKE 'QĐ%') AND url LIKE '%/file/d/%' ORDER BY so_di DESC LIMIT 4" },
    @{ Type = "Bao_cao"; Sql = "SELECT DISTINCT so_di, ngay_vanban, tenloai_trichyeu, url FROM cv_di_qlvb WHERE faculty='YTCC' AND (tenloai_trichyeu LIKE 'Báo cáo%' OR tenloai_trichyeu LIKE 'BC%') AND url LIKE '%/file/d/%' ORDER BY so_di DESC LIMIT 4" }
)

$downloadList = @()
foreach ($q in $queries) {
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = $q.Sql
    $reader = $cmd.ExecuteReader()
    while ($reader.Read()) {
        $downloadList += [PSCustomObject]@{
            Loai = $q.Type
            SoDi = $reader["so_di"]
            Ngay = [DateTime]$reader["ngay_vanban"]
            TrichYeu = $reader["tenloai_trichyeu"].ToString()
            Url = $reader["url"].ToString()
        }
    }
    $reader.Close()
}
$conn.Close()

Write-Host "Total sample files to download: $($downloadList.Count)"

$wc = New-Object System.Net.WebClient
$successCount = 0

foreach ($item in $downloadList) {
    if ($item.Url -match "/file/d/([^/]+)") {
        $fileId = $matches[1]
        $downloadUrl = "https://drive.usercontent.google.com/download?id=$fileId&export=download"
        $fileName = ("{0}_SoDi_{1}.pdf" -f $item.Loai, $item.SoDi)
        $destPath = Join-Path $targetDir $fileName

        if (-not (Test-Path $destPath)) {
            try {
                Write-Host ("Downloading SoDi {0} ({1})..." -f $item.SoDi, $item.Loai)
                $wc.DownloadFile($downloadUrl, $destPath)
                $successCount++
            } catch {
                Write-Host ("  Failed SoDi {0}: {1}" -f $item.SoDi, $_.Message)
            }
        } else {
            $successCount++
        }
    }
}

Write-Host "Downloaded successfully: $successCount / $($downloadList.Count) sample PDFs."