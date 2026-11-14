$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $doc = $word.Documents.Add()

    # 1. Khổ giấy A4 & Căn lề chuẩn Nghị định 30 (Trên 2cm, Dưới 2cm, Trái 3cm, Phải 2cm)
    $doc.PageSetup.PaperSize = 7 # wdPaperA4
    $doc.PageSetup.TopMargin = 56.7     # 2.0 cm
    $doc.PageSetup.BottomMargin = 56.7  # 2.0 cm
    $doc.PageSetup.LeftMargin = 85.05   # 3.0 cm
    $doc.PageSetup.RightMargin = 56.7   # 2.0 cm

    $range = $doc.Range(0, 0)

    # 2. Bảng Tiêu ngữ (Header Table): Vùng in = 595.3 - 85.05 - 56.7 = 453.55 pt.
    # Cột 1 = 195 pt, Cột 2 = 258 pt (Tổng = 453 pt)
    $tHeader = $doc.Tables.Add($range, 1, 2)
    $tHeader.Borders.Enable = 0
    $tHeader.Columns.Item(1).Width = 195
    $tHeader.Columns.Item(2).Width = 258

    # Cột 1: Cơ quan ban hành, Số văn bản, Trích yếu
    $c1 = $tHeader.Cell(1, 1)
    $c1.Range.Text = "ĐẠI HỌC Y DƯỢC`r`nTHÀNH PHỐ HỒ CHÍ MINH`r`nKHOA Y TẾ CÔNG CỘNG`r`nSố:       /YTCC-VP`r`nV/v đồng ý để viên chức tham gia ghi hình chương trình truyền hình"
    $c1.Range.Font.Name = "Times New Roman"
    $c1.Range.ParagraphFormat.Alignment = 1 # Center
    $c1.Range.ParagraphFormat.LineSpacingRule = 0
    $c1.Range.ParagraphFormat.SpaceBefore = 0
    $c1.Range.ParagraphFormat.SpaceAfter = 0

    $c1.Range.Paragraphs.Item(1).Range.Font.Size = 10.5
    $c1.Range.Paragraphs.Item(2).Range.Font.Size = 10.5
    $c1.Range.Paragraphs.Item(3).Range.Font.Size = 11
    $c1.Range.Paragraphs.Item(3).Range.Font.Bold = 1
    $c1.Range.Paragraphs.Item(3).Range.Borders.Item(-3).LineStyle = 1 # wdBorderBottom
    $c1.Range.Paragraphs.Item(3).Range.Borders.Item(-3).LineWidth = 4
    $c1.Range.Paragraphs.Item(4).Range.Font.Size = 11
    $c1.Range.Paragraphs.Item(4).Range.ParagraphFormat.SpaceBefore = 3
    $c1.Range.Paragraphs.Item(5).Range.Font.Size = 11
    $c1.Range.Paragraphs.Item(5).Range.Font.Italic = 1
    $c1.Range.Paragraphs.Item(5).Range.ParagraphFormat.LineSpacing = 12

    # Cột 2: Quốc hiệu, Tiêu ngữ, Địa danh & Ngày tháng
    $c2 = $tHeader.Cell(1, 2)
    $c2.Range.Text = "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM`r`nĐộc lập – Tự do – Hạnh phúc`r`nThành phố Hồ Chí Minh, ngày 14 tháng 11 năm 2026"
    $c2.Range.Font.Name = "Times New Roman"
    $c2.Range.ParagraphFormat.Alignment = 1 # Center
    $c2.Range.ParagraphFormat.LineSpacingRule = 0
    $c2.Range.ParagraphFormat.SpaceBefore = 0
    $c2.Range.ParagraphFormat.SpaceAfter = 0

    $c2.Range.Paragraphs.Item(1).Range.Font.Size = 10.5
    $c2.Range.Paragraphs.Item(1).Range.Font.Bold = 1
    $c2.Range.Paragraphs.Item(2).Range.Font.Size = 11
    $c2.Range.Paragraphs.Item(2).Range.Font.Bold = 1
    $c2.Range.Paragraphs.Item(2).Range.Borders.Item(-3).LineStyle = 1 # wdBorderBottom
    $c2.Range.Paragraphs.Item(2).Range.Borders.Item(-3).LineWidth = 4
    $c2.Range.Paragraphs.Item(3).Range.Font.Size = 11
    $c2.Range.Paragraphs.Item(3).Range.Font.Italic = 1
    $c2.Range.Paragraphs.Item(3).Range.ParagraphFormat.SpaceBefore = 3

    # Di chuyển sau bảng Tiêu ngữ
    $pEnd = $doc.Paragraphs.Item($doc.Paragraphs.Count).Range
    $pEnd.Collapse(0)

    # 3. Kính gửi
    $pKinhGui = $doc.Paragraphs.Add($pEnd)
    $pKinhGui.Range.Text = "Kính gửi:`r`n- Công ty TNHH Truyền hình Kết Nối;`r`n- Ban Giám hiệu Đại học Y Dược TP. Hồ Chí Minh;`r`n- Phòng Tổ chức Cán bộ, Đại học Y Dược TP. Hồ Chí Minh."
    $pKinhGui.Range.Font.Name = "Times New Roman"
    $pKinhGui.Range.Font.Size = 11.5
    $pKinhGui.Range.ParagraphFormat.Alignment = 0
    $pKinhGui.Range.ParagraphFormat.LeftIndent = 36 # Indent kính gửi
    $pKinhGui.Range.ParagraphFormat.LineSpacing = 13.0
    $pKinhGui.Range.ParagraphFormat.SpaceBefore = 6
    $pKinhGui.Range.ParagraphFormat.SpaceAfter = 2
    $pKinhGui.Range.Paragraphs.Item(1).Range.Font.Bold = 1

    # 4. Thêm nội dung chi tiết Công văn
    $paragraphsToAdd = @(
        "Căn cứ Công văn số 1011/CV2026 ngày 10 tháng 11 năm 2026 của Công ty TNHH Truyền hình Kết Nối về việc mời viên chức tham gia ghi hình chương trình truyền hình `"Sức Khỏe 24h`" trên kênh HTV7;",
        "Căn cứ ý kiến chỉ đạo của Ban Giám hiệu Đại học Y Dược TP. Hồ Chí Minh tại Công văn đến số 5405/ĐHYD ngày 11 tháng 11 năm 2026;",
        "Sau khi xem xét kế hoạch công tác và sự thống nhất của Bộ môn Dinh dưỡng, Khoa Y tế công cộng có ý kiến như sau:",
        "1. Thống nhất đồng ý để ThS. Trương Nhật Khuê Tường – Giảng viên Bộ môn Dinh dưỡng, Khoa Y tế công cộng tham gia ghi hình 02 nội dung Talk show với chủ đề `"Dinh dưỡng và sức khỏe đường ruột`" trong chương trình `"Sức Khỏe 24h`" do Quý Công ty phối hợp phát sóng trên kênh HTV7.",
        "- Thời gian ghi hình: Ngày 18 tháng 11 năm 2026.",
        "- Địa điểm: Phim trường Đài Truyền hình TP. Hồ Chí Minh (HTV).",
        "- Thời lượng: 10 phút/01 nội dung.",
        "2. ThS. Trương Nhật Khuê Tường có trách nhiệm chủ động bố trí, sắp xếp lịch giảng dạy và công tác chuyên môn tại Bộ môn để tham gia ghi hình đúng thời gian quy định; bảo đảm tuân thủ nghiêm túc các quy định chuyên môn y tế và giữ gìn uy tín, hình ảnh của Nhà trường và Khoa.",
        "3. Đề nghị Quý Công ty phối hợp chặt chẽ với giảng viên trong việc hoàn thiện nội dung và bảo đảm các điều kiện ghi hình theo đúng cam kết.",
        "Khoa Y tế công cộng trân trọng thông báo đến Quý Đơn vị và báo cáo Ban Giám hiệu, Phòng Tổ chức Cán bộ để phối hợp thực hiện./."
    )

    foreach ($paraText in $paragraphsToAdd) {
        $p = $doc.Paragraphs.Add()
        $p.Range.Text = $paraText
        $p.Range.Font.Name = "Times New Roman"
        $p.Range.Font.Size = 11.5
        $p.Range.ParagraphFormat.Alignment = 3 # Justify
        $p.Range.ParagraphFormat.LeftIndent = 0
        $p.Range.ParagraphFormat.FirstLineIndent = 28.35 # 1 cm
        $p.Range.ParagraphFormat.LineSpacing = 13.0
        $p.Range.ParagraphFormat.SpaceBefore = 0
        $p.Range.ParagraphFormat.SpaceAfter = 2

        if ($paraText -like "Căn cứ *") {
            $p.Range.Font.Italic = 1
        }
        if ($paraText -like "- *") {
            $p.Range.ParagraphFormat.FirstLineIndent = 42.5
        }
    }

    # 5. Bảng Chữ ký & Nơi nhận (Footer Table)
    $pEnd2 = $doc.Paragraphs.Item($doc.Paragraphs.Count).Range
    $pEnd2.Collapse(0)
    $tFooter = $doc.Tables.Add($pEnd2, 1, 2)
    $tFooter.Borders.Enable = 0
    $tFooter.Columns.Item(1).Width = 200
    $tFooter.Columns.Item(2).Width = 253

    $fc1 = $tFooter.Cell(1, 1)
    $fc1.Range.Text = "Nơi nhận:`r`n- Như trên;`r`n- Bộ môn Dinh dưỡng (để biết);`r`n- ThS. Trương Nhật Khuê Tường (để t/h);`r`n- Lưu: VT, HCTC_VTTH."
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
    $fc2.Range.Text = "TRƯỞNG KHOA`r`n`r`n`r`n`r`nPGS. TS. Nguyễn Duy Phong"
    $fc2.Range.Font.Name = "Times New Roman"
    $fc2.Range.ParagraphFormat.Alignment = 1 # Center
    $fc2.Range.ParagraphFormat.LineSpacingRule = 0
    $fc2.Range.ParagraphFormat.SpaceBefore = 0
    $fc2.Range.ParagraphFormat.SpaceAfter = 0
    $fc2.Range.Paragraphs.Item(1).Range.Font.Size = 11.5
    $fc2.Range.Paragraphs.Item(1).Range.Font.Bold = 1
    $fc2.Range.Paragraphs.Item($fc2.Range.Paragraphs.Count).Range.Font.Size = 11.5
    $fc2.Range.Paragraphs.Item($fc2.Range.Paragraphs.Count).Range.Font.Bold = 1

    # Kiểm tra số trang
    $pageCount = $doc.ComputeStatistics(2)
    Write-Host "Kiem tra so trang: $pageCount trang."

    $outDir = "D:\TH\vanban-ytcc\drafts\2026-11"
    if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }

    $outDocx = Join-Path $outDir "CVDi_20261114_Dong_y_ghi_hinh_HTV7_ThS_Truong_Nhat_Khue_Tuong.docx"
    $outPdf = Join-Path $outDir "CVDi_20261114_Dong_y_ghi_hinh_HTV7_ThS_Truong_Nhat_Khue_Tuong.pdf"

    $doc.SaveAs2($outDocx) # 16 = wdFormatDocumentDefault
    $doc.ExportAsFixedFormat($outPdf, 17) # 17 = wdExportFormatPDF
    $doc.Close([ref]0)

    Write-Host "HOAN TAT: Xuat thanh cong $outDocx va $outPdf"
    Write-Host "So trang cuoi cung: $pageCount"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
