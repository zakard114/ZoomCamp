# Flask는 파이썬으로 가벼운 웹 서버를 구축해 외부에서 호출할 수 있는 웹 API를 만들게 해주는 마이크로 웹 프레임워크다.
from flask import Flask

# Flask 앱 객체를 생성하고, 이 서비스의 식별자(import name)를 'ping'으로 지정한다.
app = Flask('ping')

# @app.route 데코레이터는 특정 URL 경로와 HTTP 메서드를 함수와 연결해 웹 서비스 기능을 더해 준다.
@app.route('/ping', methods=['GET'])
def ping():
    return "PONG"

# 이 파일을 직접 실행할 때만 웹 서버가 켜지게 한다.
if __name__ == "__main__":
    # 디버그 모드, 모든 네트워크 인터페이스, 9696 포트에서 대기한다.
    app.run(debug=True, host='0.0.0.0', port=9696)

