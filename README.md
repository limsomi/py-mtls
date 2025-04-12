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

## 📂 디렉토리 구조

. ├── Makefile # 인증서 정리 명령어 포함 ├── requirements.txt # 필요한 Python 패키지 목록 ├── generate_certificate.bat # 인증서 자동 생성 (Windows용) ├── src/ │ ├── server-tls.py # TLS 서버 스크립트 │ └── client-tls.py # TLS 클라이언트 스크립트 ├── ssl/ # 인증서 저장 폴더 │ ├── RootCA/ # 루트 CA 및 통합된 CA 체인 저장 │ │ └── RootCA_with_ClientCA.pem │ │ └── RootCA_with_ServerCA.pem │ ├── server/ # 서버 인증서 저장 폴더 │ │ └── <server-name>/ # 서버별 디렉토리 │ │ ├── <server-name>.pem # 서버 인증서 │ │ └── <server-name>.key # 서버 개인키 │ └── client/ # 클라이언트 인증서 저장 폴더 │ └── <client-name>/ # 클라이언트별 디렉토리 │ ├── <client-name>.crt # 클라이언트 인증서 │ └── <client-name>.key # 클라이언트 개인키