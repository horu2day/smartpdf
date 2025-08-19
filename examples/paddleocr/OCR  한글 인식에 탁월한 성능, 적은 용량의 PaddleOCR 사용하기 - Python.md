### PaddleOCR 이란?

[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 은 중국의 인터넷 기업인 바이두(Baidu)가 만든 딥러닝 플랫폼 PaddlePaddle로 구현된 오픈 소스 OCR(Optical Character Recognition)입니다. 다양한 언어를 지원하며, 이미지와 문서에서 텍스트를 인식할 수 있습니다. PaddleOCR의 경량 모델은 14.8M로 매우 가벼워 모바일 등 다양한 플랫폼에서 사용이 가능합니다. 또한 중국어, 영어 이외에도 한국어를 포함하여 80개 이상의 다양한 언어를 지원합니다.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdna%2FA7567%2FbtsmnBzek5n%2FAAAAAAAAAAAAAAAAAAAAAMXG9XcpTUtuclOWqnQxkTaIBKZ3HGtF1VllLNFwB5f9%2Fimg.png%3Fcredential%3DyqXZFxpELC7KVnFOS48ylbz2pIh7yKj8%26expires%3D1756652399%26allow_ip%3D%26allow_referer%3D%26signature%3DG08%252FkFE4u7wrS0lKL6jzUx49WeU%253D)

PaddleOCR의 장점은 아래와 같습니다.

- 다양한 언어 지원
- 이미지와 문서에서 텍스트 인식
- 빠른 속도와 높은 정확도
- 다양한 플랫폼 지원

PaddleOCR는 다양한 최첨단 OCR 관련 알고리즘을 지원하며, 이를 바탕으로 산업용 특화 모델 및 솔루션인 PP-OCR과 PP-Structure를 개발하였습니다. PP-Structure는 레이아웃 분석, 표인식, 핵심정보 추출 등의 기능을 제공합니다.

PaddleOCR은 [온라인 웹페이지를 통해 체험](https://www.paddlepaddle.org.cn/hub/scene/ocr) 해볼 수 있습니다.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdna%2FcxFrXu%2FbtsmnBMKRgs%2FAAAAAAAAAAAAAAAAAAAAAPGItXU8QWhObpKcAfMHnsO27GOW6VdH_D-WKIdo20wV%2Fimg.png%3Fcredential%3DyqXZFxpELC7KVnFOS48ylbz2pIh7yKj8%26expires%3D1756652399%26allow_ip%3D%26allow_referer%3D%26signature%3D2s76zFr668M7h%252FT8gxCBB%252FBYCE4%253D)

### PP-OCR 시리즈 모델 목록

Detection Model에는 MobileNetV3, ResNet18\_vd, ResNet50 이렇게 3가지 Model이 있으며 MobileNetV3가 그 중 가장 일반적으로 사용되며 상대적으로 작고 모바일 애플리케이션에도 적합합니다. Recognition Model에는 사전학습된 MobileNetV3 모델이 있습니다.

---

### Install

pip를 이용하여 설치가 가능합니다.

```nginx
pip install paddlepaddle # for gpu user please install paddlepaddle-gpu

pip install paddleocr
```

그리고 설치 후 간단하게는 아래와 같이 실행이 가능합니다.

```lua
paddleocr --image_dir /your/test/image.jpg --lang=korean
```

### OCR (Optical Character Recognition)

ocr = PaddleOCR(lang="korean") 선언하면 최초에 한번은 Model을 다운로드 합니다. 경로는 Windows의 경우 C:/paddleocr/whl/rec/korean이고 Mac OS의 경우는 ~/.paddleocr/whl/rec/korean 입니다.

테스트는 아래 이미지를 이용합니다.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdna%2Fn1V12%2FbtsmBg04xXX%2FAAAAAAAAAAAAAAAAAAAAAGSQU2SdZD9MyeBS56QZrurWn5m8Jya70mp9RYGIR_zs%2Fimg.jpg%3Fcredential%3DyqXZFxpELC7KVnFOS48ylbz2pIh7yKj8%26expires%3D1756652399%26allow_ip%3D%26allow_referer%3D%26signature%3D2m3x9XbI2fr3GjsQbWCGdlTZIhg%253D)

```makefile
from paddleocr import PaddleOCR

 

ocr = PaddleOCR(lang="korean")

 

img_path = "assets/images/test_image_1.jpg"

result = ocr.ocr(img_path, cls=False)

 

ocr_result = result[0]

print(ocr_result)
```

Output:

