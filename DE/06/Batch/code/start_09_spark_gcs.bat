@echo off
REM 09_spark_gcs_provided.ipynb 실행 - HADOOP_HOME 필수
set HADOOP_HOME=E:\IT_SPACES\AI\ZoomCamp\DE\06\tools\hadoop-3.3.5
set PATH=%PATH%;%HADOOP_HOME%\bin

cd /d E:\IT_SPACES\AI\ZoomCamp\DE\06\Batch\code
call E:\IT_SPACES\AI\ZoomCamp\DE\06\venv\Scripts\activate.bat
echo HADOOP_HOME=%HADOOP_HOME%
jupyter notebook 09_spark_gcs_provided.ipynb
