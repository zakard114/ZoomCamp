# read_parquet_safe.py
"""
winutils 없이 Parquet 읽기 (pandas 사용)
Spark의 UnsatisfiedLinkError 회피용
"""
import pandas as pd

def read_green():
    return pd.read_parquet("data/pq/green/2021/01/")

def read_yellow():
    return pd.read_parquet("data/pq/yellow/2021/01/")

if __name__ == "__main__":
    df = read_green()
    print(df.head())
