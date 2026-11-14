$excelFiles = Get-ChildItem "D:\TH" -Filter "*.xlsx"
$excelPath = $excelFiles[0].FullName
$outputDir = "D:\TH\vanban-ytcc\knowledge_base\metadata_index"

Write-Host "Excel path: $excelPath"
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false

try {
    $wb = $excel.Workbooks.Open($excelPath)

    # 1. CV Di
    Write-Host "Extracting CV Di..."
    $cvDiList = @()
    foreach ($sheetName in @("CV đi 2023", "CV đi 2024", "CV đi 2025", "CV đi 2026")) {
        $ws = $null
        try { $ws = $wb.Worksheets.Item($sheetName) } catch { continue }
        $year = [regex]::Match($sheetName, "\d{4}").Value
        $rowCount = $ws.UsedRange.Rows.Count
        Write-Host "Reading $sheetName with $rowCount rows..."

        for ($r = 2; $r -le $rowCount; $r++) {
            $soDi = $ws.Cells.Item($r, 1).Text.Trim()
            $ngay = $ws.Cells.Item($r, 2).Text.Trim()
            $trichYeu = $ws.Cells.Item($r, 3).Text.Trim()
            $nguoiKy = $ws.Cells.Item($r, 4).Text.Trim()
            $noiNhan = if ($sheetName -in @("CV đi 2025", "CV đi 2026")) { $ws.Cells.Item($r, 5).Text.Trim() } else { "" }

            if ([string]::IsNullOrWhiteSpace($trichYeu) -and [string]::IsNullOrWhiteSpace($soDi)) { continue }

            $cvDiList += [PSCustomObject]@{
                nam = [int]$year
                so_di = $soDi
                ngay_vanban = $ngay
                tenloai_trichyeu = $trichYeu
                nguoi_ky = $nguoiKy
                noi_nhan = $noiNhan
            }
        }
    }
    $cvDiPath = Join-Path $outputDir "cv_di_history.json"
    $cvDiList | ConvertTo-Json -Depth 4 | Set-Content -Path $cvDiPath -Encoding UTF8
    Write-Host "Saved CV Di: $($cvDiList.Count) records to $cvDiPath"

    # 2. CV Den
    Write-Host "Extracting CV Den..."
    $cvDenList = @()
    foreach ($sheetName in @("CV đến 2025", "CV đến 2026")) {
        $ws = $null
        try { $ws = $wb.Worksheets.Item($sheetName) } catch { continue }
        $year = [regex]::Match($sheetName, "\d{4}").Value
        $rowCount = $ws.UsedRange.Rows.Count
        Write-Host "Reading $sheetName with $rowCount rows..."

        for ($r = 2; $r -le $rowCount; $r++) {
            $ngayNhan = $ws.Cells.Item($r, 2).Text.Trim()
            $tacGia = $ws.Cells.Item($r, 4).Text.Trim()
            $soKiHieu = $ws.Cells.Item($r, 5).Text.Trim()
            $ngayVb = $ws.Cells.Item($r, 6).Text.Trim()
            $trichYeu = $ws.Cells.Item($r, 7).Text.Trim()
            $donViNhan = $ws.Cells.Item($r, 8).Text.Trim()

            if ([string]::IsNullOrWhiteSpace($trichYeu) -and [string]::IsNullOrWhiteSpace($soKiHieu)) { continue }

            $cvDenList += [PSCustomObject]@{
                nam = [int]$year
                ngay_nhan = $ngayNhan
                tac_gia = $tacGia
                so_kihieu = $soKiHieu
                ngay_vanban = $ngayVb
                trich_yeu = $trichYeu
                donvi_nhan = $donViNhan
            }
        }
    }
    $cvDenPath = Join-Path $outputDir "cv_den_history.json"
    $cvDenList | ConvertTo-Json -Depth 4 | Set-Content -Path $cvDenPath -Encoding UTF8
    Write-Host "Saved CV Den: $($cvDenList.Count) records to $cvDenPath"

    # 3. Recipient Summary
    $recipients = $cvDiList | Where-Object { -not [string]::IsNullOrWhiteSpace($_.noi_nhan) } | Group-Object -Property noi_nhan | Select-Object Name, Count | Sort-Object Count -Descending
    $recPath = Join-Path $outputDir "recipient_summary.json"
    $recipients | ConvertTo-Json -Depth 3 | Set-Content -Path $recPath -Encoding UTF8
    Write-Host "Saved Recipient Summary to $recPath"

    $wb.Close($false)
} finally {
    $excel.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
}