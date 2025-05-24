# 🏥 Pharmacy API Service (Kubernetes + Docker)

서울시 약국 정보를 공공데이터 포털에서 수집하고,  
Flask 백엔드 + HTML/JS 프론트엔드로 사용자에게 제공하는 **컨테이너 기반 분산 서비스**입니다.

---

## 📦 프로젝트 개요

- **공공 API 수집기능**: 서울시 강서구, 강남구, 강북구 약국 정보 요청
- **Flask API 서버**: `/startCollecting` API로 JSON 응답 제공
- **프론트엔드**: HTML + jQuery로 사용자 인터페이스 구성
- **Docker로 패키징 후 Kubernetes에 배포**
- **MetalLB로 외부 IP 부여**, Ingress를 통한 웹 진입점 관리

---

## 🗂️ 프로젝트 구조

```bash
pharmacy-api-docker-k8s/
├── app/                         # Flask 백엔드
│   └── main.py
├── frontend/                    # 정적 프론트엔드 리소스
│   ├── index.html
│   └── script.js
├── k8s/                         # Kubernetes 리소스 정의
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── pharmacy-service-lb.yaml
│   ├── ingress.yaml
│   └── metallb-config.yaml
├── backend.Dockerfile           # 백엔드 Docker 설정
├── frontend.Dockerfile          # 프론트 Docker 설정
├── requirements.txt             # 백엔드 의존성
├── .env                         # API 키 환경변수
└── README.md
```

---

## 🐳 Docker 이미지 빌드 및 푸시

### 🔹 백엔드

```bash
docker build -t banghyunmin1999/pharmacy-api:latest -f backend.Dockerfile .
docker push banghyunmin1999/pharmacy-api:latest
```

### 🔹 프론트엔드

```bash
docker build -t banghyunmin1999/pharmacy-frontend:latest -f frontend.Dockerfile ./frontend
docker push banghyunmin1999/pharmacy-frontend:latest
```

---

## ☸️ Kubernetes 배포 순서

### 1. 클러스터 준비

- Master / Worker 구성
- `kubectl get nodes` 확인

### 2. MetalLB 설치

```bash
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.9/config/manifests/metallb-native.yaml
kubectl apply -f k8s/metallb-config.yaml
```

### 3. Secret 생성

```bash
kubectl create secret generic pharmacy-secret --from-literal=API_KEY=<your_api_key>
```

### 4. 백엔드 + 프론트엔드 배포

```bash
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/pharmacy-service-lb.yaml

kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

### 5. Ingress 설치 및 설정

```bash
kubectl apply -f k8s/ingress.yaml
```

---

## 🌐 외부 접속 경로

| 목적 | 주소 예시 |
|------|-----------|
| 프론트 접속 | http://192.168.56.61/web |
| API 호출 | http://192.168.56.240/startCollecting |


---

## 🧪 테스트 방법

### ✅ 브라우저 접속

- `http://192.168.56.61/web` → 버튼 클릭 → 결과 출력

### ✅ Postman 테스트

```http
GET http://192.168.56.240/startCollecting
```

→ JSON 형식으로 약국 리스트 응답

### ✅ curl 테스트

```bash
curl http://192.168.56.240/startCollecting
```

---

## 📊 주요 기능 요약

| 기능 | 설명 |
|------|------|
| Flask API | `/startCollecting`에서 약국 데이터 수집 후 JSON 응답 |
| jQuery | Ajax로 API 호출하여 결과 테이블로 렌더링 |
| Docker | 백엔드/프론트 분리 컨테이너화 |
| Kubernetes | 분산 클러스터에서 서비스 관리 |
| MetalLB | LoadBalancer로 외부 IP 노출 |
| Ingress | `/web` 경로로 프론트 서비스 라우팅 |

---

## 💡 운영 가이드

- API 키는 `.env` → Docker COPY 또는 Kubernetes Secret으로 분리
- 코드 수정 시:
  1. `docker build && docker push`
  2. `kubectl rollout restart deployment <name>`
- 로그 확인:
  ```bash
  kubectl logs deploy/pharmacy-api
  ```

---

## 🧾 참고

- 프로젝트 작성자: 방현민  
- GitHub: [github.com/banghyunmin1999/pharmacy-api-docker-k8s](https://github.com/banghyunmin1999/pharmacy-api-docker-k8s)
