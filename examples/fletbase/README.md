# Flet 기본 애플리케이션

## 프로젝트 소개
이 프로젝트는 Flet 프레임워크를 사용한 기본 애플리케이션입니다. Flet은 Python을 사용하여 Flutter 기반의 애플리케이션을 손쉽게 개발할 수 있게 해주는 프레임워크입니다.

## 기술 스택
- Python 3.9+
- Flet 0.25.2
- 기타 라이브러리 (requirements.txt 참조)

## 기능
- 버튼을 클릭하면 "Hello World" 메시지를 표시합니다.

## 설치 방법

### 1. 저장소 클론
```bash
git clone <repository-url>
cd fletbase
```

### 2. 가상환경 설정
```bash
python -m venv .venv
```

### 3. 가상환경 활성화
Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

### 4. 의존성 설치
```bash
pip install -r requirements.txt
```

## 실행 방법
```bash
python src/main.py
```

## 프로젝트 구조
```
fletbase/
├── .venv/                  # 가상 환경
├── src/                    # 소스 코드
│   ├── main.py             # 메인 애플리케이션 진입점
│   ├── components/         # UI 컴포넌트
│   ├── models/             # 데이터 모델
│   └── utils/              # 유틸리티 함수
├── assets/                 # 정적 자산 (이미지, 폰트 등)
├── tests/                  # 테스트 코드
├── requirements.txt        # 의존성 목록
├── project_plan.md         # 프로젝트 계획
└── README.md               # 프로젝트 설명
```
