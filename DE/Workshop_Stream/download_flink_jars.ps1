# Flink 1.19.0 호환 Kafka/JDBC 커넥터 JAR 다운로드
# 실행: .\download_flink_jars.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$base = "https://repo1.maven.org/maven2"
$jars = @(
    @{
        url = "$base/org/apache/flink/flink-sql-connector-kafka/3.3.0-1.19/flink-sql-connector-kafka-3.3.0-1.19.jar"
        dir = "plugins/kafka"
    },
    @{
        url = "$base/org/apache/flink/flink-connector-jdbc/3.2.0-1.19/flink-connector-jdbc-3.2.0-1.19.jar"
        dir = "plugins/jdbc"
    },
    @{
        url = "$base/org/postgresql/postgresql/42.7.3/postgresql-42.7.3.jar"
        dir = "plugins/jdbc"
    }
)

foreach ($j in $jars) {
    $dir = $j.dir
    $fileName = Split-Path $j.url -Leaf
    $outPath = Join-Path $dir $fileName
    if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    if (Test-Path $outPath) {
        Write-Host "SKIP (exists): $fileName" -ForegroundColor Yellow
    } else {
        Write-Host "Downloading: $fileName" -ForegroundColor Cyan
        Invoke-WebRequest -Uri $j.url -OutFile $outPath -UseBasicParsing
    }
}
Write-Host "`nDone. plugins/kafka, plugins/jdbc 생성됨." -ForegroundColor Green
