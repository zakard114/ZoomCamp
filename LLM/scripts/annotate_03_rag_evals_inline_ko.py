#!/usr/bin/env python3
"""03-rag-evals.ipynb: 셀 1~ 끝까지 인라인 한글 주석 (셀 0은 기존 주석 유지)."""

import json
from pathlib import Path

NB = Path(__file__).resolve().parents[1] / "04/2026/Evaluation/code/03-rag-evals.ipynb"

# 셀 0은 이미 주석이 있으므로 수정하지 않음
SOURCES = {
    1: """import pandas as pd  # pd를 재import한다 — 커널 재시작 후 셀 0 없이 이후 셀만 실행할 때 DataFrame 처리용.
""",
    2: """ground_truth[10]  # ground_truth[10]으로 샘플 1건의 question·document 키 구조를 확인한다.
""",
    3: """from ingest import load_faq_data, build_index  # load_faq_data, build_index를 import해 RAG 검색용 FAQ·인덱스를 준비한다.

documents = load_faq_data()  # load_faq_data()로 FAQ 캐시(faq_llm_zoomcamp.json)에서 문서 목록을 불러온다.

documents_llm = []  # documents_llm = []로 llm-zoomcamp 코스 FAQ만 담을 빈 리스트를 만든다.

for doc in documents:  # for doc in documents로 전체 문서를 순회한다.
    if doc["course"] == "llm-zoomcamp":  # doc["course"] == "llm-zoomcamp"이면 이 과정 FAQ만 남긴다.
        documents_llm.append(doc)  # append(doc)로 필터된 문서를 리스트에 넣는다.

documents = documents_llm  # documents를 llm-zoomcamp 전용으로 고정해 doc_idx·RAG가 같은 코퍼스를 쓰게 한다.
index = build_index(documents)  # build_index(documents)로 question/section/answer 필드 minsearch 인덱스를 만든다.
""",
    4: """doc_idx = {}  # doc_idx = {}로 FAQ id → 문서 dict를 바로 찾을 해시 맵을 만든다.

for doc in documents:  # for doc in documents로 llm-zoomcamp FAQ 전체를 순회한다.
    doc_idx[doc["id"]] = doc  # doc_idx[doc["id"]] = doc로 ground_truth의 document id로 원문 FAQ를 O(1) 조회한다.
""",
    5: """q = ground_truth[10]  # ground_truth[10]에서 RAG 데모·검증용 샘플 질문 1건(rec)을 꺼낸다.
q  # q를 출력해 question, document 키 구조를 확인한다.
""",
    6: """doc_idx[q['document']]  # doc_idx[q['document']]로 이 질문의 정답 FAQ 원문(question, answer)을 조회한다.
""",
    7: """from dotenv import load_dotenv  # load_dotenv()로 .env에서 OPENAI_API_KEY 등을 환경변수로 읽는다.
from openai import OpenAI  # OpenAI 클라이언트로 RAGWithUsage가 호출할 클라우드 LLM API를 쓴다.

load_dotenv()  # load_dotenv()를 호출해 노트북 실행 시 API 키를 로드한다.
openai_client = OpenAI()  # OpenAI()로 기본 OpenAI 클라이언트를 만들어 assistant에 넘긴다.
""",
    8: """from evaluation_utils import RAGWithUsage  # RAGWithUsage를 import해 검색+생성+토큰 사용량 추적 RAG 래퍼를 쓴다.

assistant = RAGWithUsage(  # RAGWithUsage()로 인덱스·LLM 클라이언트를 묶은 RAG 실행 객체를 만든다.
    index=index,  # index=index로 위에서 만든 FAQ minsearch 인덱스를 검색 백엔드로 쓴다.
    llm_client=openai_client,  # llm_client=openai_client로 OpenAI API로 답변을 생성한다.
    course='llm-zoomcamp',  # course='llm-zoomcamp'로 검색 필터·프롬프트를 이 코스에 맞춘다.
)
""",
    9: """q['question']  # q['question']만 출력해 RAG에 넣을 실제 질문 문자열을 확인한다.
""",
    10: """# 아래 코드 (API 호출 및 비용 발생 부분)
# answer = assistant.rag(q['question'])  # assistant.rag()는 검색+LLM으로 답 생성 — B안(CSV 사용)에서는 API 호출을 건너뜀
""",
    11: """import pandas as pd  # pd.read_csv로 기존 RAG 답변 CSV를 읽기 위해 pandas를 import한다.
from evaluation_paths import RAG_ANSWERS_CSV  # RAG_ANSWERS_CSV로 rag-answers-new.csv 절대경로를 가져온다.
import os  # os.path.exists()로 CSV 파일 존재 여부를 확인한다.

# 파일이 존재하는지 확인하고 로드합니다.
if os.path.exists(RAG_ANSWERS_CSV):  # exists()로 B안용 미리 생성된 CSV가 있는지 검사한다.
    print(f"이미 생성된 파일({RAG_ANSWERS_CSV})을 불러옵니다.")  # 경로를 출력해 어떤 파일을 쓰는지 확인한다.
    df_results = pd.read_csv(RAG_ANSWERS_CSV)  # read_csv()로 395건 RAG 답변 결과를 DataFrame으로 적재한다.
    # 이후 셀에서 변수를 재사용할 수 있도록 딕셔너리 리스트로 변환합니다.
    results = df_results.to_dict(orient="records")  # to_dict(records)로 배치 결과와 동일한 list[dict] 형태를 만든다.
    print(f"{len(results)}개의 답변 데이터를 성공적으로 로드했습니다.")  # 건수를 출력해 cell 0 로드와 일치하는지 확인한다.
else:
    print(f"오류: {RAG_ANSWERS_CSV} 파일을 찾을 수 없습니다. 경로를 확인해주세요.")  # 없으면 A안 배치 실행 또는 경로 점검 안내
""",
    12: """# assistant.total_cost()  # total_cost()는 누적 API 비용(USD)을 반환 — B안에서는 rag() 미호출이라 여기서는 주석 처리
""",
    13: """# print(answer)  # print(answer)로 assistant.rag() 생성 답 출력 — B안에서는 answer 변수가 없어 주석 처리
""",
    14: """# 방금 로드한 결과 데이터(df_results)에서 첫 번째 행의 답변 확인
first_row = df_results.iloc[0]  # iloc[0]으로 CSV 첫 행을 꺼내 RAG 출력 형식(question, answer_llm, answer_orig)을 본다.

print(f"질문: {first_row['question']}")  # question 컬럼으로 평가 대상 질문을 확인한다.
print(f"생성된 답변: {first_row['answer_llm']}")  # answer_llm으로 LLM이 만든 답을 본다.
print(f"원본 답변: {first_row['answer_orig']}")  # answer_orig으로 FAQ 정답 원문과 비교 기준을 확인한다.
""",
    15: """doc_id = q["document"]  # q["document"]로 샘플 질문의 정답 FAQ id를 꺼낸다.
original_doc = doc_idx[doc_id]  # doc_idx[doc_id]로 id에 해당하는 FAQ 전체 레코드를 조회한다.
answer_orig = original_doc["answer"]  # original_doc["answer"]로 FAQ 원문 답변(answer_orig)을 추출한다.

answer_orig  # answer_orig를 출력해 rag_result·평가 시 비교할 기준 답을 확인한다.
""",
    16: """# rag_result = {
#     "question": q['question'],
#     "answer_llm": answer,
#     "answer_orig": answer_orig,
#     "document": doc_id,
# }
#
# rag_result
#
# 대체용 코드 (CSV에서 샘플 레코드 가져오기)
# 이 코드는 rag_result를 직접 만들 대신, 이미 로드된 df_results에서 데이터를 확인합니다.
rag_result = df_results.iloc[0].to_dict()  # iloc[0].to_dict()로 CSV 첫 행을 단건 rag_result dict로 만든다 — B안에서 API 없이 동일 구조 확인

print("성공적으로 레코드를 로드했습니다:")  # 샘플 1건 로드 성공 메시지
print(rag_result)  # rag_result를 출력해 generate_rag_answer() 반환 형식과 맞는지 본다.
""",
    17: """def generate_rag_answer(rec):  # generate_rag_answer(rec)로 ground_truth 1행마다 RAG 답변·원문을 묶는 배치 함수를 정의한다 — A안 배치의 핵심
    question = rec["question"]  # rec["question"]으로 학생 질문 문자열을 꺼낸다.
    doc_id = rec["document"]  # rec["document"]로 정답 FAQ id를 꺼낸다.
    original_doc = doc_idx[doc_id]  # doc_idx[doc_id]로 원문 FAQ를 조회한다.

    answer_llm = assistant.rag(question)  # assistant.rag(question)으로 검색+LLM 생성 답변을 받는다.
    answer_orig = original_doc["answer"]  # original_doc["answer"]로 평가·비교용 FAQ 정답 원문을 넣는다.

    result = {  # result dict로 04-llm-judge.ipynb가 기대하는 4개 필드를 만든다.
        "question": question,
        "answer_llm": answer_llm,
        "answer_orig": answer_orig,
        "document": doc_id,
    }

    return result  # return result로 map_progress·CSV 저장 단계에 넘긴다.
""",
    18: """# [강의 본 코드 - 주석 처리]
# record = generate_rag_answer(q)  # generate_rag_answer(q)는 API 1회 호출 — B안에서는 비용 절약을 위해 스킵
# record

# [대체용 코드 - 전체 코드]
# 1. generate_rag_answer(q)를 실행하는 API 호출을 생략합니다.
# 2. 대신 이미 로드된 df_results(CSV)에서 해당 질문에 맞는 레코드를 찾습니다.

def get_record_from_csv(question_text):  # get_record_from_csv()로 CSV에서 question 일치 행을 rag_result 형태로 꺼낸다.
    # df_results에서 질문이 일치하는 행을 찾음
    match = df_results[df_results['question'] == question_text]  # boolean mask로 question 컬럼 전체 일치 행을 필터한다.
    if not match.empty:  # empty가 아니면 해당 질문의 기존 RAG 결과가 CSV에 있다.
        return match.iloc[0].to_dict()  # iloc[0].to_dict()로 generate_rag_answer()와 같은 dict를 반환한다.
    return None  # 없으면 None — A안 배치 미실행 또는 질문 불일치

# q는 샘플 안에서 꺼낸 단일 질문 딕셔너리입니다.
record = get_record_from_csv(q['question'])  # q['question']으로 샘플 질문의 CSV 레코드를 조회한다.

if record:  # record가 있으면 B안 경로로 동일 검증을 통과했다는 뜻
    print("성공적으로 데이터를 가져왔습니다.")
    print(record)
else:
    print("해당 질문에 대한 기록이 CSV에서 찾을 수 없습니다.")
""",
    19: """assistant.total_cost()  # total_cost()로 누적 OpenAI 호출 비용(USD) 확인 — B안·CSV만 쓴 경우 usages 없어 0.0
""",
    20: """assistant.reset_usage()  # reset_usage()로 usages 리스트를 비워 배치 전 비용 카운터를 0으로 맞춘다 — A안 배치 직전용
""",
    21: """# API 호출을 건너뛰고 CSV만 로드했으므로 결과는 0.0으로 나올 것
assistant.total_cost()  # reset_usage() 직후 total_cost()로 카운터가 0인지 확인한다.
""",
    22: """# from concurrent.futures import ThreadPoolExecutor  # ThreadPoolExecutor로 ground_truth 병렬 RAG 생성 — B안에서는 API 비용 때문에 스킵
# from evaluation_utils import map_progress  # map_progress(pool, seq, f)로 tqdm 진행률과 함께 배치 map
""",
    23: """# with ThreadPoolExecutor(max_workers=6) as pool:
#     results = map_progress(pool, ground_truth, generate_rag_answer)  # A안: 395건 전체 RAG 답변 생성 후 results에 적재

# [대체용 코드] 이미 생성된 CSV 파일을 로드하여 배치 단계 대체
import pandas as pd  # read_csv·to_dict용 pandas 재import (이 셀만 단독 실행 시 대비)
from evaluation_paths import RAG_ANSWERS_CSV  # RAG_ANSWERS_CSV 경로로 동일 CSV를 다시 가리킨다.

# 배치 처리 대신 저장된 CSV 로드
df_results = pd.read_csv(RAG_ANSWERS_CSV)  # read_csv()로 A안 배치와 동일한 results 소스 파일을 읽는다.
results = df_results.to_dict(orient="records")  # to_dict(records)로 이후 DataFrame·head·to_csv 셀과 같은 results 변수를 만든다.

print(f"총 {len(results)}개의 데이터를 CSV에서 성공적으로 로드했습니다.")  # 395건인지 확인
""",
    24: """results[:10]  # results[:10]으로 배치 결과 앞 10건의 question/answer_llm/answer_orig/document 구조를 확인한다.
""",
    25: """df_results = pd.DataFrame(results)  # DataFrame(results)로 list[dict]를 표 형태로 바꿔 head·to_csv에 쓴다.
""",
    26: """df_results.head()  # head()로 저장 전 컬럼 4개와 샘플 5행이 기대 형식인지 눈으로 확인한다.
""",
    27: """assistant.total_cost()  # total_cost()로 전체 배치 OpenAI 비용 합계 확인 — B안(CSV 로드만)이면 0.0
""",
    28: """df_results.to_csv(RAG_ANSWERS_CSV, index=False)  # to_csv()로 rag-answers-new.csv에 395건 저장해 04-llm-judge.ipynb 입력을 확정한다.
""",
    29: """# 노트북 끝 — 저장된 RAG_ANSWERS_CSV로 04-llm-judge.ipynb를 이어서 실행한다.
""",
}


def to_source(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    lines = text.splitlines()
    out = [ln + "\n" for ln in lines]
    out[-1] = out[-1].rstrip("\n")
    return out


def main() -> None:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    for idx, src in SOURCES.items():
        if idx >= len(nb["cells"]):
            continue
        nb["cells"][idx]["source"] = to_source(src)
    NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print("done", NB, "annotated cells", len(SOURCES), "total cells", len(nb["cells"]))


if __name__ == "__main__":
    main()
