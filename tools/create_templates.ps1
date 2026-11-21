param(
    [string]$outputDir = "D:\TH\vanban-ytcc\knowledge_base\templates"
)

if (-not (Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir -Force | Out-Null }

Write-Host "Starting Word COM to build standardized 1-page templates..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

function Set-PageSetup($doc) {
    # Chuan kho giay A4: Top 20mm, Bottom 15mm, Left 25mm, Right 15mm
    $doc.PageSetup.TopMargin = 56.7    # 2.0 cm
    $doc.PageSetup.BottomMargin = 42.5 # 1.5 cm
    $doc.PageSetup.LeftMargin = 70.8   # 2.5 cm
    $doc.PageSetup.RightMargin = 42.5  # 1.5 cm
}

function Build-Document($type, $fileName, $soKyHieu, $isCV, $trichYeuCV, $title, $subTitle, $kinhGui, $noiDung, $noiNhan, $thamQuyen, $nguoiKy) {
    Write-Host "Creating $fileName..."
    $doc = $word.Documents.Add()
    Set-PageSetup $doc

    # Header Table: Col 1 = 210 pt, Col 2 = 272 pt (Tong = 482 pt)
    $table = $doc.Tables.Add($doc.Range(0, 0), 1, 2)
    $table.Borders.Enable = 0
    $table.Columns.Item(1).Width = 210
    $table.Columns.Item(2).Width = 272

    # Cell 1 (Left): Co quan ban hanh
    $c1 = $table.Cell(1, 1)
    if ($isCV) {
        $c1.Range.Text = "ĐẠI HỌC Y DƯỢC`r`nTHÀNH PHỐ HỒ CHÍ MINH`r`nKHOA Y TẾ CÔNG CỘNG`r`nSố: $soKyHieu`r`n$trichYeuCV"
    } else {
        $c1.Range.Text = "ĐẠI HỌC Y DƯỢC`r`nTHÀNH PHỐ HỒ CHÍ MINH`r`nKHOA Y TẾ CÔNG CỘNG`r`nSố: $soKyHieu"
    }
    $c1.Range.Font.Name = "Times New Roman"
    $c1.Range.ParagraphFormat.Alignment = 1 # Center
    $c1.Range.ParagraphFormat.LineSpacingRule = 0 # Single
    $c1.Range.ParagraphFormat.SpaceBefore = 0
    $c1.Range.ParagraphFormat.SpaceAfter = 0

    $c1.Range.Paragraphs.Item(1).Range.Font.Size = 10.5
    $c1.Range.Paragraphs.Item(1).Range.Font.Bold = 0
    $c1.Range.Paragraphs.Item(2).Range.Font.Size = 10.5
    $c1.Range.Paragraphs.Item(2).Range.Font.Bold = 0
    $c1.Range.Paragraphs.Item(3).Range.Font.Size = 11
    $c1.Range.Paragraphs.Item(3).Range.Font.Bold = 1
    $c1.Range.Paragraphs.Item(4).Range.Font.Size = 10.5
    $c1.Range.Paragraphs.Item(4).Range.Font.Bold = 0
    if ($isCV) {
        $c1.Range.Paragraphs.Item(5).Range.Font.Size = 10.5
        $c1.Range.Paragraphs.Item(5).Range.Font.Italic = 1
    }

    # Cell 2 (Right): Quoc hieu & Tieu ngu
    $c2 = $table.Cell(1, 2)
    $c2.Range.Text = "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM`r`nĐộc lập – Tự do – Hạnh phúc`r`nThành phố Hồ Chí Minh, ngày {{NGAY}} tháng {{THANG}} năm {{NAM}}"
    $c2.Range.Font.Name = "Times New Roman"
    $c2.Range.ParagraphFormat.Alignment = 1 # Center
    $c2.Range.ParagraphFormat.LineSpacingRule = 0 # Single
    $c2.Range.ParagraphFormat.SpaceBefore = 0
    $c2.Range.ParagraphFormat.SpaceAfter = 0

    $c2.Range.Paragraphs.Item(1).Range.Font.Size = 11
    $c2.Range.Paragraphs.Item(1).Range.Font.Bold = 1
    $c2.Range.Paragraphs.Item(2).Range.Font.Size = 11.5
    $c2.Range.Paragraphs.Item(2).Range.Font.Bold = 1
    $c2.Range.Paragraphs.Item(3).Range.Font.Size = 11
    $c2.Range.Paragraphs.Item(3).Range.Font.Italic = 1

    # End of header
    $r = $doc.Range($doc.Content.End - 1)
    $r.InsertParagraphAfter()

    # Title
    if ($title -ne "") {
        $pTitle = $doc.Paragraphs.Add()
        $pTitle.Range.Font.Name = "Times New Roman"
        $pTitle.Range.Font.Size = 13
        $pTitle.Range.Font.Bold = 1
        $pTitle.Range.ParagraphFormat.Alignment = 1
        $pTitle.Range.ParagraphFormat.SpaceBefore = 6
        $pTitle.Range.ParagraphFormat.SpaceAfter = 2
        $pTitle.Range.Text = "$title`r`n"

        if ($subTitle -ne "") {
            $pSub = $doc.Paragraphs.Add()
            $pSub.Range.Font.Name = "Times New Roman"
            $pSub.Range.Font.Size = 12
            $pSub.Range.Font.Bold = 1
            $pSub.Range.ParagraphFormat.Alignment = 1
            $pSub.Range.ParagraphFormat.SpaceBefore = 0
            $pSub.Range.ParagraphFormat.SpaceAfter = 6
            $pSub.Range.Text = "$subTitle`r`n"
        }
    }

    # Kính gửi
    if ($kinhGui -ne "") {
        $pKinhGui = $doc.Paragraphs.Add()
        $pKinhGui.Range.Font.Name = "Times New Roman"
        $pKinhGui.Range.Font.Size = 12
        $pKinhGui.Range.Font.Bold = 0
        $pKinhGui.Range.ParagraphFormat.Alignment = 0 # Left
        $pKinhGui.Range.ParagraphFormat.LeftIndent = 85.05 # Thut vao giua trang 3.0 cm
        $pKinhGui.Range.ParagraphFormat.SpaceBefore = 6
        $pKinhGui.Range.ParagraphFormat.SpaceAfter = 6
        $pKinhGui.Range.Text = "Kính gửi:`r`n$kinhGui`r`n"
        $pKinhGui.Range.Paragraphs.Item(1).Range.Font.Bold = 1
    }

    # Body
    $pBody = $doc.Paragraphs.Add()
    $pBody.Range.Font.Name = "Times New Roman"
    $pBody.Range.Font.Size = 12
    $pBody.Range.Font.Bold = 0
    $pBody.Range.ParagraphFormat.Alignment = 3 # Justify
    $pBody.Range.ParagraphFormat.LeftIndent = 0
    $pBody.Range.ParagraphFormat.FirstLineIndent = 28.35 # 1.0 cm
    $pBody.Range.ParagraphFormat.LineSpacing = 13.5 # 1.1 lines
    $pBody.Range.ParagraphFormat.SpaceBefore = 0
    $pBody.Range.ParagraphFormat.SpaceAfter = 3
    $pBody.Range.Text = "$noiDung`r`n"

    # Footer Table
    $doc.Content.InsertParagraphAfter()
    $tFooter = $doc.Tables.Add($doc.Range($doc.Content.End - 1), 1, 2)
    $tFooter.Borders.Enable = 0
    $tFooter.Columns.Item(1).Width = 210
    $tFooter.Columns.Item(2).Width = 272

    $fc1 = $tFooter.Cell(1, 1)
    $fc1.Range.Text = "Nơi nhận:`r`n$noiNhan"
    $fc1.Range.Font.Name = "Times New Roman"
    $fc1.Range.ParagraphFormat.Alignment = 0
    $fc1.Range.ParagraphFormat.LineSpacingRule = 0
    $fc1.Range.ParagraphFormat.SpaceBefore = 0
    $fc1.Range.ParagraphFormat.SpaceAfter = 0
    $fc1.Range.Paragraphs.Item(1).Range.Font.Size = 10
    $fc1.Range.Paragraphs.Item(1).Range.Font.Bold = 1
    $fc1.Range.Paragraphs.Item(1).Range.Font.Italic = 1
    for ($i = 2; $i -le $fc1.Range.Paragraphs.Count; $i++) {
        $fc1.Range.Paragraphs.Item($i).Range.Font.Size = 9.5
        $fc1.Range.Paragraphs.Item($i).Range.Font.Bold = 0
        $fc1.Range.Paragraphs.Item($i).Range.Font.Italic = 0
    }

    $fc2 = $tFooter.Cell(1, 2)
    $fc2.Range.Text = "$thamQuyen`r`n`r`n`r`n`r`n$nguoiKy"
    $fc2.Range.Font.Name = "Times New Roman"
    $fc2.Range.ParagraphFormat.Alignment = 1 # Center
    $fc2.Range.ParagraphFormat.LineSpacingRule = 0
    $fc2.Range.ParagraphFormat.SpaceBefore = 0
    $fc2.Range.ParagraphFormat.SpaceAfter = 0
    $fc2.Range.Paragraphs.Item(1).Range.Font.Size = 11.5
    $fc2.Range.Paragraphs.Item(1).Range.Font.Bold = 1
    $fc2.Range.Paragraphs.Item($fc2.Range.Paragraphs.Count).Range.Font.Size = 11.5
    $fc2.Range.Paragraphs.Item($fc2.Range.Paragraphs.Count).Range.Font.Bold = 1

    $savePath = Join-Path $outputDir $fileName
    $doc.SaveAs2("$savePath")
    $doc.Close()
    Write-Host "Saved: $savePath"
}

try {
    # 1. Mau To Trinh
    Build-Document -type "To_trinh" -fileName "Mau_To_trinh.docx" `
        -soKyHieu "{{SO_DI}}/TTr-YTCC" -isCV $false -trichYeuCV "" `
        -title "TỜ TRÌNH" -subTitle "Về việc {{TRICH_YEU_NOI_DUNG}}" `
        -kinhGui "- Ban Giám hiệu Đại học Y Dược TP.HCM;`r`n- Phòng {{PHONG_CHUC_NANG}}." `
        -noiDung "I. SỰ CẦN THIẾT`r`n{{SU_CAN_THIET}}`r`n`r`nII. NỘI DUNG ĐỀ XUẤT`r`n{{NOI_DUNG_DE_XUAT}}`r`n`r`nIII. DỰ TRÙ KINH PHÍ`r`n{{DU_TRU_KINH_PHI}}`r`n`r`nIV. KIẾN NGHỊ`r`nKhoa Y tế công cộng kính đề nghị Ban Giám hiệu xem xét, phê duyệt đề xuất nêu trên." `
        -noiNhan "- Như trên;`r`n- Phòng {{PHONG_CHUC_NANG}};`r`n- BCN Khoa YTCC;`r`n- Lưu: VT, HCTC_VTTH." `
        -thamQuyen "TRƯỞNG KHOA" -nguoiKy "PGS. TS. Nguyễn Duy Phong"

    # 2. Mau Cong Van
    Build-Document -type "Cong_van" -fileName "Mau_Cong_van.docx" `
        -soKyHieu "{{SO_DI}}/YTCC-VP" -isCV $true -trichYeuCV "{{TRICH_YEU}}" `
        -title "" -subTitle "" `
        -kinhGui "{{KINH_GUI}}"`
        -noiDung "{{NOI_DUNG_CONG_VAN}}`r`n`r`nTrân trọng kính chào./." `
        -noiNhan "- Như trên;`r`n- BCN Khoa YTCC;`r`n- Lưu: VT, HCTC_VTTH." `
        -thamQuyen "TRƯỞNG KHOA" -nguoiKy "PGS. TS. Nguyễn Duy Phong"

    # 3. Mau Giay Gioi Thieu
    Build-Document -type "Giay_gioi_thieu" -fileName "Mau_Giay_gioi_thieu.docx" `
        -soKyHieu "{{SO_DI}}/GGT-YTCC" -isCV $false -trichYeuCV "" `
        -title "GIẤY GIỚI THIỆU" -subTitle "KHOA Y TẾ CÔNG CỘNG TRÂN TRỌNG GIỚI THIỆU:" `
        -kinhGui "- Ban Giám đốc {{CO_SO_DEN}}." `
        -noiDung "Ông/Bà: {{HO_TEN}}`r`nChức danh / Đơn vị / Lớp: {{CHUC_VU}}`r`nĐược cử đến liên hệ với Quý cơ quan để: {{MUC_DICH_CONG_TAC}}`r`nThời gian làm việc từ ngày {{TU_NGAY}} đến hết ngày {{DEN_NGAY}}`r`n`r`nKính mong Quý cơ quan tạo điều kiện thuận lợi để viên chức / học viên hoàn thành nhiệm vụ.`r`n`r`nTrân trọng cảm ơn./." `
        -noiNhan "- Như trên;`r`n- Học viên/Cán bộ (để t/h);`r`n- Lưu: VT, HCTC_VTTH." `
        -thamQuyen "TRƯỞNG KHOA" -nguoiKy "PGS. TS. Nguyễn Duy Phong"

    # 4. Mau Ke Hoach
    Build-Document -type "Ke_hoach" -fileName "Mau_Ke_hoach.docx" `
        -soKyHieu "{{SO_DI}}/KH-YTCC" -isCV $false -trichYeuCV "" `
        -title "KẾ HOẠCH" -subTitle "Về việc {{TRICH_YEU_NOI_DUNG}}" `
        -kinhGui "" `
        -noiDung "I. MỤC ĐÍCH - YÊU CẦU`r`n{{MUC_DICH_YEU_CAU}}`r`n`r`nII. THỜI GIAN VÀ ĐỊA ĐIỂM`r`n{{THOI_GIAN_DIA_DIEM}}`r`n`r`nIII. NỘI DUNG CHƯƠNG TRÌNH`r`n{{NOI_DUNG_CHUONG_TRINH}}`r`n`r`nIV. PHÂN CÔNG THỰC HIỆN`r`n{{PHAN_CONG}}" `
        -noiNhan "- BCN Khoa YTCC;`r`n- Các Bộ môn liên quan;`r`n- Lưu: VT, HCTC_VTTH." `
        -thamQuyen "TRƯỞNG KHOA" -nguoiKy "PGS. TS. Nguyễn Duy Phong"

    # 5. Mau Bao Cao
    Build-Document -type "Bao_cao" -fileName "Mau_Bao_cao.docx" `
        -soKyHieu "{{SO_DI}}/BC-YTCC" -isCV $false -trichYeuCV "" `
        -title "BÁO CÁO" -subTitle "{{TRICH_YEU_NOI_DUNG}}" `
        -kinhGui "- Ban Giám hiệu Đại học Y Dược TP.HCM." `
        -noiDung "I. TÌNH HÌNH THỰC HIỆN`r`n{{TINH_HINH}}`r`n`r`nII. KẾT QUẢ ĐẠT ĐƯỢC`r`n{{KET_QUA}}`r`n`r`nIII. KIẾN NGHỊ VÀ ĐỀ XUẤT`r`n{{KIEN_NGHI}}" `
        -noiNhan "- Như trên;`r`n- BCN Khoa YTCC;`r`n- Lưu: VT, HCTC_VTTH." `
        -thamQuyen "TRƯỞNG KHOA" -nguoiKy "PGS. TS. Nguyễn Duy Phong"

    Write-Host "All 1-page templates generated successfully!"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
