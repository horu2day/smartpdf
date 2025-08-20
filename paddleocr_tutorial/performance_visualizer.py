#!/usr/bin/env python3
"""
Performance Visualizer Module
============================

PaddleOCR Tutorial 성능 결과를 시각화하는 모듈
Flet UI에서 사용할 수 있는 차트와 그래프 생성
"""

import time
from typing import List, Dict, Any
from datetime import datetime
import json
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    from io import BytesIO
    import base64
    MATPLOTLIB_AVAILABLE = True
    print("✅ Matplotlib 사용 가능")
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️ Matplotlib 사용 불가 - 기본 텍스트 리포트만 제공")

def generate_performance_chart(tutorial_results: List[Any], output_dir: Path = None) -> Dict[str, Any]:
    """성능 차트 생성"""
    
    if not tutorial_results:
        return {"error": "결과 데이터가 없습니다"}
    
    if not MATPLOTLIB_AVAILABLE:
        return generate_text_report(tutorial_results)
    
    try:
        # 데이터 준비
        titles = []
        durations = []
        statuses = []
        
        for result in tutorial_results:
            titles.append(result.title.replace("섹션 ", "").replace(": ", "\n"))
            durations.append(result.duration)
            statuses.append(result.status)
        
        # 색상 매핑
        color_map = {"success": "#28a745", "failed": "#dc3545", "warning": "#ffc107"}
        colors = [color_map.get(status, "#6c757d") for status in statuses]
        
        # 그래프 생성
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        fig.suptitle("PaddleOCR Tutorial 성능 분석", fontsize=16, fontweight='bold')
        
        # 1. 실행 시간 바 차트
        bars = ax1.bar(range(len(titles)), durations, color=colors, alpha=0.7)
        ax1.set_title("튜토리얼별 실행 시간", fontsize=14)
        ax1.set_xlabel("튜토리얼 섹션", fontsize=12)
        ax1.set_ylabel("실행 시간 (초)", fontsize=12)
        ax1.set_xticks(range(len(titles)))
        ax1.set_xticklabels(titles, rotation=45, ha='right', fontsize=10)
        
        # 시간 라벨 추가
        for i, (bar, duration) in enumerate(zip(bars, durations)):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{duration:.2f}s', ha='center', va='bottom', fontsize=9)
        
        # 2. 성공률 파이 차트
        status_counts = {}
        for status in statuses:
            status_counts[status] = status_counts.get(status, 0) + 1
        
        status_labels = list(status_counts.keys())
        status_values = list(status_counts.values())
        status_colors = [color_map.get(label, "#6c757d") for label in status_labels]
        
        # 한글 라벨 매핑
        label_map = {"success": "성공", "failed": "실패", "warning": "경고"}
        display_labels = [f"{label_map.get(label, label)}\n({count}개)" 
                         for label, count in zip(status_labels, status_values)]
        
        wedges, texts, autotexts = ax2.pie(status_values, labels=display_labels, 
                                          colors=status_colors, autopct='%1.1f%%',
                                          startangle=90)
        ax2.set_title("실행 성공률", fontsize=14)
        
        # 범례 추가
        legend_elements = [mpatches.Patch(color=color_map["success"], label="성공"),
                          mpatches.Patch(color=color_map["failed"], label="실패"),
                          mpatches.Patch(color=color_map["warning"], label="경고")]
        ax1.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        
        # 이미지를 base64로 인코딩
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        # 파일로 저장 (선택사항)
        if output_dir:
            output_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            chart_file = output_dir / f"performance_chart_{timestamp}.png"
            
            with open(chart_file, 'wb') as f:
                f.write(base64.b64decode(image_base64))
        
        # 통계 계산
        total_duration = sum(durations)
        avg_duration = total_duration / len(durations) if durations else 0
        success_rate = (status_counts.get("success", 0) / len(statuses)) * 100 if statuses else 0
        
        return {
            "chart_base64": image_base64,
            "chart_available": True,
            "statistics": {
                "total_tutorials": len(tutorial_results),
                "total_duration": total_duration,
                "average_duration": avg_duration,
                "success_rate": success_rate,
                "success_count": status_counts.get("success", 0),
                "failed_count": status_counts.get("failed", 0)
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "error": f"차트 생성 실패: {str(e)}",
            "chart_available": False,
            "fallback": generate_text_report(tutorial_results)
        }

def generate_text_report(tutorial_results: List[Any]) -> Dict[str, Any]:
    """텍스트 기반 성능 리포트 생성 (matplotlib 없을 때)"""
    
    if not tutorial_results:
        return {"error": "결과 데이터가 없습니다"}
    
    # 통계 계산
    total_duration = sum(result.duration for result in tutorial_results)
    avg_duration = total_duration / len(tutorial_results)
    success_count = sum(1 for result in tutorial_results if result.status == "success")
    failed_count = sum(1 for result in tutorial_results if result.status == "failed")
    success_rate = (success_count / len(tutorial_results)) * 100
    
    # 가장 빠른/느린 튜토리얼
    fastest = min(tutorial_results, key=lambda x: x.duration)
    slowest = max(tutorial_results, key=lambda x: x.duration)
    
    # 텍스트 리포트 생성
    report = f"""
📊 PaddleOCR Tutorial 성능 리포트
{'='*50}
📅 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 전체 통계:
• 총 실행 튜토리얼: {len(tutorial_results)}개
• 성공률: {success_count}/{len(tutorial_results)} ({success_rate:.1f}%)
• 실패 수: {failed_count}개
• 총 소요 시간: {total_duration:.2f}초
• 평균 실행 시간: {avg_duration:.2f}초

⚡ 성능 분석:
• 가장 빠른 튜토리얼: {fastest.title} ({fastest.duration:.2f}초)
• 가장 느린 튜토리얼: {slowest.title} ({slowest.duration:.2f}초)
• 속도 차이: {(slowest.duration - fastest.duration):.2f}초

📋 섹션별 상세 결과:
"""
    
    for i, result in enumerate(tutorial_results, 1):
        status_icon = "✅" if result.status == "success" else "❌" if result.status == "failed" else "⚠️"
        report += f"{i:2d}. {status_icon} {result.title}: {result.duration:.2f}초\n"
    
    report += f"\n{'='*50}\n"
    
    # 시각적 바 차트 (텍스트)
    if tutorial_results:
        max_duration = max(result.duration for result in tutorial_results)
        report += "\n📊 실행 시간 분포 (텍스트 차트):\n"
        
        for result in tutorial_results:
            bar_length = int((result.duration / max_duration) * 30)
            bar = "█" * bar_length + "░" * (30 - bar_length)
            status_char = "✓" if result.status == "success" else "✗"
            report += f"{result.title[:20]:20s} {bar} {result.duration:5.2f}s {status_char}\n"
    
    return {
        "text_report": report,
        "chart_available": False,
        "statistics": {
            "total_tutorials": len(tutorial_results),
            "total_duration": total_duration,
            "average_duration": avg_duration,
            "success_rate": success_rate,
            "success_count": success_count,
            "failed_count": failed_count
        },
        "fastest": {"title": fastest.title, "duration": fastest.duration},
        "slowest": {"title": slowest.title, "duration": slowest.duration},
        "timestamp": datetime.now().isoformat()
    }

def export_performance_data(tutorial_results: List[Any], output_dir: Path) -> str:
    """성능 데이터를 JSON/CSV로 내보내기"""
    
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON 형태로 내보내기
    export_data = {
        "metadata": {
            "export_time": datetime.now().isoformat(),
            "total_tutorials": len(tutorial_results),
            "total_duration": sum(result.duration for result in tutorial_results)
        },
        "results": []
    }
    
    for result in tutorial_results:
        export_data["results"].append({
            "title": result.title,
            "status": result.status,
            "duration": result.duration,
            "details": result.details,
            "error": result.error,
            "timestamp": result.timestamp.isoformat() if hasattr(result, 'timestamp') else ""
        })
    
    # JSON 파일 저장
    json_file = output_dir / f"performance_data_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    return str(json_file)

# 편의 함수들
def create_performance_summary(tutorial_results: List[Any]) -> str:
    """간단한 성능 요약 생성"""
    if not tutorial_results:
        return "결과 데이터가 없습니다."
    
    success_count = sum(1 for r in tutorial_results if r.status == "success")
    total_time = sum(r.duration for r in tutorial_results)
    
    return f"총 {len(tutorial_results)}개 튜토리얼 | 성공 {success_count}개 | 총 시간 {total_time:.1f}초"