# Dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y iptables iproute2 net-tools
RUN apt-get update && apt-get install -y iproute2 iputils-ping procps && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install tcpdump -y

# 소스 코드 복사
COPY src/sdp.py ./sdp.py
COPY src/gateway/gateway.py ./gateway.py
COPY utils ./utils
COPY requirements.txt ./requirements.txt
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# 필요한 패키지 설치 (필요 시)
RUN pip install --no-cache-dir -r requirements.txt


# 서버 실행
CMD ["python3","-u", "gateway.py"]
