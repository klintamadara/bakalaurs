import cv2 
import pytesseract

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

IMG_DIR = 'images_raw/' # directory with the original images
IMG_DIR_AFTER = 'images_processed/combined/' #directory storing pre-processed images
TXT_DIR = 'texts_processed/combined/' # directory storing OCR result from the pre-processed images

product_type = ["n", "v"]
#test images from 1 to 100 for both non-vegan and vegan products
for t in product_type:
    for x in range(1, 5):
        img_name = t + str(x)
        #import image
        img = cv2.imread(IMG_DIR + img_name + '.jpg',0)

        #convert image to black and white, and store in a directory
        #image_greyscale = get_grayscale(image)


        #img = cv2.imread('sudoku.png',0)
        img = cv2.medianBlur(img,5)
        image2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv2.THRESH_BINARY,11,2)



        cv2.imwrite(IMG_DIR_AFTER + img_name + ".png", image2)

        #OCR configuration
        custom_config = r'--oem 3 --psm 6'

        #extract text from preprocesed image, and store in in a text file
        text = pytesseract.image_to_string(image2, config=custom_config, lang='lav')
        sourceFile2 = open(TXT_DIR + img_name + ".txt", 'w', encoding='UTF-8')
        print(text, file = sourceFile2)
        sourceFile2.close()