@echo off
REM NumPy 2.x vs pandas/numexpr 충돌 해결
REM Anaconda/Jupyter 커널에서 numpy<2 로 다운그레이드
echo NumPy 다운그레이드 (numpy^<2)...
pip install "numpy<2"
echo 완료. Jupyter 커널을 재시작하세요.
pause
