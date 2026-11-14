param(
    [string]$dir = "D:\TH\vanban-ytcc\knowledge_base\sample_pdfs"
)

$files = Get-ChildItem -Path $dir -Filter "*.pdf"
$total = $files.Count
Write-Host "Dang phan tich $total file PDF trong kho du lieu mau..."

$results = @()
foreach ($f in $files) {
    $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
    $text = [System.Text.Encoding]::ASCII.GetString($bytes)
    $pages = 1
    $m = [regex]::Match($text, '/Count\s+(\d+)')
    if ($m.Success) {
        $pages = [int]$m.Groups[1].Value
    }
    
    # Phan loai van ban theo ten file
    $name = $f.Name
    $docType = "Khac"
    if ($name -match "(Công văn|CVDi)") { $docType = "Cong_van" }
    if ($name -match "Tờ trình") { $docType = "To_trinh" }
    if ($name -match "(Kế hoạch|KH)") { $docType = "Ke_hoach" }
    if ($name -match "(Báo cáo|BC)") { $docType = "Bao_cao" }
    if ($name -match "(Giấy giới thiệu|GGT)") { $docType = "Giay_gioi_thieu" }
    if ($name -match "(Quy định|Quyết định|QD)") { $docType = "Quy_dinh_Quyet_dinh" }
    if ($name -match "(Danh sách|DS)") { $docType = "Danh_sach" }
    if ($name -match "(Giấy mời|GM)") { $docType = "Giay_moi" }
    if ($name -match "(Thông báo|TB)") { $docType = "Thong_bao" }

    $results += [PSCustomObject]@{
        Name = $name
        Type = $docType
        Pages = $pages
        SizeKB = [Math]::Round($f.Length / 1KB, 1)
    }
}

Write-Host "`n=== THONG KE SO TRANG TONG QUAT ==="
$pageGroups = $results | Group-Object Pages | Sort-Object { [int]$_.Name }
foreach ($pg in $pageGroups) {
    $pct = [Math]::Round(($pg.Count / $total) * 100, 1)
    Write-Host ("{0,2} trang: {1,4} files ({2,5}%)" -f $pg.Name, $pg.Count, $pct)
}

Write-Host "`n=== THONG KE THEO LOAI VAN BAN ==="
$typeGroups = $results | Group-Object Type | Sort-Object Count -Descending
foreach ($tg in $typeGroups) {
    $typeTotal = $tg.Count
    $avgPages = [Math]::Round(($tg.Group | Measure-Object -Property Pages -Average).Average, 1)
    $onePageCount = ($tg.Group | Where-Object { $_.Pages -eq 1 }).Count
    $onePagePct = [Math]::Round(($onePageCount / $typeTotal) * 100, 1)
    $multiPageCount = $typeTotal - $onePageCount
    
    Write-Host ("Loai: {0,-20} | Tong: {1,4} | TB: {2,3} trang | 1 trang: {3,4} ({4,5}%) | Nhieu trang: {5,4}" -f `
        $tg.Name, $typeTotal, $avgPages, $onePageCount, $onePagePct, $multiPageCount)
}

# Xuat ket qua ra file JSON de lam gia tri handoff
$statsSummary = [PSCustomObject]@{
    TotalFiles = $total
    PageDistribution = $pageGroups | Select-Object @{N="Pages";E={[int]$_.Name}}, @{N="Count";E={$_.Count}}, @{N="Pct";E={[Math]::Round(($_.Count / $total) * 100, 1)}}
    TypeDistribution = $typeGroups | Select-Object @{N="Type";E={$_.Name}}, @{N="Count";E={$_.Count}}, @{N="AvgPages";E={[Math]::Round(($_.Group | Measure-Object -Property Pages -Average).Average, 1)}}, @{N="OnePageCount";E={($_.Group | Where-Object { $_.Pages -eq 1 }).Count}}
}

$outJson = "D:\TH\vanban-ytcc\knowledge_base\metadata_index\corpus_page_statistics.json"
$statsSummary | ConvertTo-Json -Depth 5 | Set-Content -Path $outJson -Encoding UTF8
Write-Host "`nDa luu thong ke chi tiet vao: $outJson"
