#!/bin/bash

# eth1 인터페이스가 생길 때까지 대기 (최대 10초 루프)
echo "[gateway] Waiting for eth1 to be attached..."
for i in {1..100}; do
    if ip link show eth1 > /dev/null 2>&1; then
        echo "[gateway] eth1 is now available!"
        break
    fi
    sleep 0.1
done

# 서버 네트워크 (192.168.20.0/24)를 가진 인터페이스 이름을 동적으로 찾음
SERVER_IF=$(ip -o -4 addr show | awk '$4 ~ /^192\.168\.20\./ {print $2}' | head -n1)

if [ -n "$SERVER_IF" ]; then
    echo "[gateway] Found interface for 192.168.20.x → $SERVER_IF"
    ip route add 192.168.20.0/24 dev "$SERVER_IF"
else
    echo "[gateway] ❌ Could not find interface with 192.168.20.x address"
    exit 1
fi

# gateway 실행
python3 gateway.py
