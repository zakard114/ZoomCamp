@echo off
set HADOOP_HOME=E:\IT_SPACES\AI\ZoomCamp\DE\06\tools\hadoop-3.3.5
set PATH=%HADOOP_HOME%\bin;%PATH%

echo HADOOP_HOME is set to %HADOOP_HOME%
echo Starting Jupyter Notebook...

# 만약 가상환경을 쓰신다면 활성화 명령을 추가하세요
# call E:\IT_SPACES\AI\ZoomCamp\DE\06\venv\Scripts\activate

jupyter notebook