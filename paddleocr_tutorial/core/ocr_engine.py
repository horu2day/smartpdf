"""
Enhanced OCR Engine Implementation

Based on Section 1.2 and 3.1 of the tutorial guide, this module provides
an enhanced wrapper around PaddleOCR with advanced features for production use.
"""

import os
import time
import logging
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class OCRResult:
    """Structure for OCR result data"""
    bbox: List[List[float]]  # Bounding box coordinates
    text: str               # Recognized text
    confidence: float       # Recognition confidence
    

@dataclass
class DocumentResult:
    """Complete document OCR result"""
    image_path: str
    processing_time: float
    total_texts: int
    results: List[OCRResult]
    model_info: Dict[str, Any]


class EnhancedOCREngine:
    """
    Enhanced OCR Engine implementing tutorial guide best practices.
    
    Features:
    - Singleton pattern for efficient model reuse
    - Comprehensive language support  
    - Performance monitoring
    - Error handling and recovery
    - Configurable pipeline components
    """
    
    _instances = {}
    
    def __new__(cls, lang: str = 'en', **kwargs):
        """Singleton pattern to reuse model instances per language"""
        if lang not in cls._instances:
            cls._instances[lang] = super().__new__(cls)
        return cls._instances[lang]
    
    def __init__(self, 
                 lang: str = 'en',
                 use_angle_cls: bool = True,
                 use_gpu: bool = False,
                 model_type: str = 'mobile',  # 'mobile' or 'server'
                 **kwargs):
        """
        Initialize Enhanced OCR Engine
        
        Args:
            lang: Language code (en, korean, ch, etc.)
            use_angle_cls: Enable text orientation classification
            use_gpu: Use GPU acceleration if available
            model_type: Model type selection ('mobile' or 'server')
        """
        # Avoid re-initialization of singleton
        if hasattr(self, 'initialized'):
            return
            
        self.lang = lang
        self.use_angle_cls = use_angle_cls
        self.use_gpu = use_gpu
        self.model_type = model_type
        
        # Initialize performance metrics
        self.stats = {
            'total_processed': 0,
            'total_time': 0.0,
            'avg_processing_time': 0.0,
            'error_count': 0
        }
        
        # Initialize OCR engine
        try:
            logger.info(f"Initializing PaddleOCR for language: {lang}")
            start_time = time.time()
            
            # Configure OCR parameters based on model type
            ocr_kwargs = {
                'use_angle_cls': use_angle_cls,
                'lang': lang,
                'use_gpu': use_gpu,
                **kwargs
            }
            
            # Add server-specific optimizations
            if model_type == 'server':
                ocr_kwargs.update({
                    'det_model_dir': None,  # Use default server models
                    'rec_model_dir': None,
                    'cls_model_dir': None
                })
            
            self.ocr = PaddleOCR(**ocr_kwargs)
            
            init_time = time.time() - start_time
            logger.info(f"OCR engine initialized in {init_time:.2f} seconds")
            
            self.initialized = True
            
        except Exception as e:
            logger.error(f"Failed to initialize OCR engine: {e}")
            raise RuntimeError(f"OCR initialization failed: {e}")
    
    def get_available_languages(self) -> List[str]:
        """Get list of supported languages"""
        # Based on Section 3.1 of tutorial guide
        return [
            'ch', 'en', 'korean', 'japan', 'chinese_cht', 'ta', 'te', 
            'ka', 'latin', 'arabic', 'cyrillic', 'devanagari', 'french', 
            'german', 'structure'
        ]
    
    def validate_image(self, image_path: Union[str, Path]) -> bool:
        """Validate image file before processing"""
        try:
            path = Path(image_path)
            if not path.exists():
                logger.error(f"Image file not found: {image_path}")
                return False
                
            if not path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
                logger.error(f"Unsupported image format: {path.suffix}")
                return False
                
            # Check if image can be opened
            img = cv2.imread(str(path))
            if img is None:
                logger.error(f"Cannot read image: {image_path}")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Image validation failed: {e}")
            return False
    
    def process_image(self, 
                     image_path: Union[str, Path],
                     return_confidence: bool = True,
                     cls: bool = None) -> DocumentResult:
        """
        Process single image with comprehensive error handling
        
        Args:
            image_path: Path to image file
            return_confidence: Include confidence scores
            cls: Override angle classification setting
            
        Returns:
            DocumentResult with processing results and metadata
        """
        start_time = time.time()
        
        try:
            # Validate input
            if not self.validate_image(image_path):
                raise ValueError(f"Invalid image: {image_path}")
            
            # Use instance setting if cls not specified
            if cls is None:
                cls = self.use_angle_cls
            
            logger.info(f"Processing image: {image_path}")
            
            # Perform OCR
            ocr_start = time.time()
            result = self.ocr.ocr(str(image_path), cls=cls)
            ocr_time = time.time() - ocr_start
            
            # Process results
            processed_results = []
            if result and result[0]:  # Check if results exist
                for line in result[0]:
                    bbox = line[0]
                    text_info = line[1]
                    text = text_info[0] if text_info else ""
                    confidence = text_info[1] if text_info and len(text_info) > 1 else 0.0
                    
                    processed_results.append(OCRResult(
                        bbox=bbox,
                        text=text,
                        confidence=confidence
                    ))
            
            processing_time = time.time() - start_time
            
            # Update statistics
            self.stats['total_processed'] += 1
            self.stats['total_time'] += processing_time
            self.stats['avg_processing_time'] = (
                self.stats['total_time'] / self.stats['total_processed']
            )
            
            # Create document result
            doc_result = DocumentResult(
                image_path=str(image_path),
                processing_time=processing_time,
                total_texts=len(processed_results),
                results=processed_results,
                model_info={
                    'language': self.lang,
                    'model_type': self.model_type,
                    'use_angle_cls': cls,
                    'use_gpu': self.use_gpu,
                    'ocr_time': ocr_time
                }
            )
            
            logger.info(
                f"Processed {len(processed_results)} text regions in {processing_time:.2f}s"
            )
            
            return doc_result
            
        except Exception as e:
            self.stats['error_count'] += 1
            logger.error(f"Error processing image {image_path}: {e}")
            raise RuntimeError(f"OCR processing failed: {e}")
    
    def process_batch(self, 
                     image_paths: List[Union[str, Path]],
                     max_workers: int = 4) -> List[DocumentResult]:
        """
        Process multiple images with parallel processing
        
        Args:
            image_paths: List of image file paths
            max_workers: Maximum concurrent workers
            
        Returns:
            List of DocumentResult objects
        """
        results = []
        
        logger.info(f"Processing batch of {len(image_paths)} images")
        
        for i, image_path in enumerate(image_paths):
            try:
                logger.info(f"Processing image {i+1}/{len(image_paths)}: {image_path}")
                result = self.process_image(image_path)
                results.append(result)
                
            except Exception as e:
                logger.error(f"Failed to process {image_path}: {e}")
                # Continue with other images
                continue
        
        logger.info(f"Batch processing completed: {len(results)}/{len(image_paths)} successful")
        return results
    
    def extract_text_only(self, image_path: Union[str, Path]) -> str:
        """Extract only text content without formatting"""
        result = self.process_image(image_path)
        return '\n'.join([ocr_result.text for ocr_result in result.results])
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get engine performance statistics"""
        return {
            **self.stats,
            'success_rate': (
                (self.stats['total_processed'] - self.stats['error_count']) 
                / max(self.stats['total_processed'], 1) * 100
            ),
            'configuration': {
                'language': self.lang,
                'model_type': self.model_type,
                'use_angle_cls': self.use_angle_cls,
                'use_gpu': self.use_gpu
            }
        }
    
    def reset_stats(self):
        """Reset performance statistics"""
        self.stats = {
            'total_processed': 0,
            'total_time': 0.0,
            'avg_processing_time': 0.0,
            'error_count': 0
        }
    
    def save_results(self, 
                    results: List[DocumentResult], 
                    output_dir: Union[str, Path],
                    format: str = 'json') -> str:
        """
        Save processing results to file
        
        Args:
            results: List of DocumentResult objects
            output_dir: Output directory
            format: Output format ('json', 'txt', 'csv')
            
        Returns:
            Path to saved file
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        if format == 'txt':
            output_file = output_dir / f"ocr_results_{timestamp}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                for result in results:
                    f.write(f"Image: {result.image_path}\n")
                    f.write(f"Processing Time: {result.processing_time:.2f}s\n")
                    f.write(f"Total Texts: {result.total_texts}\n")
                    f.write("Recognized Text:\n")
                    for ocr_result in result.results:
                        f.write(f"  {ocr_result.text} (confidence: {ocr_result.confidence:.2f})\n")
                    f.write("\n" + "="*50 + "\n\n")
        
        elif format == 'json':
            import json
            output_file = output_dir / f"ocr_results_{timestamp}.json"
            
            # Convert results to JSON-serializable format
            json_data = []
            for result in results:
                json_data.append({
                    'image_path': result.image_path,
                    'processing_time': result.processing_time,
                    'total_texts': result.total_texts,
                    'model_info': result.model_info,
                    'results': [
                        {
                            'bbox': ocr_result.bbox,
                            'text': ocr_result.text,
                            'confidence': ocr_result.confidence
                        }
                        for ocr_result in result.results
                    ]
                })
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Results saved to: {output_file}")
        return str(output_file)


# Factory function for easy engine creation
def create_ocr_engine(lang: str = 'en', **kwargs) -> EnhancedOCREngine:
    """
    Factory function to create OCR engine with best practices
    
    Args:
        lang: Language code
        **kwargs: Additional OCR parameters
        
    Returns:
        Configured EnhancedOCREngine instance
    """
    return EnhancedOCREngine(lang=lang, **kwargs)