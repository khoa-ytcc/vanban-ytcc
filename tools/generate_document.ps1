param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("To_trinh", "Cong_van", "Giay_gioi_thieu", "Ke_hoach", "Bao_cao")]
    [string]$TemplateType,
    
    [string]$SoDi = "...",
    [string]$KyHieu = "VP",
    [string]$TrichYeu = "Trích yếu nội dung văn bản",
    [string]$KinhGui = "- Ban Giám hiệu Đại học Y Dược TP.HCM;`r`n- Phòng Tổ chức Cán bộ.",
    [string]$NoiDung = "Nội dung chi tiết của văn bản...",
    [string]$NoiNhan = "- Như trên;`r`n- BCN Khoa YTCC;`r`n- Lưu: VT, HCTC_VTTH.",
    [string]$ThamQuyen = "TRƯỞNG KHOA",
    [string]$NguoiKy = "PGS. TS. Nguyễn Duy Phong",
    [string]$HoTen = "",
    [string]$ChucVu = "",
    [string]$NoiDen = "",
    [string]$MucDich = "",
    [string]$HanDung = ""
)

$today = Get-Date
$ngay = $today.Day.ToString("00")
$thang = $today.Month.ToString("00")
$nam = $today.Year.ToString()

$monthFolder = $today.ToString("yyyy-MM")
$outputDir = Join-Path "D:\TH\vanban-ytcc\drafts" $monthFolder
if (-not (Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir -Force | Out-Null }

$templateName = "Mau_$TemplateType.docx"
$templatePath = Join-Path "D:\TH\vanban-ytcc\knowledge_base\templates" $templateName

if (-not (Test-Path $templatePath)) {
    Write-Error "Khong tim thay template: $templatePath"
    exit 1
}

# Clean TrichYeu header (Khong de bi lap V/v V/v)
$cleanTrichYeu = $TrichYeu.Trim()
if ($cleanTrichYeu -match "^(V/v|Về việc)\s*") {
    $cleanTrichYeuHeader = "V/v " + ($cleanTrichYeu -replace "^(V/v|Về việc)\s*", "")
} else {
    $cleanTrichYeuHeader = "V/v " + $cleanTrichYeu
}

$safeTrichYeu = ($TrichYeu -replace '[\\/:*?"<>|]', '_').Trim()
if ($safeTrichYeu.Length -gt 40) { $safeTrichYeu = $safeTrichYeu.Substring(0, 40) }
$outFileName = ("Draft_{0}_{1}_{2}.docx" -f $TemplateType, $today.ToString("yyyyMMdd"), $safeTrichYeu)
$outPath = Join-Path $outputDir $outFileName

# Copy template to target
Copy-Item $templatePath -Destination $outPath -Force

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $doc = $word.Documents.Open($outPath)

    function Replace-Placeholder($findText, $replaceText) {
        $range = $doc.Content
        while ($range.Find.Execute($findText)) {
            $range.Text = $replaceText
            $range.Collapse(0) # 0 = wdCollapseEnd
        }
    }

    Replace-Placeholder "{{SO_DI}}" $SoDi
    Replace-Placeholder "{{KY_HIEU}}" $KyHieu
    Replace-Placeholder "{{NGAY}}" $ngay
    Replace-Placeholder "{{THANG}}" $thang
    Replace-Placeholder "{{NAM}}" $nam
    Replace-Placeholder "{{TRICH_YEU_NOI_DUNG}}" $cleanTrichYeu
    Replace-Placeholder "{{TRICH_YEU}}" $cleanTrichYeuHeader
    Replace-Placeholder "{{KINH_GUI}}" $KinhGui
    Replace-Placeholder "{{THAM_QUYEN_KY}}" $ThamQuyen
    Replace-Placeholder "{{NGUOI_KY}}" $NguoiKy

    if ($TemplateType -eq "To_trinh") {
        Replace-Placeholder "{{NOI_DUNG_TO_TRINH}}" $NoiDung
    } elseif ($TemplateType -eq "Cong_van") {
        Replace-Placeholder "{{NOI_DUNG_CONG_VAN}}" $NoiDung
    } elseif ($TemplateType -eq "Giay_gioi_thieu") {
        Replace-Placeholder "{{HO_TEN}}" $HoTen
        Replace-Placeholder "{{CHUC_VU}}" $ChucVu
        Replace-Placeholder "{{NOI_DEN}}" $NoiDen
        Replace-Placeholder "{{MUC_DICH_CONG_TAC}}" $MucDich
        Replace-Placeholder "{{TU_NGAY}}" $ngay
        Replace-Placeholder "{{DEN_NGAY}}" $HanDung
    } elseif ($TemplateType -eq "Ke_hoach") {
        Replace-Placeholder "{{NOI_DUNG_KE_HOACH}}" $NoiDung
    } elseif ($TemplateType -eq "Bao_cao") {
        Replace-Placeholder "{{NOI_DUNG_BAO_CAO}}" $NoiDung
    }

    # Kiem tra so trang: Neu > 1 trang thi tu dong toi uu gian dong & khoang cach de vua khit 1 trang
    $pages = $doc.ComputeStatistics(2) # 2 = wdStatisticPages
    if ($pages -gt 1) {
        Write-Host "Phat hien van ban tran sang $pages trang. Dang tu dong thu gon de vua tron 1 trang..."
        # Giam spacing cua cac doan noi dung
        foreach ($p in $doc.Paragraphs) {
            if ($p.Range.Tables.Count -eq 0) {
                if ($p.Range.Font.Size -ge 12) { $p.Range.Font.Size = 11.5 }
                $p.Range.ParagraphFormat.LineSpacing = 12.0 # single compact
                if ($p.Range.ParagraphFormat.SpaceAfter -gt 2) { $p.Range.ParagraphFormat.SpaceAfter = 2 }
                if ($p.Range.ParagraphFormat.SpaceBefore -gt 2) { $p.Range.ParagraphFormat.SpaceBefore = 0 }
            }
        }
        $pagesAfter = $doc.ComputeStatistics(2)
        Write-Host "Sau khi toi uu: $pagesAfter trang."
    }

    $doc.Save()
    $doc.Close()
    Write-Host "Tao ban thao Word thanh cong: $outPath (So trang: $($pagesAfter -or $pages))"
} catch {
    Write-Error "Loi khi ghi noi dung vao file Word: $_"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
