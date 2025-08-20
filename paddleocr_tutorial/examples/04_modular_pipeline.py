#!/usr/bin/env python3
"""
Modular Pipeline Examples - Section 3.2 Implementation

This module demonstrates the modular components of PaddleOCR pipeline
as described in Section 3.2 of the comprehensive tutorial guide.

Key concepts implemented:
- Individual component usage (detection, classification, recognition)
- Pipeline customization and optimization
- Component performance analysis
- Manual model loading and configuration
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

import cv2
import numpy as np
from PIL import Image

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.ocr_engine import EnhancedOCREngine, DocumentResult

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ModularPipelineDemo:
    """
    Modular pipeline demonstration implementing tutorial guide concepts
    """
    
    def __init__(self):
        self.asset_dir = Path(__file__).parent.parent / "assets" / "images"
        self.results_dir = Path(__file__).parent.parent / "assets" / "results"
        
        # Ensure directories exist
        self.asset_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def demonstrate_detection_only(self, image_path: Optional[str] = None):
        """
        Demonstrate text detection without recognition
        Based on Section 3.2: Component Isolation
        """
        logger.info("=== Text Detection Only Demo ===")
        
        if not image_path:
            image_path = self.create_detection_sample()
        
        try:
            # Initialize detection-only pipeline
            from paddleocr import PaddleOCR
            
            logger.info("Initializing detection-only OCR...")
            start_time = time.time()
            
            # Detection only (rec=False disables recognition)
            det_ocr = PaddleOCR(use_angle_cls=True, lang='en', rec=False, show_log=False)
            
            init_time = time.time() - start_time
            logger.info(f"Detection model initialized in {init_time:.2f} seconds")
            
            # Perform detection
            logger.info(f"Processing image: {image_path}")
            detection_start = time.time()
            result = det_ocr.ocr(image_path, cls=True)
            detection_time = time.time() - detection_start
            
            # Analyze detection results
            if result and result[0]:
                logger.info(f"Detection Results:")
                logger.info(f"  Processing time: {detection_time:.2f} seconds")
                logger.info(f"  Text regions found: {len(result[0])}")
                
                # Show bounding box details
                for i, detection in enumerate(result[0]):
                    bbox = detection  # In detection-only mode, result is just bbox
                    area = self._calculate_bbox_area(bbox)
                    logger.info(f"  Region {i+1}: area={area:.0f} pixels, bbox={bbox}")
                
                # Save visualization
                self._visualize_detection_only(image_path, result[0])
                
            else:
                logger.info("No text regions detected")
                
        except ImportError:
            logger.error("PaddleOCR not available for detection-only demo")
        except Exception as e:
            logger.error(f"Detection-only demo failed: {e}")
    
    def demonstrate_recognition_only(self, image_path: Optional[str] = None):
        """
        Demonstrate text recognition on pre-segmented text
        Based on Section 3.2: Recognition Component
        """
        logger.info("=== Text Recognition Only Demo ===")
        
        if not image_path:
            image_path = self.create_recognition_samples()
        
        try:
            # Initialize recognition-only pipeline
            from paddleocr import PaddleOCR
            
            logger.info("Initializing recognition-only OCR...")
            start_time = time.time()
            
            # Recognition only (det=False disables detection)
            rec_ocr = PaddleOCR(use_angle_cls=False, lang='en', det=False, show_log=False)
            
            init_time = time.time() - start_time
            logger.info(f"Recognition model initialized in {init_time:.2f} seconds")
            
            # Test with multiple cropped text samples
            if isinstance(image_path, list):
                sample_paths = image_path
            else:
                sample_paths = [image_path]
            
            for i, sample_path in enumerate(sample_paths):
                logger.info(f"\nTesting sample {i+1}: {Path(sample_path).name}")
                
                recognition_start = time.time()
                result = rec_ocr.ocr(sample_path, cls=False)
                recognition_time = time.time() - recognition_start
                
                if result and result[0] and result[0][0]:
                    text_info = result[0][0][1]
                    text = text_info[0] if text_info else ""
                    confidence = text_info[1] if len(text_info) > 1 else 0.0
                    
                    logger.info(f"  Recognition result: '{text}'")
                    logger.info(f"  Confidence: {confidence:.3f}")
                    logger.info(f"  Processing time: {recognition_time:.3f}s")
                else:
                    logger.info("  No text recognized")
                
        except ImportError:
            logger.error("PaddleOCR not available for recognition-only demo")
        except Exception as e:
            logger.error(f"Recognition-only demo failed: {e}")
    
    def demonstrate_angle_classification(self, image_path: Optional[str] = None):
        """
        Demonstrate text angle classification
        Based on Section 3.2: Orientation Classification
        """
        logger.info("=== Text Angle Classification Demo ===")
        
        if not image_path:
            image_path = self.create_rotated_samples()
        
        try:
            from paddleocr import PaddleOCR
            
            # Test with and without angle classification
            configs = [
                ("With Angle Classification", True),
                ("Without Angle Classification", False)
            ]
            
            for config_name, use_angle_cls in configs:
                logger.info(f"\n{config_name}:")
                
                start_time = time.time()
                ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang='en', show_log=False)
                init_time = time.time() - start_time
                
                logger.info(f"  Initialization time: {init_time:.2f}s")
                
                if isinstance(image_path, list):
                    sample_paths = image_path
                else:
                    sample_paths = [image_path]
                
                for sample_path in sample_paths:
                    process_start = time.time()
                    result = ocr.ocr(sample_path, cls=use_angle_cls)
                    process_time = time.time() - process_start
                    
                    if result and result[0]:
                        text_count = len(result[0])
                        total_confidence = sum([
                            item[1][1] for item in result[0] 
                            if item[1] and len(item[1]) > 1
                        ])
                        avg_confidence = total_confidence / max(text_count, 1)
                        
                        logger.info(f"  {Path(sample_path).name}: {text_count} texts, "
                                  f"avg confidence: {avg_confidence:.3f}, time: {process_time:.2f}s")
                    else:
                        logger.info(f"  {Path(sample_path).name}: No text detected")
                
        except ImportError:
            logger.error("PaddleOCR not available for angle classification demo")
        except Exception as e:
            logger.error(f"Angle classification demo failed: {e}")
    
    def demonstrate_custom_pipeline(self, image_path: Optional[str] = None):
        """
        Demonstrate custom pipeline configuration
        Based on Section 3.2: Manual Model Loading
        """
        logger.info("=== Custom Pipeline Configuration Demo ===")
        
        if not image_path:
            image_path = self.create_pipeline_sample()
        
        try:
            from paddleocr import PaddleOCR
            
            # Different pipeline configurations
            pipeline_configs = [
                {
                    "name": "High Accuracy Server",
                    "config": {
                        "use_angle_cls": True,
                        "lang": "en",
                        "det_model_dir": None,  # Use default
                        "rec_model_dir": None,  # Use default
                        "use_gpu": False
                    }
                },
                {
                    "name": "Fast Mobile",
                    "config": {
                        "use_angle_cls": False,  # Faster without angle classification
                        "lang": "en",
                        "use_gpu": False
                    }
                },
                {
                    "name": "Detection Focused",
                    "config": {
                        "use_angle_cls": True,
                        "lang": "en",
                        "rec": False,  # Detection only
                        "use_gpu": False
                    }
                }
            ]
            
            results = {}
            
            for pipeline_config in pipeline_configs:
                name = pipeline_config["name"]
                config = pipeline_config["config"]
                
                logger.info(f"\nTesting {name} Pipeline:")
                logger.info(f"  Configuration: {config}")
                
                try:
                    start_time = time.time()
                    ocr = PaddleOCR(show_log=False, **config)
                    init_time = time.time() - start_time
                    
                    process_start = time.time()
                    result = ocr.ocr(image_path, cls=config.get('use_angle_cls', True))
                    process_time = time.time() - process_start
                    
                    # Analyze results
                    text_count = 0
                    avg_confidence = 0
                    
                    if result and result[0]:
                        if config.get('rec', True):  # Full pipeline
                            text_count = len(result[0])
                            confidences = [
                                item[1][1] for item in result[0] 
                                if item[1] and len(item[1]) > 1
                            ]
                            avg_confidence = np.mean(confidences) if confidences else 0
                        else:  # Detection only
                            text_count = len(result[0])
                            avg_confidence = -1  # N/A for detection only
                    
                    results[name] = {
                        'init_time': init_time,
                        'process_time': process_time,
                        'text_count': text_count,
                        'avg_confidence': avg_confidence,
                        'total_time': init_time + process_time
                    }
                    
                    logger.info(f"  Results: {text_count} regions, "
                              f"init: {init_time:.2f}s, process: {process_time:.2f}s")
                    if avg_confidence >= 0:
                        logger.info(f"  Average confidence: {avg_confidence:.3f}")
                    
                except Exception as e:
                    logger.error(f"  {name} pipeline failed: {e}")
                    results[name] = {'error': str(e)}
            
            # Compare pipeline performance
            self._compare_pipeline_performance(results)
                
        except ImportError:
            logger.error("PaddleOCR not available for custom pipeline demo")
        except Exception as e:
            logger.error(f"Custom pipeline demo failed: {e}")
    
    def demonstrate_performance_analysis(self):
        """
        Demonstrate component performance analysis
        """
        logger.info("=== Pipeline Performance Analysis ===")
        
        # Create test images
        test_images = []
        for i in range(3):
            img_path = self.create_performance_test_image(f"Performance test {i+1}")
            test_images.append(img_path)
        
        try:
            from paddleocr import PaddleOCR
            
            # Test different component combinations
            component_tests = [
                ("Full Pipeline", {"use_angle_cls": True, "det": True, "rec": True}),
                ("Detection + Recognition", {"use_angle_cls": False, "det": True, "rec": True}),
                ("Detection Only", {"use_angle_cls": True, "det": True, "rec": False}),
            ]
            
            performance_data = {}
            
            for test_name, config in component_tests:
                logger.info(f"\nTesting {test_name}:")
                
                total_times = []
                init_times = []
                
                for img_path in test_images:
                    try:
                        # Initialize OCR
                        init_start = time.time()
                        ocr = PaddleOCR(lang='en', show_log=False, **config)
                        init_time = time.time() - init_start
                        init_times.append(init_time)
                        
                        # Process image
                        process_start = time.time()
                        result = ocr.ocr(img_path, cls=config.get('use_angle_cls', True))
                        process_time = time.time() - process_start
                        
                        total_time = init_time + process_time
                        total_times.append(total_time)
                        
                        # Count results
                        result_count = len(result[0]) if result and result[0] else 0
                        
                        logger.info(f"  {Path(img_path).name}: {result_count} regions, "
                                  f"total: {total_time:.2f}s")
                        
                    except Exception as e:
                        logger.error(f"  Failed processing {img_path}: {e}")
                
                # Calculate averages
                if total_times:
                    performance_data[test_name] = {
                        'avg_total_time': np.mean(total_times),
                        'avg_init_time': np.mean(init_times),
                        'avg_process_time': np.mean(total_times) - np.mean(init_times),
                        'std_total_time': np.std(total_times)
                    }
            
            # Display performance comparison
            self._display_performance_analysis(performance_data)
            
        except ImportError:
            logger.error("PaddleOCR not available for performance analysis")
        except Exception as e:
            logger.error(f"Performance analysis failed: {e}")
    
    def _calculate_bbox_area(self, bbox: List[List[float]]) -> float:
        """Calculate area of bounding box"""
        if len(bbox) != 4:
            return 0.0
        
        # Convert to numpy array for easier calculation
        points = np.array(bbox)
        
        # Calculate area using shoelace formula
        x = points[:, 0]
        y = points[:, 1]
        return 0.5 * abs(sum(x[i] * y[i + 1] - x[i + 1] * y[i] for i in range(-1, len(x) - 1)))
    
    def _visualize_detection_only(self, image_path: str, detections: List):
        """Create visualization for detection-only results"""
        img = cv2.imread(image_path)
        
        for i, detection in enumerate(detections):
            bbox = detection
            pts = np.array(bbox, np.int32)
            
            # Draw bounding box
            cv2.polylines(img, [pts], True, (0, 255, 0), 2)
            
            # Add region number
            cv2.putText(img, f"R{i+1}", (int(bbox[0][0]), int(bbox[0][1]) - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Save visualization
        output_path = self.results_dir / f"detection_only_{int(time.time())}.png"
        cv2.imwrite(str(output_path), img)
        logger.info(f"Detection visualization saved: {output_path}")
    
    def _compare_pipeline_performance(self, results: Dict[str, Dict]):
        """Compare performance across different pipeline configurations"""
        logger.info("\n=== Pipeline Performance Comparison ===")
        
        valid_results = {k: v for k, v in results.items() if 'error' not in v}
        
        if not valid_results:
            logger.warning("No valid results to compare")
            return
        
        # Sort by total time
        sorted_by_speed = sorted(valid_results.items(), key=lambda x: x[1]['total_time'])
        
        logger.info("Speed Ranking (fastest to slowest):")
        for i, (name, data) in enumerate(sorted_by_speed):
            logger.info(f"  {i+1}. {name}: {data['total_time']:.2f}s total "
                      f"({data['init_time']:.2f}s init + {data['process_time']:.2f}s process)")
        
        # Sort by accuracy (if available)
        accuracy_results = {k: v for k, v in valid_results.items() if v['avg_confidence'] >= 0}
        if accuracy_results:
            sorted_by_accuracy = sorted(accuracy_results.items(), 
                                      key=lambda x: x[1]['avg_confidence'], reverse=True)
            
            logger.info("\nAccuracy Ranking (highest to lowest confidence):")
            for i, (name, data) in enumerate(sorted_by_accuracy):
                logger.info(f"  {i+1}. {name}: {data['avg_confidence']:.3f} confidence")
    
    def _display_performance_analysis(self, performance_data: Dict[str, Dict]):
        """Display detailed performance analysis"""
        logger.info("\n=== Detailed Performance Analysis ===")
        
        for test_name, data in performance_data.items():
            logger.info(f"\n{test_name}:")
            logger.info(f"  Average total time: {data['avg_total_time']:.2f}s ± {data['std_total_time']:.2f}s")
            logger.info(f"  Average init time: {data['avg_init_time']:.2f}s")
            logger.info(f"  Average process time: {data['avg_process_time']:.2f}s")
            logger.info(f"  Init/Process ratio: {data['avg_init_time']/data['avg_process_time']:.1f}:1")
    
    def create_detection_sample(self) -> str:
        """Create sample image optimized for detection testing"""
        img = np.ones((300, 600, 3), dtype=np.uint8) * 255
        
        # Add various text regions with different sizes and orientations
        texts = [
            ("LARGE TITLE TEXT", 50, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 2),
            ("Medium subtitle here", 120, cv2.FONT_HERSHEY_COMPLEX, 1.0, 2),
            ("Small details text", 180, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1),
            ("Numbers: 123456", 220, cv2.FONT_HERSHEY_DUPLEX, 0.8, 1),
            ("Mixed: ABC123!@#", 260, cv2.FONT_HERSHEY_TRIPLEX, 0.9, 2)
        ]
        
        for text, y, font, scale, thickness in texts:
            cv2.putText(img, text, (50, y), font, scale, (0, 0, 0), thickness)
        
        # Add some geometric shapes for detection challenges
        cv2.rectangle(img, (450, 50), (580, 100), (128, 128, 128), 2)
        cv2.circle(img, (520, 200), 30, (64, 64, 64), 2)
        
        sample_path = self.asset_dir / "detection_sample.png"
        cv2.imwrite(str(sample_path), img)
        logger.info(f"Created detection sample: {sample_path}")
        return str(sample_path)
    
    def create_recognition_samples(self) -> List[str]:
        """Create cropped text samples for recognition testing"""
        samples = []
        
        texts = [
            "Hello World",
            "PaddleOCR",
            "Tutorial Guide",
            "123456789",
            "Mixed Text 123"
        ]
        
        for i, text in enumerate(texts):
            img = np.ones((60, 200, 3), dtype=np.uint8) * 255
            cv2.putText(img, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            sample_path = self.asset_dir / f"recognition_sample_{i+1}.png"
            cv2.imwrite(str(sample_path), img)
            samples.append(str(sample_path))
        
        logger.info(f"Created {len(samples)} recognition samples")
        return samples
    
    def create_rotated_samples(self) -> List[str]:
        """Create rotated text samples for angle classification testing"""
        samples = []
        angles = [0, 90, 180, 270]
        
        for angle in angles:
            # Create base image
            img = np.ones((200, 300, 3), dtype=np.uint8) * 255
            cv2.putText(img, f"Rotated {angle}°", (50, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            # Rotate image
            if angle != 0:
                center = (img.shape[1] // 2, img.shape[0] // 2)
                rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
                img = cv2.warpAffine(img, rotation_matrix, (img.shape[1], img.shape[0]), 
                                   fillValue=(255, 255, 255))
            
            sample_path = self.asset_dir / f"rotated_sample_{angle}.png"
            cv2.imwrite(str(sample_path), img)
            samples.append(str(sample_path))
        
        logger.info(f"Created {len(samples)} rotated samples")
        return samples
    
    def create_pipeline_sample(self) -> str:
        """Create comprehensive sample for pipeline testing"""
        img = np.ones((400, 700, 3), dtype=np.uint8) * 255
        
        # Title
        cv2.putText(img, "Modular Pipeline Test", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 2)
        
        # Various text types
        texts = [
            ("Section 3.2: Manual Model Loading", 100),
            ("High-confidence text sample", 150),
            ("Medium quality text here", 200),
            ("Small font text", 250),
            ("Numbers and symbols: 123!@#", 300),
            ("Final line for testing", 350)
        ]
        
        for text, y in texts:
            cv2.putText(img, text, (50, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1)
        
        sample_path = self.asset_dir / "pipeline_sample.png"
        cv2.imwrite(str(sample_path), img)
        logger.info(f"Created pipeline sample: {sample_path}")
        return str(sample_path)
    
    def create_performance_test_image(self, text: str) -> str:
        """Create performance test image"""
        img = np.ones((200, 500, 3), dtype=np.uint8) * 255
        cv2.putText(img, text, (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(img, f"Timestamp: {int(time.time())}", (30, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        
        filename = f"perf_test_{text.replace(' ', '_').lower()}_{int(time.time())}.png"
        img_path = self.asset_dir / filename
        cv2.imwrite(str(img_path), img)
        return str(img_path)
    
    def run_all_demos(self, image_path: Optional[str] = None):
        """Run all modular pipeline demonstrations"""
        logger.info("Starting PaddleOCR Modular Pipeline Tutorial Demonstrations")
        logger.info("=" * 60)
        
        try:
            self.demonstrate_detection_only(image_path)
            print("\n" + "=" * 60 + "\n")
            
            self.demonstrate_recognition_only(image_path)
            print("\n" + "=" * 60 + "\n")
            
            self.demonstrate_angle_classification(image_path)
            print("\n" + "=" * 60 + "\n")
            
            self.demonstrate_custom_pipeline(image_path)
            print("\n" + "=" * 60 + "\n")
            
            self.demonstrate_performance_analysis()
            print("\n" + "=" * 60 + "\n")
            
            logger.info("All modular pipeline demonstrations completed!")
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            raise


def main():
    """Main entry point for modular pipeline examples"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="PaddleOCR Modular Pipeline Examples from Tutorial Guide"
    )
    parser.add_argument(
        "--image", 
        type=str, 
        help="Path to image file (optional, will create samples if not provided)"
    )
    parser.add_argument(
        "--demo", 
        choices=["detection", "recognition", "angle", "pipeline", "performance", "all"],
        default="all",
        help="Which demonstration to run"
    )
    
    args = parser.parse_args()
    
    # Initialize demo class
    demo = ModularPipelineDemo()
    
    try:
        if args.demo == "all":
            demo.run_all_demos(args.image)
        elif args.demo == "detection":
            demo.demonstrate_detection_only(args.image)
        elif args.demo == "recognition":
            demo.demonstrate_recognition_only(args.image)
        elif args.demo == "angle":
            demo.demonstrate_angle_classification(args.image)
        elif args.demo == "pipeline":
            demo.demonstrate_custom_pipeline(args.image)
        elif args.demo == "performance":
            demo.demonstrate_performance_analysis()
            
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()