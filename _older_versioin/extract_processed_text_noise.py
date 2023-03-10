import cv2 
import pytesseract

# get remove noise
def remove_noise(image):
    return cv2.medianBlur(image,5)

IMG_DIR = 'images_raw/' # directory with the original images
IMG_DIR_AFTER = 'images_processed/noise/' #directory storing pre-processed images
TXT_DIR = 'texts_processed/noise/' # directory storing OCR result from the pre-processed images

product_type = ["n", "v"]

#test images from 1 to 20 for both non-vegan and vegan products
for t in product_type:
    for x in range(1, 2):
        img_name = t + str(x)
        #import image
        image = cv2.imread(IMG_DIR + img_name + '.jpg')

        #convert image to black and white, and store in a directory
        image2 = remove_noise(image)
        cv2.imwrite(IMG_DIR_AFTER + img_name + ".png", image2)

        #OCR configuration
        custom_config = r'--oem 3 --psm 6'

        #extract text from preprocesed image, and store in in a text file
        text = pytesseract.image_to_string(image2, config=custom_config, lang='lav')
        sourceFile2 = open(TXT_DIR + img_name + ".txt", 'w', encoding='UTF-8')
        print(text, file = sourceFile2)
        sourceFile2.close()