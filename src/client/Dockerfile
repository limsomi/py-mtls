# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# 소스 코드 복사
COPY src/client/client_tls.py ./client_tls.py
COPY ssl ./ssl
COPY requirements.txt ./requirements.txt

# 필요한 패키지 설치 (필요 시)
RUN pip install --no-cache-dir -r requirements.txt


# 서버 실행
CMD ["python", "client_tls.py"]
