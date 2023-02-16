try:
    import Image
except ImportError:
    from PIL import Image

import pytesseract

#Basic OCR
print(pytesseract.image_to_string(Image.open('./images/test.jpg')))

#In French
print(pytesseract.image_to_string(Image.open('./images/test.jpg'), lang='lat'))