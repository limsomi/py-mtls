# 🔐 TLS/SSL 구현 예제 (Python)

이 프로젝트는 Python을 사용한 **TLS (Transport Layer Security)** 및 **SSL (Secure Socket Layer)** 통신의 기본 구현을 소개합니다.  
`server-tls.py` (서버)와 `client-tls.py` (클라이언트) 스크립트로 구성되어 있으며, `Makefile`과 `.bat` 스크립트를 통해 OpenSSL 기반의 인증서 생성도 자동화할 수 있습니다.

---

## 🚀 사용 방법

### 1. 필수 패키지 설치

Python 환경에 필요한 패키지를 설치:

```bash
pip install -r requirements.txt
```

### 2. 인증서 생성
다음 명령어로 TLS/SSL 인증서를 생성

```bash
./genearte_certificate.bat
```

### 3. 서버 및 클라이언트 실행
TLS 서버와 클라이언트를 각각 실행. 서버는 클라이언트 인증서를 요구하면 mTLS 환경응을 구성.

```bash
python src/server-tls.py
python src/client-tls.py
```

### 정리 명령어

- Clean Certificates: Remove generated certificates for a specific name:

    ```bash
    make clean NAME=<name>
    ```

- Clean All: Remove all generated certificates and files:

    ```bash
    make clean-all
    ```
