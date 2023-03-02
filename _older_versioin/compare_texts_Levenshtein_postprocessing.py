import Levenshtein

TXT_DIR_RAW = 'texts_raw/' # directory storing OCR result from the original images
TXT_DIR_BW = 'texts_processed/B&W/' # directory storing OCR result from the pre-processed images
TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/' #directory storing all of the results
TXT_DIR_POST = 'texts_processed/part1/' #directory storing manually prepared correct ingredients lists -> for testing


#code compares results from OCR to the correct ingredients list and returns Levenshtein index
#for each test case, saves it in the result txt file
results = 'similarity_Levenshtein'

#erase if there was content in the text file and write a title
result_file_raw = open(TXT_DIR_RSLTS + results + "_post_raw-shortened.txt", 'w')
print("Levenshtein post-processing between raw-shortened and actual", file = result_file_raw)
result_file_raw.close()

result_file_raw = open(TXT_DIR_RSLTS + results + "_post_raw-shortened.txt", 'a')

#test images from 1 to 20 non vegan
for x in range(1, 21):
    img_name = "n" + str(x)

    #prepare the correct ingredients list for testing purposes
    txt_tru = open(TXT_DIR_TRU + img_name + ".txt", "r", encoding='UTF-8')
    txt_tru_content = txt_tru.read()

    #prepare the OCR result from original image for testing purposes
    txt_short = open(TXT_DIR_POST + img_name + ".txt", "r", encoding='UTF-8')
    txt_short_content = txt_short.read()

    #calculate similarity index for the OCR result of the original image 
    print(img_name + ": " + str(Levenshtein.distance(txt_short_content, txt_tru_content)), file = result_file_raw)


for x in range(1, 21):
    img_name = "v" + str(x)

    #prepare the correct ingredients list for testing purposes
    txt_tru = open(TXT_DIR_TRU + img_name + ".txt", "r", encoding='UTF-8')
    txt_tru_content = txt_tru.read()

    #prepare the OCR result from original image for testing purposes
    txt_short = open(TXT_DIR_POST + img_name + ".txt", "r", encoding='UTF-8')
    txt_short_content = txt_short.read()

    #calculate similarity index for the OCR result of the original image 
    print(img_name + ": " + str(Levenshtein.distance(txt_short_content, txt_tru_content)), file = result_file_raw)


txt_tru.close()
txt_short.close()

result_file_raw.close()