```json
[[[[297.0, 246.0], [388.0, 246.0], [388.0, 272.0], [297.0, 272.0]], ('아래한글', 0.9990288019180298)], [[[398.0, 247.0], [485.0, 247.0], [485.0, 272.0], [398.0, 272.0]], ('한글문서', 0.9990617036819458)], [[[297.0, 275.0], [363.0, 277.0], [362.0, 304.0], [296.0, 302.0]], ('디자인', 0.9998207092285156)], [[[632.0, 354.0], [701.0, 354.0], [701.0, 377.0], [632.0, 377.0]], ('202204', 0.9998807907104492)]]
```

---

PaddleOCR 은 다양한 기능을 가지고 있지만 OCR 기능만을 추가로 검증하고 쉽게 확인하기 위해 추가로 개발하였습니다. 상세 Code는 [\[ Github \] PaddleOCR 라이브러리를 이용한 OCR](https://github.com/yunwoong7/korean_ocr_using_paddleOCR) 에서 확인하실 수 있습니다. 직접 작성하신다면 아래 내용을 참고하시면 됩니다.

main.py 파일을 만들어서 아래와 같이 작성하였습니다.

```python
import cv2

from paddleocr import PaddleOCR, draw_ocr

from utils.image_util import plt_imshow, put_text

from paddleocr.paddleocr import MODEL_URLS

 

 

class MyPaddleOCR:

    def __init__(self, lang: str = "korean", **kwargs):

        self.lang = lang

        self._ocr = PaddleOCR(lang="korean")

        self.img_path = None

        self.ocr_result = {}

    

    def get_available_langs(self):

        langs_info = []

 

        for idx, model_name in enumerate(list(MODEL_URLS['OCR'].keys())):

            for lang in list(MODEL_URLS['OCR'][model_name]['rec'].keys()):

                if lang not in langs_info:

                    langs_info.append(lang)

        

        print('Available Language : {}'.format(langs_info))

        

    def get_available_models(self):

        model_info = {}

 

        for idx, model_name in enumerate(list(MODEL_URLS['OCR'].keys())):

            model_info[model_name] = list(MODEL_URLS['OCR'][model_name]['rec'].keys())

            print('#{} Model Vesion : [{}] - Language : {}'.format(idx+1, model_name, list(MODEL_URLS['OCR'][model_name]['rec'].keys())))

        

    def get_ocr_result(self):

        return self.ocr_result

 

    def get_img_path(self):

        return self.img_path

 

    def show_img(self):

        plt_imshow(img=self.img_path)

        

    def run_ocr(self, img_path: str, debug: bool = False):

        self.img_path = img_path

        ocr_text = []

        result = self._ocr.ocr(img_path, cls=False)

        self.ocr_result = result[0]

 

        if self.ocr_result:

            for r in result[0]:

                ocr_text.append(r[1][0])

        else:

            ocr_text = "No text detected."

 

        if debug:

            self.show_img_with_ocr()

 

        return ocr_text

    

    def show_img_with_ocr(self):

        img = cv2.imread(self.img_path)

        roi_img = img.copy()

 

        for text_result in self.ocr_result:

            text = text_result[1][0]

            tlX = int(text_result[0][0][0])

            tlY = int(text_result[0][0][1])

            trX = int(text_result[0][1][0])

            trY = int(text_result[0][1][1])

            brX = int(text_result[0][2][0])

            brY = int(text_result[0][2][1])

            blX = int(text_result[0][3][0])

            blY = int(text_result[0][3][1])

 

            pts = ((tlX, tlY), (trX, trY), (brX, brY), (blX, blY))

 

            topLeft = pts[0]

            topRight = pts[1]

            bottomRight = pts[2]

            bottomLeft = pts[3]

 

            cv2.line(roi_img, topLeft, topRight, (0, 255, 0), 2)

            cv2.line(roi_img, topRight, bottomRight, (0, 255, 0), 2)

            cv2.line(roi_img, bottomRight, bottomLeft, (0, 255, 0), 2)

            cv2.line(roi_img, bottomLeft, topLeft, (0, 255, 0), 2)

            roi_img = put_text(roi_img, text, topLeft[0], topLeft[1] - 20, font_size=15)

 

            # print(text)

 

        plt_imshow(["Original", "ROI"], [img, roi_img], figsize=(16, 10))
```

utils/image\_util.py 파일은 아래와 같이 작성하였습니다.

```python
import cv2

import numpy as np

import platform

from PIL import ImageFont, ImageDraw, Image

from matplotlib import pyplot as plt

 

 

def plt_imshow(title='image', img=None, figsize=(8, 5)):

    plt.figure(figsize=figsize)

 

    if type(img) is str:

        img = cv2.imread(img)

 

    if type(img) == list:

        if type(title) == list:

            titles = title

        else:

            titles = []

 

            for i in range(len(img)):

                titles.append(title)

 

        for i in range(len(img)):

            if len(img[i].shape) <= 2:

                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_GRAY2RGB)

            else:

                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB)

 

            plt.subplot(1, len(img), i + 1), plt.imshow(rgbImg)

            plt.title(titles[i])

            plt.xticks([]), plt.yticks([])

 

        plt.show()

    else:

        if len(img.shape) < 3:

            rgbImg = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        else:

            rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

 

        plt.imshow(rgbImg)

        plt.title(title)

        plt.xticks([]), plt.yticks([])

        plt.show()

 

 

def put_text(image, text, x, y, color=(0, 255, 0), font_size=22):

    if type(image) == np.ndarray:

        color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(color_coverted)

 

    if platform.system() == 'Darwin':

        font = 'AppleGothic.ttf'

    elif platform.system() == 'Windows':

        font = 'malgun.ttf'

 

    image_font = ImageFont.truetype(font, font_size)

    font = ImageFont.load_default()

    draw = ImageDraw.Draw(image)

 

    draw.text((x, y), text, font=image_font, fill=color)

 

    numpy_image = np.array(image)

    opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

 

    return opencv_image
```

---

```coffeescript
from main import MyPaddleOCR

 

ocr = MyPaddleOCR()
```

지원 가능한 언어 목록을 조회하는 기능입니다.

```nginx
ocr.get_available_langs()
```

Output:

```nginx
Available Language : ['ch', 'en', 'korean', 'japan', 'chinese_cht', 'ta', 'te', 'ka', 'latin', 'arabic', 'cyrillic', 'devanagari', 'french', 'german', 'structure']
```

사용가능한 Model을 조회하는 기능입니다.

```nginx
ocr.get_available_models()
```

Output:

```nginx
#1 Model Vesion : [PP-OCRv3] - Language : ['ch', 'en', 'korean', 'japan', 'chinese_cht', 'ta', 'te', 'ka', 'latin', 'arabic', 'cyrillic', 'devanagari']

#2 Model Vesion : [PP-OCRv2] - Language : ['ch']

#3 Model Vesion : [PP-OCR] - Language : ['ch', 'en', 'french', 'german', 'korean', 'japan', 'chinese_cht', 'ta', 'te', 'ka', 'latin', 'arabic', 'cyrillic', 'devanagari', 'structure']
```
```nginx
img_path = 'assets/images/test_image_3.jpg'

ocr.run_ocr(img_path, debug=True)
```

Output:

```nginx
[2023/07/06 00:10:29] ppocr DEBUG: dt_boxes num : 4, elapse : 0.8806350231170654

[2023/07/06 00:10:29] ppocr DEBUG: rec_res num  : 4, elapse : 0.25487518310546875

['아래한글', '한글문서', '디자인', '202204']
```
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdna%2FynA1O%2FbtsmwXvgqja%2FAAAAAAAAAAAAAAAAAAAAACByittvwXVLh1xx0ILogm3jguLhC2LesALB0XLY7j-b%2Fimg.png%3Fcredential%3DyqXZFxpELC7KVnFOS48ylbz2pIh7yKj8%26expires%3D1756652399%26allow_ip%3D%26allow_referer%3D%26signature%3D80wLKF%252BxJ%252F2cMcLGuVSquqTX5ME%253D)

