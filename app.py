from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# --- ⚠️ 중요: 네이버 API 인증 정보 입력 ⚠️ ---
# 실제 값으로 대체해야 합니다!
CLIENT_ID = "rp4gWjzI5KM1csxw_vrG" 
CLIENT_SECRET = "EVrG8hiBzA"
# ---------------------------------------------

# 네이버 블로그 검색 API URL
NAVER_API_URL = "https://openapi.naver.com/v1/search/blog.json"

@app.route('/blog', methods=['GET', 'POST'])
def search_blog():
    search_results = None
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # 1. API 요청 헤더 설정
            headers = {
                "X-Naver-Client-Id": CLIENT_ID,
                "X-Naver-Client-Secret": CLIENT_SECRET
            }
            
            # 2. API 요청 파라미터 설정
            # query: 검색어, display: 검색 결과 수 (최대 100), sort: 정렬 옵션 (sim: 정확도순, date: 날짜순)
            params = {
                "query": query, # 검색어에 "맛집"을 추가하여 블로그 검색 정확도 높이기
                "display": 20,
                "sort": "sim" 
            }

            # 3. 네이버 API 호출
            response = requests.get(NAVER_API_URL, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                search_results = data.get('items')
            else:
                # API 호출 오류 처리
                print(f"Error: {response.status_code}, {response.text}")

    # GET 요청이나 검색 결과가 없는 경우 None을 전달
    return render_template('index.html', search_results=search_results)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)