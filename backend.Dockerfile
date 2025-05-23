# 1. Python 3.9 슬림 이미지 사용
FROM python:3.9-slim

# 2. 컨테이너 내 작업 디렉토리 지정
WORKDIR /app

# 3. 의존성 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4. 앱 소스 복사
COPY app/ ./app/
COPY .env .env

# 5. 서버 실행
CMD ["python", "app/main.py"]
