param(
    [Parameter(Mandatory=$true)]
    [string]$docxPath,
    [string]$pdfPath = ""
)

if (-not (Test-Path $docxPath)) {
    Write-Error "Khong tim thay file docx: $docxPath"
    exit 1
}

$docxFull = (Get-Item $docxPath).FullName
if ([string]::IsNullOrWhiteSpace($pdfPath)) {
    $pdfFull = [System.IO.Path]::ChangeExtension($docxFull, ".pdf")
} else {
    $pdfFull = (Get-Item -Path (Split-Path $pdfPath -Parent) -ErrorAction SilentlyContinue).FullName
    $pdfFull = Join-Path $pdfFull (Split-Path $pdfPath -Leaf)
}

Write-Host "Dang chuyen doi sang PDF: $docxFull -> $pdfFull"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $doc = $word.Documents.Open($docxFull)
    # wdFormatPDF = 17
    $doc.ExportAsFixedFormat($pdfFull, 17)
    $doc.Close($false)
    Write-Host "Xuat PDF thanh cong: $pdfFull"
} catch {
    Write-Error "Loi khi xuat PDF: $_"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
