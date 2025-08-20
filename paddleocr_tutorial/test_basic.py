#!/usr/bin/env python3
"""
Basic functionality test for PaddleOCR tutorial implementation
"""

import sys
import traceback
from pathlib import Path

def test_basic_imports():
    """Test basic imports"""
    print("Testing basic imports...")
    
    try:
        import numpy as np
        print("[OK] numpy imported successfully")
    except ImportError as e:
        print(f"[FAIL] numpy import failed: {e}")
        return False
    
    try:
        import cv2
        print("[OK] opencv imported successfully")
    except ImportError as e:
        print(f"[FAIL] opencv import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("[OK] PIL imported successfully")
    except ImportError as e:
        print(f"[FAIL] PIL import failed: {e}")
        return False
    
    return True

def test_paddleocr_import():
    """Test PaddleOCR import"""
    print("\nTesting PaddleOCR import...")
    
    try:
        from paddleocr import PaddleOCR
        print("[OK] PaddleOCR imported successfully")
        return True
    except ImportError as e:
        print(f"[FAIL] PaddleOCR import failed: {e}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"[FAIL] PaddleOCR import error: {e}")
        traceback.print_exc()
        return False

def test_core_imports():
    """Test our core module imports"""
    print("\nTesting core module imports...")
    
    try:
        sys.path.append(str(Path(__file__).parent))
        from core.ocr_engine import EnhancedOCREngine
        print("[OK] EnhancedOCREngine imported successfully")
        return True
    except ImportError as e:
        print(f"[FAIL] Core module import failed: {e}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"[FAIL] Core module error: {e}")
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic OCR functionality"""
    print("\nTesting basic OCR functionality...")
    
    try:
        # Create a simple test image
        import numpy as np
        import cv2
        
        # Create a simple white image with black text
        img = np.ones((100, 300, 3), dtype=np.uint8) * 255
        cv2.putText(img, "Hello World", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Save test image
        test_img_path = "test_image.png"
        cv2.imwrite(test_img_path, img)
        print(f"[OK] Test image created: {test_img_path}")
        
        # Test basic PaddleOCR
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
        result = ocr.ocr(test_img_path, cls=True)
        
        if result and result[0]:
            print(f"[OK] OCR processed successfully, found {len(result[0])} text regions")
            for item in result[0]:
                text = item[1][0] if item[1] else ""
                confidence = item[1][1] if item[1] and len(item[1]) > 1 else 0
                print(f"  Text: '{text}', Confidence: {confidence:.3f}")
        else:
            print("[OK] OCR completed but no text found")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Basic functionality test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("PaddleOCR Tutorial - Basic Functionality Test")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_paddleocr_import,
        test_core_imports,
        test_basic_functionality
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"[CRASH] Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("Test Results:")
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "PASS" if result else "FAIL"
        print(f"{i+1}. {test.__name__}: {status}")
    
    passed = sum(results)
    total = len(results)
    print(f"\nSummary: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] All tests passed! Ready to proceed with tutorial examples.")
    else:
        print("[WARNING] Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)