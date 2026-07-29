# pd.read_parquet() ImportError 해결

## 오류 메시지

```
ImportError: Unable to find a usable engine; tried using: 'pyarrow', 'fastparquet'.
A suitable version of pyarrow or fastparquet is required for parquet support.
- `Import pyarrow` failed. pyarrow is required for parquet support.
- `Import fastparquet` failed. fastparquet is required for parquet support.
```

---

## 원인 분석

### 1. pandas의 Parquet 엔진 의존성

- `pd.read_parquet()`은 **Parquet 형식 전용 엔진**이 필요함
- pandas 자체에는 Parquet 읽기/쓰기 코드가 포함되어 있지 않음
- 지원 엔진: **pyarrow** 또는 **fastparquet** 중 하나 필수

### 2. 왜 이 오류가 발생했는가?

| 항목 | 설명 |
|------|------|
| **pandas만 설치된 상태** | `pip install pandas`만 수행하면 Parquet 지원 라이브러리는 포함되지 않음 |
| **엔진 미설치** | pyarrow, fastparquet 둘 다 설치되지 않아 pandas가 사용할 엔진이 없음 |
| **엔진 선택 순서** | pandas는 먼저 pyarrow를 시도하고, 실패 시 fastparquet를 시도함. 둘 다 없으면 ImportError 발생 |

### 3. 기술적 배경

- Parquet는 **컬럼 기반 바이너리 형식**으로, Apache Arrow와 밀접한 관계가 있음
- **pyarrow**: Apache Arrow의 Python 바인딩, Parquet 처리 시 가장 널리 사용
- **fastparquet**: 대안 구현, 일부 대용량 환경에서 사용

---

## 해결 과정

### 1단계: 필요한 패키지 확인

```bash
pip list | findstr -i "pyarrow fastparquet"
# (결과 없음 → pyarrow, fastparquet 미설치)
```

### 2단계: pyarrow 설치

```bash
# DE venv 환경 기준
E:\IT_SPACES\AI\ZoomCamp\DE\venv\Scripts\python.exe -m pip install pyarrow
```

### 3단계: 설치 확인

```python
import pyarrow
import pandas as pd
df = pd.read_parquet(url, columns=columns)  # 정상 동작
```

---

## 해결 요약

| 구분 | 내용 |
|------|------|
| **원인** | pandas만 설치되어 있어 Parquet 읽기에 필요한 pyarrow/fastparquet 엔진이 없음 |
| **해결** | `pip install pyarrow` 실행 |
| **권장** | 워크샵 환경(Workshop_Stream)에서는 `uv add pyarrow` 또는 `pyproject.toml`에 pyarrow 의존성 추가 |

---

## 앞으로의 예방

Workshop_Stream `pyproject.toml`에는 이미 pyarrow가 포함되어 있음:

```toml
dependencies = [
    "pandas>=3.0.1",
    "pyarrow>=23.0.1",
    ...
]
```

**DE venv**를 사용할 경우, Parquet 작업 전에 다음을 확인:

```bash
pip install pandas pyarrow
```
