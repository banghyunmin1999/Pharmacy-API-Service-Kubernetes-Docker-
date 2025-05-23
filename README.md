# 💊 Pharmacy API with Flask + HTML Frontend (Kubernetes 배포)

공공데이터 약국 정보를 실시간 수집하고, 웹에서 확인할 수 있는 **Flask 기반 백엔드**와 **HTML + JS 프론트엔드** 프로젝트입니다.  
Docker로 컨테이너화하고, Kubernetes 위에 **실제 서비스 구조처럼 배포**되며, `/api`, `/web` 경로로 분기됩니다.

---

## 📌 주요 기능

- ✅ Flask 기반 공공데이터 수집 API (`/api/startCollecting`)
- ✅ HTML + jQuery 프론트엔드 (`/web`)
- ✅ Docker 컨테이너화 및 Docker Hub 업로드
- ✅ Kubernetes 클러스터에 Deployment + Service 구성
- ✅ MetalLB 설치로 LoadBalancer 외부 IP 자동 할당
- ✅ Ingress 설정으로 경로 기반 트래픽 분기

---

## 🧱 프로젝트 구조

pharmacy-api-docker-k8s/
├── app/ # Flask 백엔드 코드
│ └── main.py
├── frontend/ # HTML + JS 프론트
│ ├── index.html
│ └── script.js
├── backend.Dockerfile
├── frontend.Dockerfile
├── k8s/ # Kubernetes 배포 YAML들
│ ├── backend-deployment.yaml
│ ├── frontend-deployment.yaml
│ ├── pharmacy-service-lb.yaml
│ ├── frontend-service.yaml
│ ├── ingress.yaml
│ └── metallb-config.yaml
├── requirements.txt
└── README.md

---

## 🚀 실행 흐름 요약
브라우저 접속 → /web (프론트 로딩)
↓
사용자 버튼 클릭 → /api/startCollecting 호출
↓
Ingress → Flask → 공공데이터 포털 → JSON 응답
↓
프론트에서 결과 출력


---

## 🐳 Docker 이미지

| 구성 | 이미지 |
|------|--------|
| 백엔드 | `banghyunmin1999/pharmacy-api:latest` |
| 프론트 | `banghyunmin1999/pharmacy-frontend:latest` |

---

## ☸ Kubernetes 주요 리소스

### 🔹 Flask 백엔드

- `backend-deployment.yaml`
- `pharmacy-service-lb.yaml` → `type: LoadBalancer` 사용

### 🔹 HTML 프론트

- `frontend-deployment.yaml`
- `frontend-service.yaml`

### 🔹 Ingress 라우팅

📄 `ingress.yaml`

```yaml
- path: /api(/|$)(.*) → pharmacy-service
- path: /web(/|$)(.*) → frontend-service

🌐 외부 접속 예시
경로	기능
http://192.168.56.240/web	프론트 페이지
http://192.168.56.240/api/startCollecting	약국 정보 수집 API

IP는 MetalLB가 할당한 외부 IP

⚙ 설치 필수 구성 요소
Docker

VirtualBox + Ubuntu (2노드: Master + Worker)

Kubernetes (kubeadm, kubectl, kubelet)

MetalLB (v0.14.x)

ingress-nginx Controller

🙌 마무리
이 프로젝트를 통해 Kubernetes 실습 환경에서 실무와 동일한 구조로 API + 웹 서비스를 배포하는 경험을 할 수 있습니다.

구성부터 배포까지 모든 흐름을 직접 구성한 💪 풀사이클 클라우드 애플리케이션 실습 예제입니다.

✨ 제작
🧑‍💻 개발자: banghyunmin1999

📦 배포: Docker Hub + Kubernetes + MetalLB + Ingress



---

