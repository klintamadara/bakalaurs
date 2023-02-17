import cv2
import pytesseract

#testnr = 'v1'
IMG_DIR = 'images_raw/' # directory with the original images
TXT_DIR = 'texts_raw/' # directory storing OCR result from the original images

#test images from 1 to 20
for x in range(1, 21):
    img_name = "v" + str(x)

    #import image
    image = cv2.imread(IMG_DIR + img_name + '.jpg')
    #OCR configuration
    custom_config = r'--oem 3 --psm 6'

    #extract text from the original image using PyTesseract, Latvian language
    text_original = pytesseract.image_to_string(image, config=custom_config, lang='lav')
    #save the result in a text file
    sourceFile = open(TXT_DIR + img_name + ".txt", 'w', encoding='UTF-8')
    print(text_original, file = sourceFile)
    sourceFile.close()