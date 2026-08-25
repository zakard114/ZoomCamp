# ML 줌캠프 모듈 03 — 노트북 기동 (Windows Git Bash)

한 덩어리로 붙이지 말 것. Git Bash를 새로 열었으면 [A] export를 다시 할 것.  
명령은 **한 줄씩**, 한 단계 **5분**을 넘기면 중단. `uv pip install` / `--reinstall` / 병렬 uv **금지**. numpy를 재설치하지 말 것.

`03/classification/.venv`는 공용 `E:/IT_SPACES/AI/ZoomCamp/ML/.venv` **정션**이다. 패키지를 여기에 또 깔지 말 것.  
레슨 파일: `notebook/notebook.ipynb`. `materials/`는 GitHub 원본(참고용, 그대로 둘 것).

---

## [A] 같은 창이면 생략. 새 Git Bash면 실행

```bash
export UV_PYTHON_INSTALL_DIR="E:/IT_SPACES/AI/.cache/uv-python"
export UV_CACHE_DIR="E:/IT_SPACES/AI/.cache/uv"
export PIP_CACHE_DIR="E:/IT_SPACES/AI/.cache/pip"
export HF_HOME="E:/IT_SPACES/AI/.cache/hf"
export TEMP="E:/IT_SPACES/AI/.cache/tmp"
export TMP="E:/IT_SPACES/AI/.cache/tmp"
export TMPDIR="E:/IT_SPACES/AI/.cache/tmp"
mkdir -p "$UV_PYTHON_INSTALL_DIR" "$UV_CACHE_DIR" "$PIP_CACHE_DIR" "$TEMP"
```

## [B] 노트북 (한 명령씩)

```bash
PY="E:/IT_SPACES/AI/ZoomCamp/ML/.venv/Scripts/python.exe"
```

```bash
cd "E:/IT_SPACES/AI/ZoomCamp/ML/03/classification/notebook"
```

```bash
"$PY" "E:/IT_SPACES/AI/ZoomCamp/ML/.venv/Scripts/jupyter-nbclassic-script.py" notebook.ipynb
```

브라우저가 열리거나 콘솔의 `http://localhost:8888/...` 로 접속. 클래식 UI (Esc / a / b).

## 하지 말 것

- `jupyter notebook` — 공용 venv에 `jupyter-notebook.exe` 없음. 되는 명령은 **nbclassic**.
- `source .venv/Scripts/activate` 후 `jupyter notebook` — activate는 정션 때문에 공용 venv로 들어가지만, 기동은 그래도 위 nbclassic 한 줄이어야 함.
- classification에 패키지 재설치, `--reinstall`, C: Anaconda jupyter.

## 셀에서 확인

```python
import numpy, sklearn, matplotlib
print(numpy.__version__, sklearn.__version__, matplotlib.__version__)
```

기대: `2.4.6  1.9.0  3.11.1`
