@echo off
REM HADOOP_HOME을 설정한 뒤 Jupyter 실행 (winutils 인식용)
set HADOOP_HOME=E:\IT_SPACES\AI\ZoomCamp\DE\06\tools\hadoop-3.3.5
set PATH=%PATH%;%HADOOP_HOME%\bin

cd /d E:\IT_SPACES\AI\ZoomCamp\DE\06\Batch\code
call E:\IT_SPACES\AI\ZoomCamp\DE\06\venv\Scripts\activate.bat
jupyter notebook
