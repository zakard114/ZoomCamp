#!/usr/bin/env python
# coding: utf-8

# 파이썬에서 다른 웹 서버로 데이터를 쉽게 보내고 받을 수 있게 해주는 도구입니다.
import requests


# 우리가 방금 켠 이탈 예측 서버의 주소입니다. 이 주소로 데이터를 보낼 겁니다.
url = 'http://localhost:9696/predict'

customer_id = 'xyz-123'
# 서버로 보낼 가상의 고객 정보입니다. (이 사람이 이탈할지 안 할지 물어볼 겁니다)
customer = {
    "gender": "female",
    "seniorcitizen": 0,
    "partner": "yes",
    "dependents": "no",
    "phoneservice": "no",
    "multiplelines": "no_phone_service",
    "internetservice": "dsl",
    "onlinesecurity": "no",
    "onlinebackup": "yes",
    "deviceprotection": "no",
    "techsupport": "no",
    "streamingtv": "no",
    "streamingmovies": "no",
    "contract": "month-to-month",
    "paperlessbilling": "yes",
    "paymentmethod": "electronic_check",
    "tenure": 24,  # 이용 기간
    "monthlycharges": 29.85,
    "totalcharges": (24 * 29.85)
}


# 설정한 주소(url)로 고객 정보(customer)를 JSON 형식으로 감싸서 POST 요청을 보냅니다.
# 서버가 답변으로 보내준 결과물을 파이썬이 읽을 수 있는 딕셔너리로 바꿉니다.
response = requests.post(url, json=customer)

# 서버가 답변으로 보내준 결과물을 파이썬이 읽을 수 있는 딕셔너리로 바꿉니다.
result = response.json()

# 결과를 화면에 출력해서 확인합니다.
print(result)

# 서버로부터 받은 결과 딕셔너리에서 'churn' 값이 True(이탈 예상)인지 확인합니다.
if result['churn'] == True:
    # 이탈할 확률이 높은 고객이므로, 프로모션 할인 메일을 발송한다는 메시지를 출력합니다. (%s에는 고객 아이디가 들어갑니다)
    print('sending promo email to %s' % customer_id)
else:
    # 이탈할 확률이 낮은(유지 예상) 고객이므로, 프로모션 메일을 보내지 않는다는 메시지를 출력합니다.
    print('not sending promo email to %s' % customer_id)
