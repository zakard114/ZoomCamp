#!/usr/bin/env python3
"""02-search-eval.ipynb: 줄마다 인라인 한글 주석 (기능 + 왜 이 위치에서)."""

import json
from pathlib import Path

NB = Path(__file__).resolve().parents[1] / "04/2026/Evaluation/code/02-search-eval.ipynb"

SOURCES = {
    0: """## 02 — 검색 평가 (Search Evaluation)

- **입력:** `ground_truth-new.csv` (학생 질문 + 정답 document id)
- **검색:** minsearch 인덱스 (FAQ question / section / answer)
- **지표:** Hit Rate, MRR
- **튜닝:** boost 가중치 그리드 서치
""",
    1: """import pandas as pd  # pd.read_csv, DataFrame 처리를 위해 pandas를 import한다.
from evaluation_paths import GROUND_TRUTH_CSV  # GROUND_TRUTH_CSV를 import해서 노트북 cwd와 무관하게 같은 CSV 경로를 쓴다.

df_ground_truth = pd.read_csv(GROUND_TRUTH_CSV)  # read_csv()로 01 단계에서 만든 평가용 질문 CSV를 메모리에 올린다.

ground_truth = df_ground_truth.to_dict(orient="records")  # to_dict(orient="records")로 각 행을 dict로 바꿔 이후 for q in ground_truth 루프에서 쓴다.
""",
    2: """df_ground_truth.head()  # head()로 컬럼(question, course, document)과 값 형태를 먼저 눈으로 확인한다.
""",
    3: """ground_truth = df_ground_truth.to_dict(orient="records")  # to_dict()를 다시 호출해 ground_truth 변수명으로 평가 루프에 넘길 리스트를 확정한다.
""",
    4: """ground_truth[10]  # ground_truth[10]으로 샘플 한 건의 question/document 키 구조를 확인한다.
""",
    5: """from ingest import load_faq_data, build_index  # load_faq_data, build_index를 import해서 FAQ 원문과 검색 인덱스를 준비한다.

documents = load_faq_data()  # load_faq_data()로 검색 대상 FAQ 문서 전체를 불러온다.

documents_llm = []  # documents_llm = []로 llm-zoomcamp만 담을 빈 리스트를 만든다.

for doc in documents:  # for doc in documents로 전체 FAQ를 순회한다.
    if doc["course"] == "llm-zoomcamp":  # doc["course"] == "llm-zoomcamp"이면 이 과정 FAQ만 남긴다.
        documents_llm.append(doc)  # append(doc)로 필터된 문서를 리스트에 넣는다.

documents = documents_llm  # documents = documents_llm으로 검색·평가 대상 문서 집합을 고정한다.
index = build_index(documents)  # build_index(documents)로 question/section/answer 필드 기반 minsearch 인덱스를 만든다.
""",
    6: """boost = {"question": 3.0}  # boost dict로 question 필드 검색 가중치를 3.0으로 설정한다.

index.search(  # index.search()로 인덱스가 실제로 동작하는지 스모크 테스트한다.
    "What is the course about?",  # 첫 인자 query에 테스트 질문 문자열을 넣는다.
    num_results=5,  # num_results=5로 상위 5개만 받아 이후 top-5 평가 설정과 맞춘다.
    boost_dict=boost,  # boost_dict=boost로 question 가중치가 반영되는지 확인한다.
)
""",
    7: """def text_search(query):  # text_search(query) 함수를 정의해 이후 evaluate()에 search_function으로 넘긴다.
    boost_dict = {"question": 3.0, "section": 0.5}  # boost_dict로 question·section 필드별 가중치를 정한다.

    return index.search(  # index.search()를 return해서 호출부에서 검색 결과 리스트를 받게 한다.
        query,  # query 인자로 학생 질문 문자열을 그대로 검색어로 쓴다.
        num_results=5,  # num_results=5로 Hit Rate/MRR 계산에 쓰는 top-5를 유지한다.
        boost_dict=boost_dict,  # boost_dict로 필드별 점수 비중을 검색에 반영한다.
    )
""",
    8: """q = ground_truth[0]  # ground_truth[0]에서 평가 파이프라인 테스트용 샘플 질문 하나를 꺼낸다.
q  # q를 출력해 question, document 키가 있는지 확인한다.
""",
    9: """doc_id = q["document"]  # q["document"]로 이 질문의 정답 FAQ id를 저장한다.
doc_id  # doc_id를 출력해 이후 검색 결과 id와 비교할 기준값을 확인한다.
""",
    10: """results = text_search(q["question"])  # text_search()에 q["question"]을 넣어 실제 검색 top-5를 받는다.
results  # results를 출력해 어떤 FAQ id들이 나오는지 본다.
""",
    11: """for d in results:  # for d in results로 top-5 각 문서를 순회한다.
    print(f'{d["id"]} == {doc_id}: {d["id"] == doc_id}')  # d["id"] == doc_id를 출력해 순위별로 정답 여부를 눈으로 확인한다.
""",
    12: """relevance = []  # relevance = []로 순위별 0/1 벡터를 담을 리스트를 만든다.

for d in results:  # for d in results로 검색 결과 각 순위를 본다.
    relevance.append(int(d["id"] == doc_id))  # append(int(...))로 정답 id면 1, 아니면 0을 넣어 MRR 입력을 만든다.

relevance  # relevance를 출력해 [1,0,0,0,0] 같은 형태를 확인한다.
""",
    13: """def compute_relevance_text(q):  # compute_relevance_text(q)로 질문 1건의 relevance 벡터를 계산하는 함수를 정의한다.
    doc_id = q["document"]  # q["document"]로 정답 id를 꺼내 검색 결과와 비교한다.
    results = text_search(query=q["question"])  # text_search(query=...)로 이 질문에 대한 top-5 검색을 수행한다.

    relevance = []  # relevance = []로 이 질문 전용 0/1 리스트를 초기화한다.
    for d in results:  # for d in results로 top-5를 순회한다.
        relevance.append(int(d["id"] == doc_id))  # append(int(...))로 순위별 hit 여부를 기록한다.

    return relevance  # return relevance로 한 질문의 평가 벡터를 호출부에 돌려준다.
""",
    14: """q = ground_truth[0]  # ground_truth[0]으로 첫 질문 샘플을 고른다.
print(q["question"])  # print(q["question"])로 어떤 질문인지 확인한다.
compute_relevance_text(q)  # compute_relevance_text(q)를 호출해 보통 [1,0,0,0,0] 같은 케이스를 본다.
# [1, 0, 0, 0, 0]
""",
    15: """q = ground_truth[11]  # ground_truth[11]로 정답이 3위에 오는 다른 샘플을 고른다.
print(q["question"])  # print()로 질문 내용을 확인한다.
compute_relevance_text(q)  # compute_relevance_text()로 순위가 낮을 때 relevance 형태를 본다.
# [0, 0, 1, 0, 0]
""",
    16: """[0, 0, 1, 0, 0]  # 위 셀 결과 참고: 정답이 3위일 때 relevance 벡터 예시.
""",
    17: """q = ground_truth[50]  # ground_truth[50]으로 검색 실패(전부 0) 케이스를 본다.
print(q["question"])  # print()로 질문을 확인한다.
compute_relevance_text(q)  # compute_relevance_text()로 miss 케이스 relevance를 확인한다.
# [0, 0, 0, 0, 0]
""",
    18: """[0, 0, 0, 0, 0]  # 위 셀 결과 참고: 정답 문서가 top-5에 없을 때 벡터 예시.
""",
    19: """from tqdm.auto import tqdm  # tqdm을 import해서 전체 ground_truth 루프 진행률을 표시한다.


def compute_relevance_total_text(ground_truth):  # compute_relevance_total_text()로 전체 질문 relevance 리스트를 만든다.
    relevance_total = []  # relevance_total = []로 질문별 relevance 벡터들을 모을 리스트를 초기화한다.

    for q in tqdm(ground_truth):  # for q in tqdm(ground_truth)로 395건 전체를 순회한다.
        relevance = compute_relevance_text(q)  # compute_relevance_text(q)로 질문 하나의 0/1 벡터를 구한다.
        relevance_total.append(relevance)  # append(relevance)로 전체 결과 리스트에 쌓는다.

    return relevance_total  # return relevance_total로 Hit Rate/MRR 입력 데이터를 돌려준다.
""",
    20: """relevance = compute_relevance_total_text(ground_truth)  # compute_relevance_total_text()를 실행해 전체 relevance를 계산한다.
""",
    21: """relevance[:15]  # relevance[:15]로 앞 15건만 잘라 중간 결과 형태를 빠르게 확인한다.
""",
    22: """def compute_relevance(q, search_function):  # compute_relevance()에 search_function 인자를 넣어 boost 튜닝 시 함수만 바꿀 수 있게 한다.
    doc_id = q["document"]  # q["document"]로 정답 id를 가져온다.
    results = search_function(query=q["question"])  # search_function(query=...)로 text_search 대신 다른 검색 함수도 쓸 수 있게 한다.

    relevance = []  # relevance = []로 0/1 벡터를 초기화한다.
    for d in results:  # for d in results로 top-5를 순회한다.
        relevance.append(int(d["id"] == doc_id))  # append(int(...))로 hit 여부를 기록한다.

    return relevance  # return relevance로 한 질문 평가 결과를 반환한다.
""",
    23: """def compute_relevance_total(ground_truth, search_function):  # compute_relevance_total()로 전체 질문 + 임의 검색 함수 조합을 평가한다.
    relevance_total = []  # relevance_total = []로 전체 결과를 담을 리스트를 만든다.

    for q in tqdm(ground_truth):  # for q in tqdm(ground_truth)로 모든 질문을 돈다.
        relevance = compute_relevance(q, search_function)  # compute_relevance(q, search_function)로 검색 함수별 relevance를 구한다.
        relevance_total.append(relevance)  # append()로 질문별 벡터를 모은다.

    return relevance_total  # return relevance_total로 evaluate()에 넘길 데이터를 만든다.
""",
    24: """relevance_total = compute_relevance_total(ground_truth, text_search)  # compute_relevance_total(..., text_search)로 기본 검색 설정의 전체 relevance를 계산한다.
""",
    25: """sample = relevance_total[:15]  # relevance_total[:15]로 15건만 잘라 지표 수동 계산·이해용 샘플을 만든다.
""",
    26: """sample  # sample을 출력해 15개 relevance 벡터를 확인한다.
""",
    27: """14 / 15  # 14/15로 샘플 15건 중 14건 hit라는 수동 계산 예시를 보여준다.
""",
    28: """cnt = 0  # cnt = 0으로 hit 개수 카운터를 초기화한다.

for line in sample:  # for line in sample으로 질문별 relevance 벡터를 순회한다.
    if 1 in line:  # if 1 in line이면 top-5 안에 정답이 하나라도 있다는 뜻이다.
        cnt = cnt + 1  # cnt += 1로 hit 질문 수를 증가시킨다.

cnt / len(sample)  # cnt / len(sample)로 샘플 Hit Rate를 직접 계산한다.
""",
    29: """def hit_rate(relevance):  # hit_rate(relevance) 함수로 전체 relevance에서 Hit Rate를 계산한다.
    cnt = 0  # cnt = 0으로 hit 카운터를 초기화한다.

    for line in relevance:  # for line in relevance로 모든 질문의 relevance 벡터를 본다.
        if 1 in line:  # if 1 in line이면 해당 질문은 검색 성공(hit)이다.
            cnt = cnt + 1  # cnt를 올려 hit 개수를 센다.

    return cnt / len(relevance)  # return cnt/len(relevance)로 hit 비율을 반환한다.
""",
    30: """hit_rate(relevance)  # hit_rate(relevance)를 호출해 text_search 기준 전체 Hit Rate를 본다.
""",
    31: """total_score = 0.0  # total_score = 0.0으로 MRR 합계를 초기화한다.

for line in sample:  # for line in sample으로 샘플 질문별 relevance를 순회한다.
    for rank in range(len(line)):  # for rank in range(len(line))으로 0,1,2,... 순위를 본다.
        if line[rank] == 1:  # line[rank] == 1이면 그 순위에 정답 문서가 있다.
            score = 1 / (rank + 1)  # score = 1/(rank+1)로 reciprocal rank 점수를 구한다.
            total_score = total_score + score  # total_score에 더해 질문당 첫 정답 순위 점수만 반영한다.
            break  # break로 한 질문에서 첫 번째 정답 순위만 MRR에 넣는다.

total_score / len(sample)  # total_score/len(sample)로 샘플 MRR을 수동 계산한다.
""",
    32: """def mrr(relevance):  # mrr(relevance)로 Mean Reciprocal Rank를 계산하는 함수를 정의한다.
    total_score = 0.0  # total_score = 0.0으로 역순위 점수 합을 초기화한다.

    for line in relevance:  # for line in relevance로 각 질문의 relevance 벡터를 본다.
        for rank in range(len(line)):  # for rank로 top-5 순위를 순회한다.
            if line[rank] == 1:  # line[rank] == 1이면 그 순위가 정답 문서 위치이다.
                score = 1 / (rank + 1)  # score = 1/(rank+1)로 reciprocal rank를 계산한다.
                total_score = total_score + score  # total_score에 더한다.
                break  # break로 질문당 첫 정답만 반영한다.

    return total_score / len(relevance)  # return total_score/len(relevance)로 평균 MRR을 반환한다.
""",
    33: """mrr(sample)  # mrr(sample)로 15건 샘플 MRR을 확인한다.
""",
    34: """mrr(relevance)  # mrr(relevance)로 전체 395건 MRR을 확인한다.
""",
    35: """def evaluate(ground_truth, search_function):  # evaluate()로 relevance 계산 + Hit Rate + MRR을 한 번에 수행한다.
    relevance_total = compute_relevance_total(ground_truth, search_function)  # compute_relevance_total()로 해당 검색 함수의 전체 relevance를 만든다.

    return {  # return dict로 두 지표를 함께 돌려준다.
        "hit_rate": hit_rate(relevance_total),  # hit_rate()로 top-5에 정답이 포함된 비율을 계산한다.
        "mrr": mrr(relevance_total),  # mrr()로 정답 순위의 역수 평균을 계산한다.
    }
""",
    36: """evaluate(ground_truth, text_search)  # evaluate(..., text_search)로 기본 boost 설정의 성능을 본다.
""",
    37: """def text_search_v2(query):  # text_search_v2()로 question boost를 낮춘 변형 검색을 정의한다.
    boost_dict = {"question": 2.0, "section": 0.5}  # boost_dict에서 question=2.0으로 v1(3.0)과 비교한다.

    return index.search(  # index.search()로 동일 인덱스에 다른 가중치를 적용한다.
        query,  # query로 학생 질문을 검색한다.
        num_results=5,  # num_results=5로 평가 설정을 유지한다.
        boost_dict=boost_dict,  # boost_dict로 v2 가중치를 반영한다.
    )
""",
    38: """evaluate(ground_truth, text_search_v2)  # evaluate(..., text_search_v2)로 boost 변경 효과를 숫자로 비교한다.
""",
    39: """def search_boost(query, question_boost):  # search_boost()로 question boost만 바꿔가며 실험한다.
    boost_dict = {"question": question_boost, "section": 0.5}  # boost_dict에 question_boost 인자를 넣는다.

    return index.search(  # index.search()로 각 boost 값마다 top-5를 받는다.
        query,  # query에 질문 문자열을 넣는다.
        num_results=5,  # num_results=5로 고정한다.
        boost_dict=boost_dict,  # boost_dict로 가중치를 적용한다.
    )
""",
    40: """for boost in [0.5, 1.0, 3.0, 5.0, 10.0]:  # for boost in [...]로 question 가중치 후보를 순회한다.
    result = evaluate(  # evaluate()로 각 boost마다 Hit Rate/MRR을 계산한다.
        ground_truth,  # ground_truth로 동일 평가 집합을 쓴다.
        lambda query, boost=boost: search_boost(query, boost),  # lambda로 boost 값을 search_boost에 고정해 넘긴다.
    )
    print(f"boost={boost}: {result}")  # print()로 boost별 결과를 바로 비교한다.
""",
    41: """def search_boosts(query, question_boost, answer_boost, section_boost):  # search_boosts()로 세 필드 boost를 동시에 튜닝한다.
    boost_dict = {  # boost_dict에 question/section/answer 가중치를 모두 넣는다.
        "question": question_boost,  # question_boost로 질문 필드 비중을 조절한다.
        "section": section_boost,  # section_boost로 섹션 필드 비중을 조절한다.
        "answer": answer_boost,  # answer_boost로 답변 필드 비중을 조절한다.
    }

    return index.search(  # index.search()로 조합별 top-5를 반환한다.
        query,  # query로 검색한다.
        num_results=5,  # num_results=5로 유지한다.
        boost_dict=boost_dict,  # boost_dict로 세 가중치를 반영한다.
    )
""",
    42: """results = []  # results = []로 그리드 서치 결과를 담을 리스트를 만든다.

for question_boost in [1.0, 2.0, 5.0]:  # for question_boost로 question 가중치 후보를 순회한다.
    for answer_boost in [1.0, 2.0, 4.0, 10.0]:  # for answer_boost로 answer 가중치 후보를 순회한다.
        for section_boost in [0.1, 0.2, 0.5]:  # for section_boost로 section 가중치 후보를 순회한다.
            print(  # print()로 현재 조합을 로그에 남긴다.
                f"Evaluating question_boost={question_boost}, "
                f"answer_boost={answer_boost}, section_boost={section_boost}..."
            )
            result = evaluate(  # evaluate()로 이 boost 조합의 Hit Rate/MRR을 계산한다.
                ground_truth,  # ground_truth 전체로 평가한다.
                lambda query, question_boost=question_boost, answer_boost=answer_boost, section_boost=section_boost: search_boosts(
                    query,  # query를 search_boosts에 전달한다.
                    question_boost,  # question_boost를 고정한다.
                    answer_boost,  # answer_boost를 고정한다.
                    section_boost,  # section_boost를 고정한다.
                ),
            )

            results.append({  # results.append()로 조합별 지표를 저장한다.
                "question": question_boost,  # question 키에 question_boost 값을 기록한다.
                "answer": answer_boost,  # answer 키에 answer_boost 값을 기록한다.
                "section": section_boost,  # section 키에 section_boost 값을 기록한다.
                "hit_rate": result["hit_rate"],  # hit_rate를 저장해 나중에 정렬한다.
                "mrr": result["mrr"],  # mrr을 저장해 최적 조합을 고른다.
            })
""",
    43: """df_results = pd.DataFrame(results)  # DataFrame(results)로 그리드 서치 결과를 표로 만든다.
df_results.sort_values("mrr", ascending=False).head(10)  # sort_values("mrr")로 MRR 상위 10개 boost 조합을 본다.
""",
}


def to_source(text: str, cell_type: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if cell_type == "markdown":
        return [ln + "\n" for ln in text.splitlines()]
    lines = text.splitlines()
    out = [ln + "\n" for ln in lines]
    out[-1] = out[-1].rstrip("\n")
    return out


def main() -> None:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    for idx, src in SOURCES.items():
        if idx >= len(nb["cells"]):
            continue
        cell = nb["cells"][idx]
        ctype = "markdown" if idx == 0 else "code"
        cell["cell_type"] = ctype
        cell["source"] = to_source(src, ctype)
    NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print("done", NB, "cells", len(SOURCES))


if __name__ == "__main__":
    main()