```nginx
ocr.get_ocr_result()
```
```json
[[[[297.0, 246.0], [388.0, 246.0], [388.0, 272.0], [297.0, 272.0]], ('아래한글', 0.9990288019180298)],

 [[[398.0, 247.0], [485.0, 247.0], [485.0, 272.0], [398.0, 272.0]], ('한글문서', 0.9990617036819458)],

 [[[297.0, 275.0], [363.0, 277.0], [362.0, 304.0], [296.0, 302.0]], ('디자인', 0.9998207092285156)],

 [[[632.0, 354.0], [701.0, 354.0], [701.0, 377.0], [632.0, 377.0]], ('202204', 0.9998807907104492)]]
```

---

PaddleOCR는 복잡한 환경의 이미지에서는 인식률이 다소 떨어질 수 있지만, 전반적으로는 매우 만족스러운 성능을 보여줍니다. 특히, 그 적은 용량 덕분에 다양한 플랫폼에서 쉽게 활용할 수 있으며, 이는 특히 모바일 환경에서의 사용성을 크게 향상시킵니다.

[이 글은 (새창열림) 본 저작자 표시 규칙 하에 배포할 수 있습니다. 자세한 내용은 Creative Commons 라이선스를 확인하세요.](https://creativecommons.org/licenses/by/4.0/deed.ko)