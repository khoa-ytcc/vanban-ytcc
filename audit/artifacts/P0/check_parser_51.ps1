$auditResult = @()
foreach ($auditScript in Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot '../../../tools') -Filter '*.ps1') {
    $auditTokens=$null
    $auditErrors=$null
    [System.Management.Automation.Language.Parser]::ParseFile($auditScript.FullName,[ref]$auditTokens,[ref]$auditErrors) | Out-Null
    $auditResult += [pscustomobject]@{
        Path=$auditScript.Name
        ParserVersion=$PSVersionTable.PSVersion.ToString()
        Errors=@($auditErrors | ForEach-Object { [pscustomobject]@{Id=$_.ErrorId;Line=$_.Extent.StartLineNumber} })
    }
}
$auditResult | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'parser_powershell51.json') -Encoding utf8
$auditResult | Select-Object Path,@{n='ErrorCount';e={$_.Errors.Count}}
