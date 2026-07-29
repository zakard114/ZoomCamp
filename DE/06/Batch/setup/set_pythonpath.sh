# pyspark.md에서 가져온 PYTHONPATH 설정 (Git Bash에서 source set_pythonpath.sh 로 실행)
# SPARK_HOME이 있어야 함. pip으로만 pyspark 쓸 때는 불필요할 수 있음.

if [ -z "$SPARK_HOME" ]; then
  echo "SPARK_HOME이 설정되어 있지 않습니다."
  echo "pip으로 pyspark를 설치했다면 이 스크립트 없이 주피터에서 'Python (ZoomCamp-Venv)' 커널만 선택하면 됩니다."
  exit 0
fi

export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
echo "PYTHONPATH 설정 완료."
