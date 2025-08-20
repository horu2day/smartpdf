"""
PaddleOCR Tutorial Core Components

This module provides enhanced OCR functionality based on the comprehensive
tutorial guide, implementing best practices for production-ready OCR applications.
"""

try:
    from .ocr_engine import EnhancedOCREngine
    OCR_ENGINE_AVAILABLE = True
except ImportError:
    OCR_ENGINE_AVAILABLE = False
    # Dummy class when PaddleOCR not available
    class EnhancedOCREngine:
        def __init__(self, *args, **kwargs):
            self.available = False
        def process_image(self, *args, **kwargs):
            return {"error": "PaddleOCR not available"}

try:
    from .pipeline import ModularOCRPipeline
except ImportError:
    class ModularOCRPipeline:
        pass

try:
    from .visualizer import OCRResultVisualizer
except ImportError:
    class OCRResultVisualizer:
        pass

__all__ = ['EnhancedOCREngine', 'ModularOCRPipeline', 'OCRResultVisualizer', 'OCR_ENGINE_AVAILABLE']