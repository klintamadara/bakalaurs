import cv2 
import pytesseract


IMG_DIR = 'images_raw/' # directory with the original images
IMG_DIR_AFTER = 'images_processed/upscale/' #directory storing pre-processed images
TXT_DIR = 'texts_processed/upscale/' # directory storing OCR result from the pre-processed images

#manipulate images from 1 to 100 for both non-vegan and vegan products
product_type = ["n"]#,"v"]
for t in product_type:
    for x in range(1, 2):
        img_name = t + str(x)

        #import image
        image = cv2.imread(IMG_DIR + img_name + '.jpg')
        #image = image[:80,850:]

        #upscale image 4x using Super Resolution technique
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        path = "EDSR_x4.pb"
        sr.readModel(path)
        sr.setModel("edsr",4)
        
        image2 = sr.upsample(image)
        

        cv2.imwrite(IMG_DIR_AFTER + img_name + ".png", image2)

        #OCR configuration
        custom_config = r'--oem 3 --psm 6'

        #extract text from preprocesed image, and store in in a text file
        text = pytesseract.image_to_string(image2, config=custom_config, lang='lav')
        sourceFile2 = open(TXT_DIR + img_name + ".txt", 'w', encoding='UTF-8')
        print(text, file = sourceFile2)
        sourceFile2.close()