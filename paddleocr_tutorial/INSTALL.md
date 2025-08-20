# PaddleOCR Tutorial Flet UI - 설치 가이드

## 🚀 빠른 설치

### 1. 필수 의존성 설치

```bash
# 기본 의존성 설치
pip install flet opencv-python pillow numpy

# 또는 requirements 파일 사용
pip install -r requirements_flet.txt
```

### 2. 선택적 의존성 (추천)

```bash
# PaddleOCR (실제 OCR 기능)
pip install paddleocr paddlepaddle

# 성능 시각화
pip install matplotlib seaborn

# PDF 처리 지원
pip install PyPDF2
```

### 3. 실행

```bash
# 웹 브라우저 모드 (기본값)
python run_flet_ui.py

# 데스크톱 앱 모드
python run_flet_ui.py --desktop

# 특정 포트로 실행
python run_flet_ui.py --port 8080
```

## 📋 전체 의존성 목록

### 필수 (Required)
- `flet>=0.25.2` - UI 프레임워크
- `opencv-python>=4.8.0` - 이미지 처리
- `pillow>=10.0.0` - 이미지 라이브러리
- `numpy>=1.24.0` - 수치 연산

### 선택적 (Optional)
- `paddleocr>=2.10.0` - OCR 엔진 (없으면 시뮬레이션 모드)
- `paddlepaddle>=3.0.0` - PaddleOCR 백엔드
- `matplotlib>=3.7.0` - 차트 생성
- `PyPDF2>=3.0.0` - PDF 처리

## 🔧 트러블슈팅

### 1. Flet 설치 오류
```bash
# 최신 pip 업그레이드
python -m pip install --upgrade pip

# Flet 재설치
pip uninstall flet
pip install flet
```

### 2. OpenCV 설치 오류
```bash
# opencv-python 대신 opencv-python-headless 시도
pip install opencv-python-headless
```

### 3. PaddleOCR 설치 오류 (선택사항)
```bash
# CPU 버전만 설치 (안정성 향상)
pip install paddlepaddle==3.0.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install paddleocr
```

### 4. 한글/유니코드 오류
- Windows에서 콘솔 인코딩 오류 발생 시:
```bash
# 환경변수 설정
set PYTHONIOENCODING=utf-8
python run_flet_ui.py
```

## 📱 실행 모드

### 웹 브라우저 모드 (기본값)
```bash
python run_flet_ui.py
# http://localhost:8551 에서 접속
```

### 데스크톱 앱 모드
```bash
python run_flet_ui.py --desktop
# 독립 실행형 데스크톱 앱으로 실행
```

### 개발 모드
```bash
python run_flet_ui.py --dev
# 핫 리로드 지원
```

## 🎯 기능 확인

설치 후 다음 명령으로 모든 기능이 정상 작동하는지 확인:

```bash
python test_dependencies.py
```

## 🔍 주요 기능

### ✅ 항상 사용 가능한 기능
- Flet UI 인터페이스
- 튜토리얼 섹션 실행 (시뮬레이션)
- 결과 로그 및 요약
- 텍스트 기반 성능 리포트

### 🎯 PaddleOCR 설치 시 추가 기능
- 실제 OCR 처리
- 이미지/PDF 텍스트 인식
- 다국어 지원
- 정확한 성능 측정

### 📊 Matplotlib 설치 시 추가 기능
- 시각적 성능 차트
- 실행 시간 그래프
- 성공률 파이 차트

## 💡 사용 팁

1. **첫 실행 시**: PaddleOCR 모델 다운로드로 시간이 걸릴 수 있음
2. **성능 최적화**: CPU 모드 사용으로 안정성 확보
3. **오프라인 사용**: 모델 다운로드 후 인터넷 없이 사용 가능
4. **멀티플랫폼**: Windows, Linux, macOS 지원

## 🆘 지원

문제가 발생하면:
1. `test_dependencies.py` 실행하여 의존성 확인
2. `requirements_flet.txt` 파일로 재설치
3. GitHub Issues에 문제 신고

---

**참고**: PaddleOCR 없이도 모든 UI 기능과 튜토리얼 구조를 체험할 수 있습니다. 시뮬레이션 모드에서도 완전한 학습 경험을 제공합니다.