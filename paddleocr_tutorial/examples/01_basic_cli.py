#!/usr/bin/env python3
"""
Basic CLI Examples - Section 2.3 Implementation

This module demonstrates the PaddleOCR command-line interface usage patterns
as described in Section 2.3 of the comprehensive tutorial guide.

Key concepts implemented:
- Full pipeline inference
- Component-specific inference
- Model version selection
- Language configuration
"""

import os
import sys
import subprocess
import argparse
import logging
from pathlib import Path
from typing import List, Optional

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.ocr_engine import EnhancedOCREngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PaddleOCRCLIDemo:
    """
    CLI demonstration class implementing tutorial guide examples
    """
    
    def __init__(self):
        self.asset_dir = Path(__file__).parent.parent / "assets" / "images"
        self.results_dir = Path(__file__).parent.parent / "assets" / "results"
        
        # Ensure directories exist
        self.asset_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def demonstrate_full_pipeline(self, image_path: Optional[str] = None):
        """
        Demonstrate full OCR pipeline using CLI
        Based on Section 2.3: Full Pipeline Inference
        """
        logger.info("=== Full Pipeline Inference Demo ===")
        
        if not image_path:
            # Create a sample image if none provided
            image_path = self.create_sample_image()
        
        # Example 1: Basic English OCR with angle classification
        logger.info("Example 1: Basic English OCR")
        cmd = [
            "paddleocr", 
            "--image_dir", str(image_path),
            "--lang", "en",
            "--use_angle_cls", "true"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                logger.info("CLI Output:")
                logger.info(result.stdout)
            else:
                logger.error(f"CLI Error: {result.stderr}")
        except subprocess.TimeoutExpired:
            logger.error("CLI command timed out")
        except FileNotFoundError:
            logger.warning("paddleocr CLI not found, using Python API instead")
            self._fallback_to_api(image_path, "en")
    
    def demonstrate_component_specific(self, image_path: Optional[str] = None):
        """
        Demonstrate component-specific inference
        Based on Section 2.3: Component-Specific Inference
        """
        logger.info("=== Component-Specific Inference Demo ===")
        
        if not image_path:
            image_path = self.create_sample_image()
        
        # Example 1: Detection only (recognition disabled)
        logger.info("Example 1: Text Detection Only")
        cmd = [
            "paddleocr",
            "--image_dir", str(image_path),
            "--rec", "false"  # Disable recognition
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                logger.info("Detection-only output:")
                logger.info(result.stdout)
            else:
                logger.error(f"Detection CLI Error: {result.stderr}")
        except subprocess.TimeoutExpired:
            logger.error("Detection CLI command timed out")
        except FileNotFoundError:
            logger.warning("paddleocr CLI not found, using Python API instead")
            self._fallback_detection_only(image_path)
        
        # Example 2: Recognition only (detection disabled)
        logger.info("Example 2: Text Recognition Only")
        # Note: This would require pre-cropped text images
        logger.info("Recognition-only requires pre-cropped text images")
        
    def demonstrate_model_versions(self, image_path: Optional[str] = None):
        """
        Demonstrate model version selection
        Based on Section 2.3: Model Version Selection
        """
        logger.info("=== Model Version Selection Demo ===")
        
        if not image_path:
            image_path = self.create_sample_image()
        
        # Example: Using different PP-OCR versions
        versions = ["PP-OCRv3", "PP-OCRv4"]
        
        for version in versions:
            logger.info(f"Testing {version}")
            cmd = [
                "paddleocr",
                "--image_dir", str(image_path),
                "--ocr_version", version,
                "--lang", "en"
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    logger.info(f"{version} output:")
                    logger.info(result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
                else:
                    logger.error(f"{version} CLI Error: {result.stderr}")
            except subprocess.TimeoutExpired:
                logger.error(f"{version} CLI command timed out")
            except FileNotFoundError:
                logger.warning("paddleocr CLI not found, using Python API instead")
                self._fallback_to_api(image_path, "en", version)
    
    def demonstrate_multilingual_cli(self):
        """
        Demonstrate multilingual OCR via CLI
        Based on Section 3.1: Multilingual Support
        """
        logger.info("=== Multilingual CLI Demo ===")
        
        # Create sample images for different languages
        image_path = self.create_sample_image()
        
        # Languages to test (based on tutorial Section 3.1)
        languages = [
            ("en", "English"),
            ("korean", "Korean"),
            ("ch", "Chinese"),
            ("japanese", "Japanese"),
            ("french", "French"),
            ("german", "German")
        ]
        
        for lang_code, lang_name in languages:
            logger.info(f"Testing {lang_name} ({lang_code})")
            cmd = [
                "paddleocr",
                "--image_dir", str(image_path),
                "--lang", lang_code,
                "--use_angle_cls", "true"
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    logger.info(f"{lang_name} OCR successful")
                    # Log first 100 characters to avoid flooding
                    output_preview = result.stdout[:100] + "..." if len(result.stdout) > 100 else result.stdout
                    logger.info(f"Output preview: {output_preview}")
                else:
                    logger.warning(f"{lang_name} CLI had issues: {result.stderr}")
            except subprocess.TimeoutExpired:
                logger.error(f"{lang_name} CLI command timed out")
            except FileNotFoundError:
                logger.warning("paddleocr CLI not found, using Python API instead")
                self._fallback_to_api(image_path, lang_code)
    
    def create_sample_image(self) -> str:
        """Create a sample image with text for testing"""
        import numpy as np
        import cv2
        
        # Create a simple text image
        img = np.ones((200, 600, 3), dtype=np.uint8) * 255
        
        # Add some text
        cv2.putText(img, "PaddleOCR Tutorial", (50, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(img, "Comprehensive Guide", (50, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(img, "CLI Examples Demo", (50, 180), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Save sample image
        sample_path = self.asset_dir / "sample_text.png"
        cv2.imwrite(str(sample_path), img)
        
        logger.info(f"Created sample image: {sample_path}")
        return str(sample_path)
    
    def _fallback_to_api(self, image_path: str, lang: str, version: str = None):
        """Fallback to Python API when CLI is not available"""
        logger.info(f"Using Python API fallback for {lang}")
        
        try:
            # Use our enhanced OCR engine
            engine = EnhancedOCREngine(lang=lang)
            result = engine.process_image(image_path)
            
            logger.info(f"API Result for {lang}:")
            logger.info(f"Processing time: {result.processing_time:.2f}s")
            logger.info(f"Total texts found: {result.total_texts}")
            
            for i, ocr_result in enumerate(result.results[:3]):  # Show first 3 results
                logger.info(f"Text {i+1}: '{ocr_result.text}' (confidence: {ocr_result.confidence:.2f})")
                
        except Exception as e:
            logger.error(f"API fallback failed for {lang}: {e}")
    
    def _fallback_detection_only(self, image_path: str):
        """Fallback for detection-only using Python API"""
        logger.info("Using Python API for detection-only fallback")
        
        try:
            # Initialize OCR with detection only
            from paddleocr import PaddleOCR
            ocr = PaddleOCR(use_angle_cls=True, lang='en', rec=False)
            
            result = ocr.ocr(image_path, cls=True)
            
            if result and result[0]:
                logger.info(f"Detected {len(result[0])} text regions:")
                for i, detection in enumerate(result[0][:3]):  # Show first 3
                    bbox = detection
                    logger.info(f"Region {i+1}: bbox={bbox}")
            else:
                logger.info("No text regions detected")
                
        except Exception as e:
            logger.error(f"Detection-only fallback failed: {e}")
    
    def run_all_demos(self, image_path: Optional[str] = None):
        """Run all CLI demonstrations"""
        logger.info("Starting PaddleOCR CLI Tutorial Demonstrations")
        logger.info("=" * 60)
        
        try:
            self.demonstrate_full_pipeline(image_path)
            print("\n" + "=" * 60 + "\n")
            
            self.demonstrate_component_specific(image_path)
            print("\n" + "=" * 60 + "\n")
            
            self.demonstrate_model_versions(image_path)
            print("\n" + "=" * 60 + "\n")
            
            self.demonstrate_multilingual_cli()
            print("\n" + "=" * 60 + "\n")
            
            logger.info("All CLI demonstrations completed!")
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            raise


def main():
    """Main entry point for CLI examples"""
    parser = argparse.ArgumentParser(
        description="PaddleOCR CLI Examples from Tutorial Guide"
    )
    parser.add_argument(
        "--image", 
        type=str, 
        help="Path to image file (optional, will create sample if not provided)"
    )
    parser.add_argument(
        "--demo", 
        choices=["full", "components", "versions", "multilingual", "all"],
        default="all",
        help="Which demonstration to run"
    )
    
    args = parser.parse_args()
    
    # Initialize demo class
    demo = PaddleOCRCLIDemo()
    
    try:
        if args.demo == "all":
            demo.run_all_demos(args.image)
        elif args.demo == "full":
            demo.demonstrate_full_pipeline(args.image)
        elif args.demo == "components":
            demo.demonstrate_component_specific(args.image)
        elif args.demo == "versions":
            demo.demonstrate_model_versions(args.image)
        elif args.demo == "multilingual":
            demo.demonstrate_multilingual_cli()
            
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()