import random
import string

# 랜덤한 데이터 리스트
countries = ["US", "KR", "JP", "CN", "DE", "FR", "IN", "BR", "UK", "AU"]
states = ["Seoul", "Tokyo", "Berlin", "Paris", "Delhi", "SaoPaulo", "Shanghai", "NewYork", "London", "Sydney"]
localities = ["Gangnam", "Shibuya", "Mitte", "ChampsElysees", "ConnaughtPlace", "Paulista", "Bund", "Manhattan", "Westminster", "CBD"]
organizations = ["Google", "Amazon", "Microsoft", "Facebook", "Tesla", "OpenAI", "IBM", "Apple", "Samsung", "Huawei"]
organization_units = ["IT", "HR", "Finance", "Security", "R&D", "Marketing", "Sales", "Support", "Legal", "Admin"]
domains = ["example.com", "test.com", "mycompany.org", "random.net", "secure.co"]

# 랜덤 문자열 생성 함수
def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 랜덤 값 생성
random_values = {
    "C": random.choice(countries),
    "ST": random.choice(states),
    "L": random.choice(localities),
    "O": random.choice(organizations),
    "OU": random.choice(organization_units),
    "CN": f"{random_string(5)}.{random.choice(domains)}",
    "email": f"{random_string(5)}@{random.choice(domains)}"
}

# OpenSSL `-subj` 형식으로 출력
subject_string = "/C={C}/ST={ST}/L={L}/O={O}/OU={OU}/CN={CN}/emailAddress={email}".format(**random_values)
print(subject_string)
