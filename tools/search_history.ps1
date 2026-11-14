param(
    [Parameter(Mandatory=$true)]
    [string]$Keyword,
    [ValidateSet("di", "den", "all")]
    [string]$Scope = "di",
    [int]$Limit = 10
)

$metaDir = "D:\TH\vanban-ytcc\knowledge_base\metadata_index"
$kwLower = $Keyword.ToLower()

if ($Scope -in @("di", "all")) {
    $diFile = Join-Path $metaDir "cv_di_history.json"
    if (Test-Path $diFile) {
        $diList = Get-Content $diFile -Raw -Encoding UTF8 | ConvertFrom-Json
        $matches = $diList | Where-Object { $_.tenloai_trichyeu.ToLower().Contains($kwLower) -or $_.noi_nhan.ToLower().Contains($kwLower) } | Select-Object -First $Limit
        Write-Host "=== TIM THAY TRONG CONG VAN DI ($($matches.Count) ket qua) ==="
        foreach ($m in $matches) {
            Write-Host ("Nam {0} | SoDi: {1,4} | Ngay: {2} | NoiNhan: {3} | NguoiKy: {4}`r`n  -> TrichYeu: {5}`r`n" -f $m.nam, $m.so_di, $m.ngay_vanban, $m.noi_nhan, $m.nguoi_ky, $m.tenloai_trichyeu)
        }
    }
}

if ($Scope -in @("den", "all")) {
    $denFile = Join-Path $metaDir "cv_den_history.json"
    if (Test-Path $denFile) {
        $denList = Get-Content $denFile -Raw -Encoding UTF8 | ConvertFrom-Json
        $matches = $denList | Where-Object { $_.trich_yeu.ToLower().Contains($kwLower) -or $_.tac_gia.ToLower().Contains($kwLower) -or $_.so_kihieu.ToLower().Contains($kwLower) } | Select-Object -First $Limit
        Write-Host "=== TIM THAY TRONG CONG VAN DEN ($($matches.Count) ket qua) ==="
        foreach ($m in $matches) {
            Write-Host ("Nam {0} | SoDen: {1} | TacGia: {2} | SoKiHieu: {3} | NgayVB: {4}`r`n  -> TrichYeu: {5}`r`n" -f $m.nam, $m.ngay_nhan, $m.tac_gia, $m.so_kihieu, $m.ngay_vanban, $m.trich_yeu)
        }
    }
}
