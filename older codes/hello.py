
"""
def remove_neighbors(list_raw, index, i):
    if(i == 0): i = 3
    if(i == 1): i = 2
    if(i == 2): i = 1
    for k in range(0, i):
        try:
            list_raw.remove(index-k)
        except IndexError:
            pass
        try:
            list_raw.remove(index+k)
        except IndexError:
            pass
    return list_raw
"""


def remove_duplicates(list_raw, list_removed, i):
    if(list_removed == []): return list_raw
    all_words_identified = get_all_words(list_raw)
    
    if(i == 0): word_count = 2
    elif(i == 1): word_count = 1
    elif(i == 2): word_count = 0
    print(list_removed)
    for word in list_removed:
        for k in range(0, word_count):
            try:
                all_words_identified.remove(word)
            except ValueError:
                pass
    return split_text_into_ingredients(all_words_identified, word_count + 1)





""" image = cv2.imread(IMG_DIR + '3.jpg', 1)

# Convert image to image gray
tmp = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Applying thresholding technique
_, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)

b,g,r = cv2.split(image)
rgba = [b, g, r, alpha]
rgb_img = cv2.merge(rgba,4)
cv2.imwrite("gfg_white.png", rgb_img) """
#cv2.imwrite("gfg_white.png", rgb_img)

import re
import cv2 
import numpy as np
import pytesseract
from pytesseract import Output
from matplotlib import pyplot as plt
import Levenshtein


def bgremove1(myimage):
    # Blur to image to reduce noise
    myimage = cv2.GaussianBlur(myimage,(5,5), 0)
    # We bin the pixels. Result will be a value 1..5
    bins=np.array([0,51,102,153,204,255])
    myimage[:,:,:] = np.digitize(myimage[:,:,:],bins,right=True)*51
    # Create single channel greyscale for thresholding
    myimage_grey = cv2.cvtColor(myimage, cv2.COLOR_BGR2GRAY)
    # Perform Otsu thresholding and extract the background.
    # We use Binary Threshold as we want to create an all white background
    ret,background = cv2.threshold(myimage_grey,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # Convert black and white back into 3 channel greyscale
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)
    # Perform Otsu thresholding and extract the foreground.
    # We use TOZERO_INV as we want to keep some details of the foregorund
    ret,foreground = cv2.threshold(myimage_grey,0,255,cv2.THRESH_TOZERO_INV+cv2.THRESH_OTSU)  #Currently foreground is only a mask
    foreground = cv2.bitwise_and(myimage,myimage, mask=foreground)  # Update foreground with bitwise_and to extract real foreground
    # Combine the background and foreground to obtain our final image
    return background+foreground


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

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def get_blackwhite(image):
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
    return blackAndWhiteImage

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


testnr = '1'
IMG_DIR = 'images/'
IMG_DIR_TEST = 'test_images/'
TXT_DIR = 'test_texts/'
image = cv2.imread(IMG_DIR + testnr + '.jpg')


#b,g,r = cv2.split(image)
#rgb_img = cv2.merge([r,g,b])

image2 = get_blackwhite(image)
#image2 = rgb_img
cv2.imwrite(IMG_DIR_TEST + testnr + "_after.png", image2)

#plt.imshow(image2[:,:,::-1]) #-1 changes RGB to BGR as CV2 uses BGR
#plt.show()
#plt.title('AUREBESH ORIGINAL IMAGE')


#image2=image
#OCR
custom_config = r'--oem 3 --psm 6'

#"""
#extract text from original image
text_original = pytesseract.image_to_string(image, config=custom_config, lang='lav')
sourceFile = open(TXT_DIR + testnr + ".txt", 'w')
print(text_original, file = sourceFile)
sourceFile.close()

#compare to actual text
txt_file = open("texts/"+testnr+".txt", "r", encoding='UTF-8')
file_content = txt_file.read()
print(file_content)
print(Levenshtein.distance(text_original, file_content))
txt_file.close()
#"""

#extract text from preprocesed image
text = pytesseract.image_to_string(image2, config=custom_config, lang='lav')
sourceFile2 = open(TXT_DIR + testnr + "_after.txt", 'w')
print(text, file = sourceFile2)
sourceFile2.close()


#compare to actual text
txt_file = open("texts/"+testnr+".txt", "r", encoding='UTF-8')
file_content = txt_file.read()
print(Levenshtein.distance(text, file_content))
txt_file.close()


"""
1. a seperate file get text and image without preprocessing
2. write a code which eliminates "Sastāvdaļas - before"?
3. Metrics - Levenshtein + F1?
4. Jāaiziet uz veikalu un jānofotografē piemēri

text = text.replace(",", "")
list_text = text.split() #make a list of all ingredients


print(text+"\nAtbilde:")

#for i in list_text:
#    print(i)

txt_file = open("list.txt", "r", encoding='UTF-8')
file_content = txt_file.read()
#print("The file content are: ", file_content)
list_ingredients = file_content.split("\n")
txt_file.close()
#print("The list is: ", list_ingredients)

veg = 1

for word in list_text:
    #print(word.casefold())
    if word.casefold() in list_ingredients:
        print ("Nav vegānisks. Satur " + word)
        veg = 0
        break
if veg == 1:
    print("Produkts ir vegānisks")
    
"""