# 🎓 PaddleOCR Tutorial - Flet UI

**완전한 PaddleOCR 튜토리얼을 위한 현대적인 웹/데스크톱 UI**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flet](https://img.shields.io/badge/flet-0.25.2-green.svg)

## 🌟 주요 특징

### 📚 완전한 튜토리얼 커버리지
- **섹션 2.3**: 기본 CLI 예제
- **섹션 2.4**: Python API 사용법
- **섹션 3.1**: 다국어 지원 (80+ 언어)
- **섹션 3.2**: 모듈러 파이프라인
- **섹션 4**: 성능 테스트 및 벤치마킹

### 🖥️ 현대적인 UI/UX
- **반응형 웹 인터페이스**: 모든 기기에서 최적화
- **데스크톱 앱 모드**: 독립 실행형 애플리케이션
- **실시간 진행률**: 시각적 피드백과 로그
- **다크/라이트 테마**: 사용자 선호도 지원

### 📊 고급 분석 기능
- **성능 시각화**: 차트와 그래프
- **실시간 모니터링**: 처리 시간 및 메모리 사용량
- **결과 내보내기**: JSON, PNG, PDF 형식
- **비교 분석**: 튜토리얼 섹션간 성능 비교

### 🔧 유연한 실행 모드
- **실제 OCR 모드**: PaddleOCR 엔진 사용
- **시뮬레이션 모드**: 의존성 없이도 학습 가능
- **하이브리드 모드**: 일부 기능만 사용 가능할 때

## 🚀 빠른 시작

### 1. 설치

```bash
# Git 클론
git clone <repository-url>
cd paddleocr_tutorial

# 의존성 설치
pip install -r requirements_flet.txt

# 또는 최소 설치
pip install flet opencv-python pillow numpy
```

### 2. 실행

```bash
# 웹 브라우저 모드
python run_flet_ui.py

# 데스크톱 앱 모드  
python run_flet_ui.py --desktop

# 커스텀 포트
python run_flet_ui.py --port 8080
```

### 3. 첫 사용

1. **브라우저에서 접속**: http://localhost:8551
2. **OCR 엔진 초기화**: "OCR 엔진 초기화" 버튼 클릭
3. **튜토리얼 선택**: 원하는 섹션 또는 "전체 튜토리얼 실행"
4. **결과 확인**: 실시간 로그 및 성능 분석 확인

## 📋 시스템 요구사항

### 최소 요구사항
- **Python**: 3.8 이상
- **RAM**: 2GB 이상
- **저장공간**: 1GB 여유 공간
- **네트워크**: 초기 모델 다운로드 시 필요

### 권장 사항
- **Python**: 3.10 이상
- **RAM**: 4GB 이상 (PaddleOCR 사용 시)
- **CPU**: 멀티코어 (성능 향상)

## 🎯 사용 사례

### 👨‍🎓 교육 및 학습
- PaddleOCR 개념 이해
- 단계별 튜토리얼 진행
- 실습과 이론의 통합

### 🔬 연구 및 개발
- OCR 성능 벤치마킹
- 다국어 처리 성능 비교
- 모델 선택 가이드라인

### 🏭 프로덕션 준비
- 실제 사용사례 테스트
- 성능 최적화 전략
- 에러 핸들링 패턴

## 📊 기능 상세

### 튜토리얼 실행 엔진
```python
# Tutorial Wrapper 사용 예시
from tutorial_wrapper import get_tutorial_wrapper

wrapper = get_tutorial_wrapper()
result = wrapper.execute_tutorial("01_basic_cli")
print(f"실행 시간: {result.duration:.2f}초")
```

### 성능 시각화
```python
# Performance Visualizer 사용 예시
from performance_visualizer import generate_performance_chart

chart_data = generate_performance_chart(tutorial_results)
if chart_data["chart_available"]:
    # 차트를 UI에 표시
    display_chart(chart_data["chart_base64"])
```

### OCR 엔진 통합
```python
# Enhanced OCR Engine 사용 예시
from core.ocr_engine import EnhancedOCREngine

engine = EnhancedOCREngine(lang='korean', model_type='mobile')
result = engine.process_image('test_image.png')
```

## 🔧 구성 요소

### 핵심 모듈
- **`flet_ui_app.py`**: 메인 UI 애플리케이션
- **`tutorial_wrapper.py`**: 튜토리얼 실행 래퍼
- **`performance_visualizer.py`**: 성능 분석 및 시각화
- **`run_flet_ui.py`**: 실행 스크립트

### UI 컴포넌트
- **헤더**: 프로젝트 정보 및 상태
- **설정 패널**: 언어, 엔진 설정
- **튜토리얼 선택**: 그리드 레이아웃 카드
- **파일 업로드**: 드래그 앤 드롭 지원
- **진행률 표시**: 실시간 프로그레스 바
- **결과 탭**: 로그, 요약, 성능 분석

### 백엔드 시스템
- **Threading**: 비동기 처리
- **Error Handling**: 포괄적 오류 처리
- **Logging**: 구조화된 로그 시스템
- **State Management**: UI 상태 관리

## 📈 성능 분석

### 지원되는 메트릭
- **실행 시간**: 튜토리얼별, 전체 시간
- **성공률**: 성공/실패 비율
- **메모리 사용량**: 피크 및 평균 사용량
- **처리량**: 이미지/초, 텍스트/초

### 시각화 옵션
- **바 차트**: 튜토리얼별 실행 시간
- **파이 차트**: 성공률 분포
- **라인 차트**: 시간별 성능 변화
- **히트맵**: 다국어 성능 매트릭스

## 🌍 다국어 지원

### UI 언어
- 한국어 (기본값)
- 영어 (부분 지원)

### OCR 언어 (PaddleOCR)
- **라틴 계열**: English, French, German, Spanish
- **아시아 계열**: Korean, Chinese, Japanese
- **기타**: Arabic, Russian, Thai 등 80+ 언어

## 🛠️ 개발자 가이드

### 프로젝트 구조
```
paddleocr_tutorial/
├── flet_ui_app.py          # 메인 UI 애플리케이션
├── tutorial_wrapper.py     # 튜토리얼 실행 래퍼
├── performance_visualizer.py # 성능 분석
├── run_flet_ui.py         # 실행 스크립트
├── requirements_flet.txt  # UI 의존성
├── core/                  # 핵심 OCR 엔진
├── examples/              # 튜토리얼 예제들
├── assets/                # UI 에셋
└── results/               # 결과 출력
```

### 확장 가이드
1. **새로운 튜토리얼 추가**: `tutorial_wrapper.py`에 섹션 등록
2. **UI 컴포넌트 추가**: `flet_ui_app.py`에 새로운 탭/패널 추가
3. **성능 메트릭 추가**: `performance_visualizer.py`에 새로운 차트 타입
4. **언어 지원 추가**: 다국어 리소스 파일 추가

### API 참조
```python
# TutorialWrapper 주요 메서드
wrapper.execute_tutorial(section_id, demo_type="all")
wrapper.execute_all_tutorials(progress_callback)
wrapper.get_available_tutorials()

# PerformanceVisualizer 주요 함수
generate_performance_chart(results, output_dir)
generate_text_report(results)
export_performance_data(results, output_dir)
```

## 🔍 디버깅 및 트러블슈팅

### 로그 레벨
- **INFO**: 일반 진행 상황
- **WARNING**: 주의 사항 (시뮬레이션 모드 등)
- **ERROR**: 오류 발생
- **SUCCESS**: 성공적 완료

### 일반적인 문제들

1. **포트 충돌**
   ```bash
   python run_flet_ui.py --port 8552
   ```

2. **의존성 오류**
   ```bash
   python test_dependencies.py
   pip install -r requirements_flet.txt
   ```

3. **PaddleOCR 모델 다운로드 실패**
   - 인터넷 연결 확인
   - 방화벽 설정 확인
   - 시뮬레이션 모드로 우선 테스트

4. **메모리 부족**
   - 다른 애플리케이션 종료
   - 배치 크기 줄이기
   - CPU 모드 사용

## 📄 라이선스

MIT License - 자세한 내용은 LICENSE 파일 참조

## 🤝 기여하기

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📞 지원

- **이슈 신고**: GitHub Issues
- **문서**: 이 README 및 INSTALL.md
- **예제**: `examples/` 디렉터리

---

**PaddleOCR Tutorial Flet UI**로 OCR 기술을 마스터하세요! 🚀