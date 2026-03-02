"""
taxi_zone_lookup.csv → zones/ Parquet 생성
pandas 사용으로 winutils 없이 실행 가능.
"""
import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "taxi_zone_lookup.csv")
OUT_DIR = os.path.join(SCRIPT_DIR, "zones")

if __name__ == "__main__":
    if not os.path.exists(CSV_PATH):
        print(f"CSV 없음: {CSV_PATH}")
        print("CloudFront에서 다운로드: https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv")
        exit(1)

    df = pd.read_csv(CSV_PATH)
    os.makedirs(OUT_DIR, exist_ok=True)
    # 단일 파일로 쓰기 (디렉터리 경로 시 Windows 권한 이슈 방지)
    df.to_parquet(os.path.join(OUT_DIR, "data.parquet"), index=False)
    print(f"zones/ Parquet 생성 완료: {OUT_DIR}")
    print(f"  레코드 수: {len(df)}")
