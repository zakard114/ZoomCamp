#!/bin/bash
# HADOOP_HOME을 설정한 뒤 Jupyter 실행 (winutils 인식용)
export HADOOP_HOME="/e/IT_SPACES/AI/ZoomCamp/DE/06/tools/hadoop-3.3.5"
export PATH="$PATH:$HADOOP_HOME/bin"

cd /e/IT_SPACES/AI/ZoomCamp/DE/06/Batch/code
source ../../venv/Scripts/activate
jupyter notebook
