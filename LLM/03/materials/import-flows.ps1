# Import all Module 3 example flows into Kestra (run after docker compose up -d)
$base = "http://localhost:8080/api/v1/flows/import"
$cred = "admin@kestra.io:Admin1234!"
$dir = Join-Path $PSScriptRoot "flows"

Get-ChildItem $dir -Filter "*.yaml" | Sort-Object Name | ForEach-Object {
    Write-Host "Importing $($_.Name)..."
    curl.exe -s -X POST -u $cred -F "fileUpload=@$($_.FullName)" $base
    Write-Host ""
}
