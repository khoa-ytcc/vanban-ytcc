param(
    [Parameter(Mandatory=$false)]
    [string]$InputDocx,

    [Parameter(Mandatory=$false)]
    [string]$OutputPdf,

    [Parameter(Mandatory=$false)]
    [string]$BatchJson
)

# Đảm bảo môi trường hiển thị tiếng Việt trên console
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
} catch {}

if ([string]::IsNullOrWhiteSpace($BatchJson) -and ([string]::IsNullOrWhiteSpace($InputDocx) -or [string]::IsNullOrWhiteSpace($OutputPdf))) {
    Write-Error "Lỗi tham số: Phải truyền hoặc (-InputDocx và -OutputPdf) hoặc (-BatchJson)."
    exit 1
}

$word = $null
$hasError = $false

try {
    # Khởi tạo đối tượng Word COM duy nhất cho toàn bộ phiên làm việc
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0 # wdAlertsNone

    if (-not [string]::IsNullOrWhiteSpace($BatchJson)) {
        if (-not (Test-Path -LiteralPath $BatchJson)) {
            Write-Error "Lỗi: Không tìm thấy file BatchJson tại: '$BatchJson'"
            exit 1
        }
        $jsonContent = Get-Content -LiteralPath $BatchJson -Raw -Encoding UTF8
        $tasks = ConvertFrom-Json $jsonContent
        $count = $tasks.Count
        
        Write-Host "Bắt đầu xuất batch PDF qua Word COM ($count tài liệu)..."
        $successCount = 0
        
        foreach ($task in $tasks) {
            $inPath = $task.docx
            $outPath = $task.pdf
            $doc = $null
            
            try {
                if (-not (Test-Path -LiteralPath $inPath)) {
                    Write-Error "Không tìm thấy file Word: $inPath"
                    $hasError = $true
                    continue
                }
                $fullInPath = (Resolve-Path -LiteralPath $inPath).Path
                $fullOutPath = [System.IO.Path]::GetFullPath($outPath)
                $outDir = [System.IO.Path]::GetDirectoryName($fullOutPath)
                if (-not (Test-Path -LiteralPath $outDir)) {
                    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
                }

                $doc = $word.Documents.Open($fullInPath, $false, $true)
                if ($null -eq $doc) {
                    throw "Không thể mở tài liệu: $fullInPath"
                }

                $doc.ExportAsFixedFormat($fullOutPath, 17) # 17 = wdExportFormatPDF
                Write-Host "  [OK] Đã xuất PDF: $fullOutPath"
                $successCount++
            } catch {
                Write-Error "  [FAIL] Lỗi xuất PDF cho '$inPath': $($_.Exception.Message)"
                $hasError = $true
            } finally {
                if ($null -ne $doc) {
                    try {
                        $doc.Close(0)
                        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($doc) | Out-Null
                    } catch {}
                    $doc = $null
                }
            }
        }
        Write-Host "Hoàn thành batch export: $successCount/$count tài liệu thành công."
    } else {
        # Chế độ xuất đơn lẻ 1 file
        $doc = $null
        try {
            if (-not (Test-Path -LiteralPath $InputDocx)) {
                Write-Error "Lỗi: Không tìm thấy file đầu vào tại: '$InputDocx'"
                exit 1
            }
            $fullInputDocx = (Resolve-Path -LiteralPath $InputDocx).Path
            $fullOutputPdf = [System.IO.Path]::GetFullPath($OutputPdf)
            $outputDir = [System.IO.Path]::GetDirectoryName($fullOutputPdf)
            if (-not (Test-Path -LiteralPath $outputDir)) {
                New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
            }

            $doc = $word.Documents.Open($fullInputDocx, $false, $true)
            if ($null -eq $doc) {
                throw "Không thể mở tài liệu Word: $fullInputDocx"
            }

            $doc.ExportAsFixedFormat($fullOutputPdf, 17)
            Write-Host "Xuất PDF thành công: $fullOutputPdf"
        } catch {
            Write-Error "Lỗi trong quá trình xuất PDF qua Word COM: $($_.Exception.Message)"
            $hasError = $true
        } finally {
            if ($null -ne $doc) {
                try {
                    $doc.Close(0)
                    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($doc) | Out-Null
                } catch {}
                $doc = $null
            }
        }
    }
} catch {
    Write-Error "Lỗi khởi tạo Word COM: $($_.Exception.Message)"
    $hasError = $true
} finally {
    if ($null -ne $word) {
        try {
            $word.Quit()
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
        } catch {}
        $word = $null
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}

if ($hasError) {
    exit 1
} else {
    exit 0
}
