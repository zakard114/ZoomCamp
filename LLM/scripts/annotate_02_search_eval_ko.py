#!/usr/bin/env python3
"""Add Korean comments to 02-search-eval.ipynb (code cells only)."""

import json
from pathlib import Path

NB = Path(__file__).resolve().parents[1] / "04/2026/Evaluation/code/02-search-eval.ipynb"

# cell_index -> full source (UTF-8)
SOURCES = {
    0: '''import pandas as pd  # 표 형태 데이터 처리
from evaluation_paths import GROUND_TRUTH_CSV  # CSV 절대 경로 (cwd 무관)

# 줌캠프 제공 ground truth CSV 로드 (01에서 생성한 평가용 질문 목록)
df_ground_truth = pd.read_csv(GROUND_TRUTH_CSV)

# DataFrame → 리스트[dict] 로 변환 (이후 루프에서 q["question"] 형태로 접근)
ground_truth = df_ground_truth.to_dict(orient="records")
''',
    1: '''# 상위 5행 미리보기 (question, course, document 컬럼 확인)
df_ground_truth.head()
''',
    2: '''# orient="records": 각 행이 {"question": ..., "document": ...} dict 하나
ground_truth = df_ground_truth.to_dict(orient="records")
''',
    3: '''# 샘플 11번째 질문 레코드 확인
ground_truth[10]
''',
    4: '''from ingest import load_faq_data, build_index  # FAQ 로드 + minsearch 인덱스

documents = load_faq_data()  # FAQ 원문 전체

documents_llm = []  # llm-zoomcamp 과정만 필터링

for doc in documents:
    if doc["course"] == "llm-zoomcamp":
        documents_llm.append(doc)

documents = documents_llm
index = build_index(documents)  # question/section/answer 필드로 검색 인덱스 구축
''',
    5: '''# boost: question 필드 가중치 3.0 — 검색 시 질문 텍스트를 더 크게 반영
boost = {"question": 3.0}

index.search(
    "What is the course about?",
    num_results=5,
    boost_dict=boost,
)
''',
    6: '''# 기본 텍스트 검색 함수 (이 노트북의 메인 search_function)


def text_search(query):
    boost_dict = {"question": 3.0, "section": 0.5}

    return index.search(
        query,
        num_results=5,
        boost_dict=boost_dict,
    )
''',
    7: '''# 평가용 ground truth 첫 번째 질문
q = ground_truth[0]
q
''',
    8: '''# 정답 FAQ 문서 id (검색 결과에 이 id가 있으면 relevant=1)
doc_id = q["document"]
doc_id
''',
    9: '''# 학생 질문으로 검색 → 상위 5개 FAQ 후보
results = text_search(q["question"])
results
''',
    10: '''# 각 검색 결과가 정답 문서 id와 일치하는지 출력
for d in results:
    print(f'{d["id"]} == {doc_id}: {d["id"] == doc_id}')
''',
    11: '''# relevance 벡터: 순위별 1(정답 포함) / 0(미포함)
relevance = []

for d in results:
    relevance.append(int(d["id"] == doc_id))

relevance
''',
    12: '''# 질문 1건에 대한 relevance 계산


def compute_relevance_text(q):
    doc_id = q["document"]
    results = text_search(query=q["question"])

    relevance = []
    for d in results:
        relevance.append(int(d["id"] == doc_id))

    return relevance
''',
    13: '''# 예시: 첫 질문 — 보통 1등에 정답 문서가 오면 [1,0,0,0,0]
q = ground_truth[0]
print(q["question"])
compute_relevance_text(q)
# [1, 0, 0, 0, 0]
''',
    14: '''# 예시: 12번째 질문 — 정답이 3위에 있으면 [0,0,1,0,0]
q = ground_truth[11]
print(q["question"])
compute_relevance_text(q)
# [0, 0, 1, 0, 0]
''',
    15: '''# 위 셀 결과 참고용
[0, 0, 1, 0, 0]
''',
    16: '''# 예시: 검색 실패 케이스 — 전부 0
q = ground_truth[50]
print(q["question"])
compute_relevance_text(q)
# [0, 0, 0, 0, 0]
''',
    17: '''# 위 셀 결과 참고용
[0, 0, 0, 0, 0]
''',
    18: '''from tqdm.auto import tqdm  # 전체 ground truth 진행률 표시


def compute_relevance_total_text(ground_truth):
    relevance_total = []

    for q in tqdm(ground_truth):
        relevance = compute_relevance_text(q)
        relevance_total.append(relevance)

    return relevance_total
''',
    19: '''# 전체 질문에 대해 relevance 리스트 생성 (시간 소요)
relevance = compute_relevance_total_text(ground_truth)
''',
    20: '''# 앞 15개 질문의 relevance만 확인
relevance[:15]
''',
    21: '''# search_function을 인자로 받는 일반화 버전 (튜닝 시 재사용)


def compute_relevance(q, search_function):
    doc_id = q["document"]
    results = search_function(query=q["question"])

    relevance = []
    for d in results:
        relevance.append(int(d["id"] == doc_id))

    return relevance
''',
    22: '''# ground truth 전체 + 임의 검색 함수로 relevance_total 계산


def compute_relevance_total(ground_truth, search_function):
    relevance_total = []

    for q in tqdm(ground_truth):
        relevance = compute_relevance(q, search_function)
        relevance_total.append(relevance)

    return relevance_total
''',
    23: '''# text_search 기준 전체 relevance
relevance_total = compute_relevance_total(ground_truth, text_search)
''',
    24: '''# 샘플 15건만 지표 계산용으로 사용
sample = relevance_total[:15]
''',
    25: '''sample
''',
    26: '''# (참고) 15건 중 14건에서 hit — 수동 계산 예시
14 / 15
''',
    27: '''# 샘플 hit rate 수동 계산: relevance 줄에 1이 하나라도 있으면 hit
cnt = 0

for line in sample:
    if 1 in line:
        cnt = cnt + 1

cnt / len(sample)
''',
    28: '''# Hit Rate: top-k 중 정답 문서가 하나라도 나온 질문 비율


def hit_rate(relevance):
    cnt = 0

    for line in relevance:
        if 1 in line:
            cnt = cnt + 1

    return cnt / len(relevance)
''',
    29: '''# 전체 ground truth 기준 hit rate
hit_rate(relevance)
''',
    30: '''# MRR 수동 계산 예시: 정답 순위 r이면 1/(r+1), 질문당 첫 정답만 합산
total_score = 0.0

for line in sample:
    for rank in range(len(line)):
        if line[rank] == 1:
            score = 1 / (rank + 1)
            total_score = total_score + score
            break

total_score / len(sample)
''',
    31: '''# MRR (Mean Reciprocal Rank): 정답 문서의 역순위 평균


def mrr(relevance):
    total_score = 0.0

    for line in relevance:
        for rank in range(len(line)):
            if line[rank] == 1:
                score = 1 / (rank + 1)
                total_score = total_score + score
                break

    return total_score / len(relevance)
''',
    32: '''# 샘플 15건 MRR
mrr(sample)
''',
    33: '''# 전체 relevance MRR
mrr(relevance)
''',
    34: '''# 검색 함수 하나로 hit_rate + mrr 한 번에 계산


def evaluate(ground_truth, search_function):
    relevance_total = compute_relevance_total(ground_truth, search_function)

    return {
        "hit_rate": hit_rate(relevance_total),
        "mrr": mrr(relevance_total),
    }
''',
    35: '''# 기본 text_search 성능
evaluate(ground_truth, text_search)
''',
    36: '''# question boost를 2.0으로 낮춘 변형 검색


def text_search_v2(query):
    boost_dict = {"question": 2.0, "section": 0.5}

    return index.search(
        query,
        num_results=5,
        boost_dict=boost_dict,
    )
''',
    37: '''# v2 boost 비교
evaluate(ground_truth, text_search_v2)
''',
    38: '''# question boost만 바꿔가며 검색 (튜닝용)


def search_boost(query, question_boost):
    boost_dict = {"question": question_boost, "section": 0.5}

    return index.search(
        query,
        num_results=5,
        boost_dict=boost_dict,
    )
''',
    39: '''# question boost 후보군 스윕
for boost in [0.5, 1.0, 3.0, 5.0, 10.0]:
    result = evaluate(
        ground_truth,
        lambda query, boost=boost: search_boost(query, boost),
    )
    print(f"boost={boost}: {result}")
''',
    40: '''# question / answer / section boost 동시 튜닝용 검색


def search_boosts(query, question_boost, answer_boost, section_boost):
    boost_dict = {
        "question": question_boost,
        "section": section_boost,
        "answer": answer_boost,
    }

    return index.search(
        query,
        num_results=5,
        boost_dict=boost_dict,
    )
''',
    41: '''# 3중 루프로 boost 조합 그리드 서치
results = []

for question_boost in [1.0, 2.0, 5.0]:
    for answer_boost in [1.0, 2.0, 4.0, 10.0]:
        for section_boost in [0.1, 0.2, 0.5]:
            print(
                f"Evaluating question_boost={question_boost}, "
                f"answer_boost={answer_boost}, section_boost={section_boost}..."
            )
            result = evaluate(
                ground_truth,
                lambda query, question_boost=question_boost, answer_boost=answer_boost, section_boost=section_boost: search_boosts(
                    query,
                    question_boost,
                    answer_boost,
                    section_boost,
                ),
            )

            results.append({
                "question": question_boost,
                "answer": answer_boost,
                "section": section_boost,
                "hit_rate": result["hit_rate"],
                "mrr": result["mrr"],
            })
''',
    42: '''# MRR 상위 10개 boost 조합
df_results = pd.DataFrame(results)
df_results.sort_values("mrr", ascending=False).head(10)
''',
}


def to_cell_source(text: str) -> list[str]:
    lines = text.splitlines()
    if not lines:
        return []
    out = [ln + "\n" for ln in lines]
    out[-1] = out[-1].rstrip("\n")
    return out


def main() -> None:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    for idx, src in SOURCES.items():
        if idx >= len(nb["cells"]):
            continue
        cell = nb["cells"][idx]
        if cell.get("cell_type") != "code":
            continue
        cell["source"] = to_cell_source(src.strip() + "\n")
    NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print("annotated", NB, "cells", len(SOURCES))


if __name__ == "__main__":
    main()
