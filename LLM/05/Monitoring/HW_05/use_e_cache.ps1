# Point uv package cache to E: (never C:\Users\...)
$env:UV_CACHE_DIR = "E:\IT_SPACES\AI\.cache\uv"
New-Item -ItemType Directory -Force -Path $env:UV_CACHE_DIR | Out-Null
Write-Host "UV_CACHE_DIR=$env:UV_CACHE_DIR"
