#!/usr/bin/env python3
"""
Multilingual OCR Examples - Section 3.1 Implementation

This module demonstrates PaddleOCR multilingual capabilities as described
in Section 3.1 of the comprehensive tutorial guide, showcasing the extensive
language support and model zoo navigation.

Key concepts implemented:
- 80+ language support demonstration
- Model zoo navigation
- Language-specific optimizations
- Performance comparison across languages
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

import cv2
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MultilingualOCRDemo:
    """
    Multilingual OCR demonstration implementing tutorial guide concepts
    """
    
    def __init__(self):
        self.asset_dir = Path(__file__).parent.parent / "assets" / "images"
        self.results_dir = Path(__file__).parent.parent / "assets" / "results"
        
        # Ensure directories exist
        self.asset_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Language information from tutorial Section 3.1
        self.supported_languages = {
            'ch': {'name': 'Chinese (Simplified)', 'script': 'Chinese'},
            'en': {'name': 'English', 'script': 'Latin'},
            'korean': {'name': 'Korean', 'script': 'Hangul'},
            'japan': {'name': 'Japanese', 'script': 'Japanese'},
            'chinese_cht': {'name': 'Chinese (Traditional)', 'script': 'Chinese'},
            'ta': {'name': 'Tamil', 'script': 'Tamil'},
            'te': {'name': 'Telugu', 'script': 'Telugu'},
            'ka': {'name': 'Kannada', 'script': 'Kannada'},
            'latin': {'name': 'Latin Script Languages', 'script': 'Latin'},
            'arabic': {'name': 'Arabic', 'script': 'Arabic'},
            'cyrillic': {'name': 'Cyrillic Script', 'script': 'Cyrillic'},
            'devanagari': {'name': 'Devanagari Script', 'script': 'Devanagari'},
            'french': {'name': 'French', 'script': 'Latin'},
            'german': {'name': 'German', 'script': 'Latin'},
            'structure': {'name': 'Document Structure', 'script': 'Special'}
        }
        
        # Model performance data from tutorial (Table 1)
        self.model_performance = {
            'PP-OCRv5_server_rec': {
                'languages': ['ch', 'chinese_cht', 'en', 'japan'],
                'accuracy': 'High',
                'size': 'Large',
                'scenario': 'Server'
            },
            'PP-OCRv4_server_rec': {
                'languages': ['ch', 'en'],
                'accuracy': 85.19,
                'size': '173MB',
                'scenario': 'Server'
            },
            'PP-OCRv4_mobile_rec': {
                'languages': ['ch', 'en'],
                'accuracy': 'Good',
                'size': '7.5MB',
                'scenario': 'Mobile'
            },
            'en_PP-OCRv4_mobile_rec': {
                'languages': ['en'],
                'accuracy': 70.39,
                'size': '7.5MB',
                'scenario': 'Mobile'
            },
            'latin_PP-OCRv5_mobile_rec': {
                'languages': ['latin'],
                'accuracy': 84.7,
                'size': '14MB',
                'scenario': 'Mobile'
            },
            'korean_PP-OCRv5_mobile_rec': {
                'languages': ['korean', 'en'],
                'accuracy': 'High',
                'size': 'Small',
                'scenario': 'Mobile'
            }
        }
    
    def demonstrate_language_support_overview(self):
        """
        Demonstrate comprehensive language support overview
        Based on Section 3.1: Extensive Multilingual Support
        """
        logger.info("=== Multilingual Support Overview ===")
        logger.info(f"Total supported languages: {len(self.supported_languages)}")
        logger.info("Language categories:")
        
        # Group by script families
        script_families = {}
        for lang_code, info in self.supported_languages.items():
            script = info['script']
            if script not in script_families:
                script_families[script] = []
            script_families[script].append(f"{lang_code} ({info['name']})")
        
        for script, languages in script_families.items():
            logger.info(f"  {script} Script:")
            for lang in languages:
                logger.info(f"    - {lang}")
        
        logger.info(f"\nScript families supported: {len(script_families)}")
    
    def demonstrate_model_zoo_navigation(self):
        """
        Demonstrate model zoo navigation and selection
        Based on Section 3.1: Model Categories for Targeted Selection
        """
        logger.info("=== Model Zoo Navigation Demo ===")
        
        logger.info("Available model categories:")
        for model_name, info in self.model_performance.items():
            logger.info(f"\nModel: {model_name}")
            logger.info(f"  Target scenario: {info['scenario']}")
            logger.info(f"  Supported languages: {info['languages']}")
            logger.info(f"  Accuracy: {info['accuracy']}")
            logger.info(f"  Model size: {info['size']}")
        
        # Demonstrate selection criteria
        logger.info("\n=== Model Selection Guidelines ===")
        logger.info("For high accuracy (server deployment):")
        server_models = [name for name, info in self.model_performance.items() 
                        if info['scenario'] == 'Server']
        for model in server_models:
            logger.info(f"  - {model}")
        
        logger.info("For mobile/edge deployment:")
        mobile_models = [name for name, info in self.model_performance.items() 
                        if info['scenario'] == 'Mobile']
        for model in mobile_models:
            logger.info(f"  - {model}")
    
    def create_multilingual_test_images(self) -> Dict[str, str]:
        """Create test images with different language content"""
        logger.info("Creating multilingual test images...")
        
        test_images = {}
        
        # English test image
        img_en = np.ones((150, 500, 3), dtype=np.uint8) * 255
        cv2.putText(img_en, "Hello World - English", (20, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(img_en, "PaddleOCR Tutorial", (20, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        en_path = self.asset_dir / "test_english.png"
        cv2.imwrite(str(en_path), img_en)
        test_images['en'] = str(en_path)
        
        # Numbers and symbols (universal)
        img_num = np.ones((150, 500, 3), dtype=np.uint8) * 255
        cv2.putText(img_num, "1234567890", (20, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
        cv2.putText(img_num, "ABC-123@#$", (20, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        num_path = self.asset_dir / "test_numbers.png"
        cv2.imwrite(str(num_path), img_num)
        test_images['numbers'] = str(num_path)
        
        # Mixed language content
        img_mixed = np.ones((200, 600, 3), dtype=np.uint8) * 255
        cv2.putText(img_mixed, "English Text Here", (20, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.putText(img_mixed, "Numbers: 123456", (20, 80), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.putText(img_mixed, "Symbols: @#$%^&", (20, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.putText(img_mixed, "Mixed Content Test", (20, 160), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        mixed_path = self.asset_dir / "test_multilingual.png"
        cv2.imwrite(str(mixed_path), img_mixed)
        test_images['mixed'] = str(mixed_path)
        
        logger.info(f"Created {len(test_images)} test images")
        return test_images
    
    def test_language_models(self, test_images: Dict[str, str]):
        """
        Test different language models with sample images
        """
        logger.info("=== Language Model Testing ===")
        
        # Priority languages to test (based on availability and common usage)
        test_languages = [
            ('en', 'English'),
            ('korean', 'Korean'), 
            ('ch', 'Chinese (Simplified)'),
            ('latin', 'Latin Script'),
            ('french', 'French'),
            ('german', 'German')
        ]
        
        results = {}
        
        for lang_code, lang_name in test_languages:
            logger.info(f"\nTesting {lang_name} ({lang_code}):")
            
            try:
                # Test with English image as baseline
                test_result = self._test_single_language(
                    lang_code, test_images['en'], lang_name
                )
                results[lang_code] = test_result
                
            except Exception as e:
                logger.warning(f"Failed to test {lang_name}: {e}")
                results[lang_code] = {
                    'status': 'failed',
                    'error': str(e),
                    'processing_time': 0,
                    'text_count': 0
                }
        
        return results
    
    def _test_single_language(self, lang_code: str, image_path: str, lang_name: str) -> Dict[str, Any]:
        """Test single language model"""
        start_time = time.time()
        
        try:
            # Import PaddleOCR only when needed to avoid initialization issues
            from paddleocr import PaddleOCR
            
            # Initialize OCR for specific language
            logger.info(f"  Initializing {lang_name} model...")
            ocr = PaddleOCR(use_angle_cls=True, lang=lang_code, show_log=False)
            
            # Process image
            logger.info(f"  Processing image with {lang_name} model...")
            result = ocr.ocr(image_path, cls=True)
            
            processing_time = time.time() - start_time
            
            # Analyze results
            text_count = 0
            texts = []
            avg_confidence = 0
            
            if result and result[0]:
                text_count = len(result[0])
                confidences = []
                
                for item in result[0]:
                    if item[1]:
                        text = item[1][0]
                        confidence = item[1][1] if len(item[1]) > 1 else 0
                        texts.append(text)
                        confidences.append(confidence)
                
                avg_confidence = np.mean(confidences) if confidences else 0
            
            logger.info(f"  Results: {text_count} texts found, avg confidence: {avg_confidence:.3f}")
            logger.info(f"  Processing time: {processing_time:.2f}s")
            
            if texts:
                logger.info(f"  Sample texts: {texts[:3]}")  # Show first 3 texts
            
            return {
                'status': 'success',
                'processing_time': processing_time,
                'text_count': text_count,
                'texts': texts,
                'avg_confidence': avg_confidence,
                'model_info': {
                    'language': lang_code,
                    'name': lang_name
                }
            }
            
        except ImportError:
            return {
                'status': 'skipped',
                'error': 'PaddleOCR not available',
                'processing_time': time.time() - start_time,
                'text_count': 0
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'processing_time': time.time() - start_time,
                'text_count': 0
            }
    
    def demonstrate_performance_comparison(self, test_results: Dict[str, Any]):
        """
        Compare performance across different language models
        """
        logger.info("=== Performance Comparison ===")
        
        successful_tests = {k: v for k, v in test_results.items() 
                          if v['status'] == 'success'}
        
        if not successful_tests:
            logger.warning("No successful tests to compare")
            return
        
        logger.info(f"Comparing {len(successful_tests)} successful language models:")
        
        # Sort by processing time
        sorted_by_speed = sorted(successful_tests.items(), 
                               key=lambda x: x[1]['processing_time'])
        
        logger.info("\nSpeed Performance (fastest to slowest):")
        for lang_code, result in sorted_by_speed:
            lang_name = result['model_info']['name']
            time_taken = result['processing_time']
            text_count = result['text_count']
            logger.info(f"  {lang_name}: {time_taken:.2f}s ({text_count} texts)")
        
        # Sort by confidence
        sorted_by_confidence = sorted(successful_tests.items(), 
                                    key=lambda x: x[1]['avg_confidence'], 
                                    reverse=True)
        
        logger.info("\nAccuracy Performance (highest to lowest confidence):")
        for lang_code, result in sorted_by_confidence:
            lang_name = result['model_info']['name']
            confidence = result['avg_confidence']
            logger.info(f"  {lang_name}: {confidence:.3f} avg confidence")
        
        # Calculate performance metrics
        avg_time = np.mean([r['processing_time'] for r in successful_tests.values()])
        avg_confidence = np.mean([r['avg_confidence'] for r in successful_tests.values()])
        
        logger.info(f"\nOverall Performance:")
        logger.info(f"  Average processing time: {avg_time:.2f}s")
        logger.info(f"  Average confidence: {avg_confidence:.3f}")
        logger.info(f"  Success rate: {len(successful_tests)}/{len(test_results)} models")
    
    def demonstrate_language_specific_optimizations(self):
        """
        Demonstrate language-specific optimization strategies
        Based on tutorial Section 3.2: Manual Model Loading
        """
        logger.info("=== Language-Specific Optimization Strategies ===")
        
        optimizations = {
            'korean': {
                'model': 'korean_PP-OCRv5_mobile_rec',
                'features': ['Korean + English support', 'Ultra-lightweight', 'Mobile optimized'],
                'use_cases': ['Mobile apps', 'Real-time processing', 'Edge deployment']
            },
            'english': {
                'model': 'en_PP-OCRv4_mobile_rec',
                'features': ['English + Numeric', 'Compact size', 'Fast processing'],
                'use_cases': ['Document digitization', 'Form processing', 'Receipt scanning']
            },
            'multilingual': {
                'model': 'latin_PP-OCRv5_mobile_rec',
                'features': ['Multiple Latin scripts', 'Balanced performance', 'Good accuracy'],
                'use_cases': ['Multi-language documents', 'International applications']
            },
            'high_accuracy': {
                'model': 'PP-OCRv5_server_rec',
                'features': ['Multi-script support', 'Highest accuracy', 'Server deployment'],
                'use_cases': ['Production systems', 'Critical applications', 'Batch processing']
            }
        }
        
        for scenario, info in optimizations.items():
            logger.info(f"\n{scenario.title()} Optimization:")
            logger.info(f"  Recommended model: {info['model']}")
            logger.info(f"  Key features:")
            for feature in info['features']:
                logger.info(f"    - {feature}")
            logger.info(f"  Best use cases:")
            for use_case in info['use_cases']:
                logger.info(f"    - {use_case}")
    
    def save_multilingual_results(self, test_results: Dict[str, Any]):
        """Save multilingual test results to file"""
        output_file = self.results_dir / f"multilingual_results_{int(time.time())}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("PaddleOCR Multilingual Testing Results\n")
            f.write("=" * 50 + "\n\n")
            
            for lang_code, result in test_results.items():
                lang_name = self.supported_languages.get(lang_code, {}).get('name', lang_code)
                f.write(f"Language: {lang_name} ({lang_code})\n")
                f.write(f"Status: {result['status']}\n")
                f.write(f"Processing Time: {result['processing_time']:.2f}s\n")
                f.write(f"Text Count: {result['text_count']}\n")
                
                if result['status'] == 'success':
                    f.write(f"Average Confidence: {result['avg_confidence']:.3f}\n")
                    if 'texts' in result and result['texts']:
                        f.write("Sample Texts:\n")
                        for i, text in enumerate(result['texts'][:3]):
                            f.write(f"  {i+1}. {text}\n")
                elif result['status'] == 'error':
                    f.write(f"Error: {result['error']}\n")
                
                f.write("\n" + "-" * 30 + "\n\n")
        
        logger.info(f"Results saved to: {output_file}")
    
    def run_all_demos(self):
        """Run all multilingual demonstrations"""
        logger.info("Starting PaddleOCR Multilingual Tutorial Demonstrations")
        logger.info("=" * 60)
        
        try:
            # Overview and model zoo
            self.demonstrate_language_support_overview()
            print("\n" + "=" * 60 + "\n")
            
            self.demonstrate_model_zoo_navigation()
            print("\n" + "=" * 60 + "\n")
            
            # Create test images
            test_images = self.create_multilingual_test_images()
            print("\n" + "=" * 60 + "\n")
            
            # Test language models
            test_results = self.test_language_models(test_images)
            print("\n" + "=" * 60 + "\n")
            
            # Performance comparison
            self.demonstrate_performance_comparison(test_results)
            print("\n" + "=" * 60 + "\n")
            
            # Optimization strategies
            self.demonstrate_language_specific_optimizations()
            print("\n" + "=" * 60 + "\n")
            
            # Save results
            self.save_multilingual_results(test_results)
            
            logger.info("All multilingual demonstrations completed!")
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            raise


def main():
    """Main entry point for multilingual examples"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="PaddleOCR Multilingual Examples from Tutorial Guide"
    )
    parser.add_argument(
        "--demo", 
        choices=["overview", "models", "testing", "performance", "optimization", "all"],
        default="all",
        help="Which demonstration to run"
    )
    
    args = parser.parse_args()
    
    # Initialize demo class
    demo = MultilingualOCRDemo()
    
    try:
        if args.demo == "all":
            demo.run_all_demos()
        elif args.demo == "overview":
            demo.demonstrate_language_support_overview()
        elif args.demo == "models":
            demo.demonstrate_model_zoo_navigation()
        elif args.demo == "testing":
            test_images = demo.create_multilingual_test_images()
            test_results = demo.test_language_models(test_images)
            demo.save_multilingual_results(test_results)
        elif args.demo == "performance":
            test_images = demo.create_multilingual_test_images()
            test_results = demo.test_language_models(test_images)
            demo.demonstrate_performance_comparison(test_results)
        elif args.demo == "optimization":
            demo.demonstrate_language_specific_optimizations()
            
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()