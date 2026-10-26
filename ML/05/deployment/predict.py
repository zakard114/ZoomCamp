# 파이썬 파일 저장할 때 썼던 모델과 벡터라이저(기준표)를 다시 메모리로 불러올 때 쓰는 도구입니다.
import pickle

# 파이썬으로 웹사이트나 API 서버를 만들 수 있게 해주는 핵심 도구입니다.
from flask import Flask

# 파이썬의 결과물(딕셔너리)을 웹에서 읽을 수 있는 JSON 형식으로 바꿔서 돌려주는 도구입니다.
from flask import jsonify

# 사용자가 웹 서버로 보낸 데이터(고객 정보)를 파이썬에서 꺼내 쓸 수 있게 해주는 도구입니다.
from flask import request


model_file = 'model_C=1.0.bin'

# 1. 아까 저장해 둔 머신러닝 모델 파일(.bin)을 읽기 전용('rb')으로 엽니다.
with open(model_file, 'rb') as f_in:
    # 파일 안에 들어있던 기준표(dv)와 모델(model)을 꺼내서 각각 변수에 담아둡니다.
    dv, model = pickle.load(f_in)

# 2. 'churn'이라는 이름을 가진 플라스크 웹 서버 프로그램을 만듭니다.
app = Flask('churn')


# 3. 누군가가 웹 주소 뒤에 '/predict'라고 적고 데이터를 보내면(POST), 이 아래 함수가 실행됩니다.
@app.route('/predict', methods=['POST'])
def predict():
    # 사용자가 보낸 고객 정보(JSON 데이터)를 파이썬이 이해할 수 있는 딕셔너리로 바꿔서 꺼냅니다.
    customer = request.get_json()

    # 고객 정보를 모델이 이해할 수 있는 형태(숫자 행렬)로 변환합니다.
    X = dv.transform([customer])

    # 모델에 집어넣어서 이탈할 확률(0과 1 사이의 숫자)을 계산하고, 그중 이탈 확률만 뽑아냅니다.
    y_pred = model.predict_proba(X)[0, 1]

    # 확률이 0.5 이상이면 진짜 이탈(True), 아니면 유지(False)로 판단합니다.
    churn = y_pred >= 0.5

    # 클라이언트(보낸 사람)에게 돌려줄 결과를 상자에 담습니다.
    result = {
        'churn_probability': float(y_pred),  # 넘파이 숫자 형식을 파이썬 기본 실수 형식으로 안전하게 바꿉니다.
        'churn': bool(churn),                # 넘파이 참/거짓 형식을 파이썬 기본 참/거짓 형식으로 바꿉니다.
    }

    # 상자에 담은 결과 딕셔너리를 JSON 형식으로 포장해서 응답으로 돌려줍니다.
    return jsonify(result)


# 4. 이 파일을 직접 실행했을 때만 아래 서버 구동 코드가 작동합니다.
if __name__ == "__main__":
    # 에러를 화면에 보여주는 디버그 모드를 켜고, 내 컴퓨터의 모든 곳에서 접속할 수 있도록('0.0.0.0') 9696 포트에서 서버를 켭니다.
    app.run(debug=True, host='0.0.0.0', port=9696)

