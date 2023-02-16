import cv2 
import pytesseract
from matplotlib import pyplot as plt


testnr = 'v1'
IMG_DIR = 'images_raw/' # directory with the original images
TXT_DIR = 'texts_raw/' # directory storing OCR result from the original images

#test images from 1 to 20
for x in range(1, 21):
    #import image
    image = cv2.imread(IMG_DIR + "n" + str(x) + '.jpg')
    #OCR configuration
    custom_config = r'--oem 3 --psm 6'

    #extract text from the original image using PyTesseract, Latvian language
    text_original = pytesseract.image_to_string(image, config=custom_config, lang='lav')
    #write the result in a file
    sourceFile = open(TXT_DIR + "n" + str(x) + ".txt", 'w')
    print(text_original, file = sourceFile)
    sourceFile.close()