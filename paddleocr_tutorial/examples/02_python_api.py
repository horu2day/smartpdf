#!/usr/bin/env python3
"""
Python API Examples - Section 2.4 Implementation

This module demonstrates the PaddleOCR Python API usage patterns
as described in Section 2.4 of the comprehensive tutorial guide.

Key concepts implemented:
- PaddleOCR class initialization
- OCR method usage with structured output
- Result visualization with draw_ocr
- Error handling and performance monitoring
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.ocr_engine import EnhancedOCREngine, DocumentResult

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PaddleOCRAPIDemo:
    """
    Python API demonstration class implementing tutorial guide examples
    """
    
    def __init__(self):
        self.asset_dir = Path(__file__).parent.parent / "assets" / "images"
        self.results_dir = Path(__file__).parent.parent / "assets" / "results"
        
        # Ensure directories exist
        self.asset_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def demonstrate_basic_initialization(self):
        """
        Demonstrate PaddleOCR initialization patterns
        Based on Section 2.4: Initialization
        """
        logger.info("=== PaddleOCR Initialization Demo ===")
        
        # Example 1: Basic English initialization
        logger.info("Example 1: Basic English OCR initialization")
        try:
            start_time = time.time()
            
            # Using our enhanced engine (which wraps PaddleOCR)
            ocr_en = EnhancedOCREngine(
                lang='en', 
                use_angle_cls=True,
                model_type='mobile'
            )
            
            init_time = time.time() - start_time
            logger.info(f"English OCR initialized in {init_time:.2f} seconds")
            logger.info(f"Available languages: {ocr_en.get_available_languages()[:5]}...")  # Show first 5
            
        except Exception as e:
            logger.error(f"English OCR initialization failed: {e}")
        
        # Example 2: Korean initialization with GPU (if available)
        logger.info("Example 2: Korean OCR with GPU acceleration")
        try:
            start_time = time.time()
            
            ocr_kr = EnhancedOCREngine(
                lang='korean',
                use_angle_cls=True,
                use_gpu=False,  # Set to True if GPU available
                model_type='mobile'
            )
            
            init_time = time.time() - start_time
            logger.info(f"Korean OCR initialized in {init_time:.2f} seconds")
            
        except Exception as e:
            logger.error(f"Korean OCR initialization failed: {e}")
    
    def demonstrate_basic_ocr(self, image_path: Optional[str] = None):
        """
        Demonstrate basic OCR processing
        Based on Section 2.4: Performing OCR
        """
        logger.info("=== Basic OCR Processing Demo ===")
        
        if not image_path:
            image_path = self.create_comprehensive_sample()
        
        try:
            # Initialize OCR engine
            ocr_engine = EnhancedOCREngine(lang='en', use_angle_cls=True)
            
            # Perform OCR
            logger.info(f"Processing image: {image_path}")
            result = ocr_engine.process_image(image_path)
            
            # Display results
            logger.info(f"OCR Results:")
            logger.info(f"Image: {result.image_path}")
            logger.info(f"Processing time: {result.processing_time:.2f} seconds")
            logger.info(f"Total text regions found: {result.total_texts}")
            logger.info(f"Model info: {result.model_info}")
            
            # Show detailed results
            for i, ocr_result in enumerate(result.results):
                logger.info(f"Text {i+1}:")
                logger.info(f"  Content: '{ocr_result.text}'")
                logger.info(f"  Confidence: {ocr_result.confidence:.3f}")
                logger.info(f"  Bounding box: {ocr_result.bbox}")
            
            return result
            
        except Exception as e:
            logger.error(f"OCR processing failed: {e}")
            return None
    
    def demonstrate_output_structure(self, image_path: Optional[str] = None):
        """
        Demonstrate understanding of OCR output structure
        Based on Section 2.4: Understanding the Output Structure
        """
        logger.info("=== Output Structure Analysis Demo ===")
        
        if not image_path:
            image_path = self.create_comprehensive_sample()
        
        try:
            # Use direct PaddleOCR to show raw output format
            from paddleocr import PaddleOCR
            
            ocr = PaddleOCR(use_angle_cls=True, lang='en')
            raw_result = ocr.ocr(image_path, cls=True)
            
            logger.info("Raw PaddleOCR output structure:")
            logger.info(f"Type: {type(raw_result)}")
            logger.info(f"Length: {len(raw_result) if raw_result else 0}")
            
            if raw_result and raw_result[0]:
                logger.info(f"First page results count: {len(raw_result[0])}")
                
                # Analyze first result in detail
                if raw_result[0]:
                    first_result = raw_result[0][0]
                    logger.info(f"First result structure:")
                    logger.info(f"  Type: {type(first_result)}")
                    logger.info(f"  Length: {len(first_result)}")
                    logger.info(f"  Bounding box: {first_result[0]}")
                    logger.info(f"  Text info: {first_result[1]}")
                    
                    # Extract components
                    bbox = first_result[0]
                    text_info = first_result[1]
                    text = text_info[0] if text_info else ""
                    confidence = text_info[1] if len(text_info) > 1 else 0.0
                    
                    logger.info(f"Extracted components:")
                    logger.info(f"  Text: '{text}'")
                    logger.info(f"  Confidence: {confidence}")
                    logger.info(f"  Bounding box points: {len(bbox)} points")
                    
                    # Show bounding box coordinates
                    for i, point in enumerate(bbox):
                        logger.info(f"    Point {i+1}: x={point[0]}, y={point[1]}")
            
        except Exception as e:
            logger.error(f"Output structure analysis failed: {e}")
    
    def demonstrate_visualization(self, image_path: Optional[str] = None):
        """
        Demonstrate result visualization
        Based on Section 2.4: Visualization
        """
        logger.info("=== Result Visualization Demo ===")
        
        if not image_path:
            image_path = self.create_comprehensive_sample()
        
        try:
            # Process with enhanced engine
            ocr_engine = EnhancedOCREngine(lang='en', use_angle_cls=True)
            result = ocr_engine.process_image(image_path)
            
            # Create visualization
            self.create_advanced_visualization(image_path, result)
            logger.info("Visualization saved to results directory")
            
        except Exception as e:
            logger.error(f"Visualization failed: {e}")
    
    def create_advanced_visualization(self, image_path: str, result: DocumentResult):
        """Create advanced visualization of OCR results"""
        # Load original image
        original_image = cv2.imread(image_path)
        vis_image = original_image.copy()
        
        # Colors for different confidence levels
        colors = {
            'high': (0, 255, 0),    # Green for high confidence (>0.8)
            'medium': (0, 165, 255), # Orange for medium confidence (0.5-0.8)
            'low': (0, 0, 255)      # Red for low confidence (<0.5)
        }
        
        # Draw bounding boxes and text
        for i, ocr_result in enumerate(result.results):
            # Determine color based on confidence
            if ocr_result.confidence > 0.8:
                color = colors['high']
            elif ocr_result.confidence > 0.5:
                color = colors['medium']
            else:
                color = colors['low']
            
            # Draw bounding box
            bbox = ocr_result.bbox
            pts = np.array(bbox, np.int32)
            cv2.polylines(vis_image, [pts], True, color, 2)
            
            # Add text label
            text_label = f"{ocr_result.text} ({ocr_result.confidence:.2f})"
            text_position = (int(bbox[0][0]), int(bbox[0][1]) - 10)
            
            cv2.putText(vis_image, text_label, text_position,
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Save visualization
        output_path = self.results_dir / f"visualization_{int(time.time())}.png"
        cv2.imwrite(str(output_path), vis_image)
        
        # Create side-by-side comparison
        self.create_comparison_plot(original_image, vis_image, result, output_path)
    
    def create_comparison_plot(self, original: np.ndarray, annotated: np.ndarray, 
                              result: DocumentResult, output_path: Path):
        """Create side-by-side comparison plot"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 8))
        
        # Convert BGR to RGB for matplotlib
        original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        
        # Plot original image
        axes[0].imshow(original_rgb)
        axes[0].set_title("Original Image")
        axes[0].axis('off')
        
        # Plot annotated image
        axes[1].imshow(annotated_rgb)
        axes[1].set_title(f"OCR Results ({result.total_texts} texts found)")
        axes[1].axis('off')
        
        # Add summary text
        summary_text = f"""Processing Time: {result.processing_time:.2f}s
Model: {result.model_info.get('language', 'unknown')} - {result.model_info.get('model_type', 'unknown')}
Total Texts: {result.total_texts}
Avg Confidence: {np.mean([r.confidence for r in result.results]):.3f}"""
        
        plt.figtext(0.5, 0.02, summary_text, ha='center', fontsize=10,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
        
        plt.tight_layout()
        
        # Save comparison plot
        comparison_path = output_path.parent / f"comparison_{output_path.stem}.png"
        plt.savefig(comparison_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Comparison plot saved: {comparison_path}")
    
    def demonstrate_performance_monitoring(self):
        """Demonstrate performance monitoring capabilities"""
        logger.info("=== Performance Monitoring Demo ===")
        
        # Create test images
        test_images = []
        for i in range(3):
            img_path = self.create_test_image(f"Test image {i+1}")
            test_images.append(img_path)
        
        try:
            # Initialize engine with performance tracking
            ocr_engine = EnhancedOCREngine(lang='en', use_angle_cls=True)
            
            # Process multiple images
            results = []
            for img_path in test_images:
                result = ocr_engine.process_image(img_path)
                results.append(result)
            
            # Get performance statistics
            stats = ocr_engine.get_performance_stats()
            
            logger.info("Performance Statistics:")
            logger.info(f"Total processed: {stats['total_processed']}")
            logger.info(f"Total time: {stats['total_time']:.2f}s")
            logger.info(f"Average processing time: {stats['avg_processing_time']:.2f}s")
            logger.info(f"Success rate: {stats['success_rate']:.1f}%")
            logger.info(f"Configuration: {stats['configuration']}")
            
            # Save detailed results
            output_file = ocr_engine.save_results(results, self.results_dir, 'json')
            logger.info(f"Detailed results saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Performance monitoring failed: {e}")
    
    def create_comprehensive_sample(self) -> str:
        """Create a comprehensive sample image with various text types"""
        # Create a larger image with different text styles
        img = np.ones((400, 800, 3), dtype=np.uint8) * 255
        
        # Add title
        cv2.putText(img, "PaddleOCR Python API Demo", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
        
        # Add various text samples
        texts = [
            ("Section 2.4: API Examples", 80, cv2.FONT_HERSHEY_SIMPLEX, 0.8),
            ("High confidence text here", 120, cv2.FONT_HERSHEY_COMPLEX, 0.7),
            ("Medium quality sample", 160, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.9),
            ("Small text example", 200, cv2.FONT_HERSHEY_SIMPLEX, 0.5),
            ("UPPERCASE BOLD TEXT", 240, cv2.FONT_HERSHEY_SIMPLEX, 0.8),
            ("Numbers: 123456789", 280, cv2.FONT_HERSHEY_DUPLEX, 0.6),
            ("Mixed: Text123 & Symbols!", 320, cv2.FONT_HERSHEY_TRIPLEX, 0.7),
            ("Tutorial Guide Implementation", 360, cv2.FONT_HERSHEY_SIMPLEX, 0.8)
        ]
        
        for text, y, font, scale in texts:
            cv2.putText(img, text, (50, y), font, scale, (0, 0, 0), 1)
        
        # Add some geometric shapes for detection challenges
        cv2.rectangle(img, (650, 50), (750, 150), (100, 100, 100), 2)
        cv2.circle(img, (700, 250), 50, (150, 150, 150), 2)
        
        # Save sample image
        sample_path = self.asset_dir / "comprehensive_sample.png"
        cv2.imwrite(str(sample_path), img)
        
        logger.info(f"Created comprehensive sample: {sample_path}")
        return str(sample_path)
    
    def create_test_image(self, text: str) -> str:
        """Create a simple test image with specified text"""
        img = np.ones((150, 400, 3), dtype=np.uint8) * 255
        cv2.putText(img, text, (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Create unique filename
        filename = f"test_{text.replace(' ', '_').lower()}_{int(time.time())}.png"
        img_path = self.asset_dir / filename
        cv2.imwrite(str(img_path), img)
        
        return str(img_path)
    
    def run_all_demos(self, image_path: Optional[str] = None):
        """Run all Python API demonstrations"""
        logger.info("Starting PaddleOCR Python API Tutorial Demonstrations")
        logger.info("=" * 60)
        
        try:
            self.demonstrate_basic_initialization()
            print("\n" + "=" * 60 + "\n")
            
            self.demonstrate_basic_ocr(image_path)
            print("\n" + "=" * 60 + "\n")
            
            self.demonstrate_output_structure(image_path)
            print("\n" + "=" * 60 + "\n")
            
            self.demonstrate_visualization(image_path)
            print("\n" + "=" * 60 + "\n")
            
            self.demonstrate_performance_monitoring()
            print("\n" + "=" * 60 + "\n")
            
            logger.info("All Python API demonstrations completed!")
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            raise


def main():
    """Main entry point for Python API examples"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="PaddleOCR Python API Examples from Tutorial Guide"
    )
    parser.add_argument(
        "--image", 
        type=str, 
        help="Path to image file (optional, will create sample if not provided)"
    )
    parser.add_argument(
        "--demo", 
        choices=["init", "basic", "structure", "viz", "performance", "all"],
        default="all",
        help="Which demonstration to run"
    )
    
    args = parser.parse_args()
    
    # Initialize demo class
    demo = PaddleOCRAPIDemo()
    
    try:
        if args.demo == "all":
            demo.run_all_demos(args.image)
        elif args.demo == "init":
            demo.demonstrate_basic_initialization()
        elif args.demo == "basic":
            demo.demonstrate_basic_ocr(args.image)
        elif args.demo == "structure":
            demo.demonstrate_output_structure(args.image)
        elif args.demo == "viz":
            demo.demonstrate_visualization(args.image)
        elif args.demo == "performance":
            demo.demonstrate_performance_monitoring()
            
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()