"""
Windows용 Hadoop winutils 설치 스크립트
df.write.parquet() 시 HADOOP_HOME 에러 해결용
"""
import os
import urllib.request

HADOOP_VERSION = "3.3.5"  # Spark 3.5 호환 (cdarlint에 3.3.2 없음)
BASE_URL = f"https://raw.githubusercontent.com/cdarlint/winutils/master/hadoop-{HADOOP_VERSION}/bin/"
FILES = ["hadoop.dll", "hadoop.exp", "hadoop.lib", "hadoop.pdb", "libwinutils.lib", "winutils.exe", "winutils.pdb"]

# DE/06/tools/hadoop-3.2.0 생성 (절대경로 사용)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HADOOP_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "tools", f"hadoop-{HADOOP_VERSION}"))
BIN_DIR = os.path.join(HADOOP_DIR, "bin")
os.makedirs(BIN_DIR, exist_ok=True)

print(f"다운로드 대상: {BIN_DIR}")
for f in FILES:
    url = BASE_URL + f
    dest = os.path.join(BIN_DIR, f)
    try:
        urllib.request.urlretrieve(url, dest)
        print(f"  OK: {f}")
    except Exception as e:
        print(f"  FAIL: {f} - {e}")

print(f"\n완료. HADOOP_HOME으로 설정할 경로:\n{HADOOP_DIR}")
print("\n주피터 노트북 맨 위 셀에 아래를 추가하세요 (SparkSession 생성 전):")
print(f"""
import os
os.environ['HADOOP_HOME'] = r'{HADOOP_DIR}'
os.environ['PATH'] = os.environ.get('PATH', '') + os.pathsep + r'{os.path.join(HADOOP_DIR, "bin")}'
""")
