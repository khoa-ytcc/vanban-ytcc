param(
    [Parameter(Mandatory=$true)]
    [string]$InputDocx,

    [Parameter(Mandatory=$true)]
    [string]$OutputPdf
)

# Đảm bảo môi trường hiển thị tiếng Việt trên console
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
} catch {}

# Chuyển đổi đường dẫn sang dạng tuyệt đối chuẩn xác
try {
    if (-not (Test-Path -LiteralPath $InputDocx)) {
        Write-Error "Lỗi: Không tìm thấy file đầu vào tại: '$InputDocx'"
        exit 1
    }
    $fullInputDocx = (Resolve-Path -LiteralPath $InputDocx).Path
    $fullOutputPdf = [System.IO.Path]::GetFullPath($OutputPdf)

    # Đảm bảo thư mục đầu ra tồn tại
    $outputDir = [System.IO.Path]::GetDirectoryName($fullOutputPdf)
    if (-not (Test-Path -LiteralPath $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
    }
} catch {
    Write-Error "Lỗi chuẩn hóa đường dẫn: $($_.Exception.Message)"
    exit 1
}

$word = $null
$doc = $null

try {
    # Khởi tạo đối tượng Word COM ở chế độ chạy ngầm
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0 # wdAlertsNone

    # Mở tài liệu ở chế độ ReadOnly
    # Open(FileName, ConfirmConversions, ReadOnly, ...)
    $doc = $word.Documents.Open($fullInputDocx, $false, $true)

    if ($null -eq $doc) {
        throw "Không thể mở tài liệu Word: $fullInputDocx"
    }

    # Xuất định dạng PDF (wdExportFormatPDF = 17)
    # ExportAsFixedFormat(OutputFileName, ExportFormat, OpenAfterExport, OptimizeFor, Range, From, To, Item, IncludeDocProps, KeepIRM, CreateBookmarks, DocStructureTags, BitmapMissingFonts, UseISO19005_1)
    $doc.ExportAsFixedFormat($fullOutputPdf, 17)

    Write-Host "Xuất PDF thành công: $fullOutputPdf"
    exit 0
} catch {
    Write-Error "Lỗi trong quá trình xuất PDF qua Word COM: $($_.Exception.Message)"
    exit 1
} finally {
    # Dọn dẹp sạch tiến trình và giải phóng tài nguyên COM
    if ($null -ne $doc) {
        try {
            $doc.Close(0) # 0 = wdDoNotSaveChanges
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($doc) | Out-Null
        } catch {}
    }
    if ($null -ne $word) {
        try {
            $word.Quit()
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
        } catch {}
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
