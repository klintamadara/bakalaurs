import cv2 
import pytesseract

IMG_DIR_AFTER = 'images_processed/noiseGS/' #directory storing pre-processed images
TXT_DIR = 'texts_processed/noiseGS/' # directory storing OCR result from the pre-processed images

product_type = ["n", "v"]

#test images from 1 to 20 for both non-vegan and vegan products
for t in product_type:
    for x in range(1, 101):
        img_name = t + str(x)
        #import image
        image2 = cv2.imread(IMG_DIR_AFTER + img_name + '.png')

        #OCR configuration
        custom_config = r'--oem 3 --psm 6'

        #extract text from preprocesed image, and store in in a text file
        text = pytesseract.image_to_string(image2, config=custom_config, lang='lav')
        sourceFile2 = open(TXT_DIR + img_name + ".txt", 'w', encoding='UTF-8')
        print(text, file = sourceFile2)
        sourceFile2.close()