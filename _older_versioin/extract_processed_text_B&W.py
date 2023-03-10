import cv2 
import numpy as np
import pytesseract
#from pytesseract import Output
#from matplotlib import pyplot as plt


def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def rotate(image):
    # convert the image to grayscale and flip the foreground and background to ensure foreground is now "white" and
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    # threshold the image, setting all foreground pixels to 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # grab the (x, y) coordinates of all pixel values that are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    # the `cv2.minAreaRect` function returns values in the range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we need to add 90 degrees to the angle
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # draw the correction angle on the image so we can validate it
    cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    print("[INFO] angle: {:.3f}".format(angle))
    return image


def get_blackwhite(image):
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
    return blackAndWhiteImage



#testnr = 'v1'
IMG_DIR = 'images_raw/' # directory with the original images
IMG_DIR_AFTER = 'images_processed/B&W/' #directory storing pre-processed images
TXT_DIR = 'texts_processed/B&W/' # directory storing OCR result from the pre-processed images


#test images from 1 to 20
for x in range(1, 21):
    img_name = "v" + str(x)
    #import image
    image = cv2.imread(IMG_DIR + img_name + '.jpg')

    #convert image to black and white, and store in a directory
    image2 = get_blackwhite(image)
    cv2.imwrite(IMG_DIR_AFTER + img_name + "_B&W.png", image2)

    #OCR configuration
    custom_config = r'--oem 3 --psm 6'

    #extract text from preprocesed image, and store in in a text file
    text = pytesseract.image_to_string(image2, config=custom_config, lang='lav')
    sourceFile2 = open(TXT_DIR + img_name + "_B&W.txt", 'w', encoding='UTF-8')
    print(text, file = sourceFile2)
    sourceFile2.close()