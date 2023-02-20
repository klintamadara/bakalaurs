import Levenshtein

TXT_DIR_RAW = 'texts_raw/' # directory storing OCR result from the original images
TXT_DIR_BW = 'texts_processed/B&W/' # directory storing OCR result from the pre-processed images
TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/' #directory storing all of the results


#code compares results from OCR to the correct ingredients list and returns Levenshtein index
#for each test case, saves it in the result txt file
results = 'similarity_Levenshtein'

#erase if there was content in the text files before and write title
result_file_raw = open(TXT_DIR_RSLTS + results + "_raw.txt", 'w')
print("Levenshtein between raw and actual", file = result_file_raw)
result_file_BW = open(TXT_DIR_RSLTS + results + "_B&W.txt", 'w')
print("Levenshtein between Black&White and actual", file = result_file_BW)
result_file_raw.close()
result_file_BW.close()

result_file_raw = open(TXT_DIR_RSLTS + results + "_raw.txt", 'a')
result_file_BW = open(TXT_DIR_RSLTS + results + "_B&W.txt", 'a')

#test images from 1 to 20 non vegan
for x in range(1, 21):
    img_name = "n" + str(x)

    #prepare the correct ingredients list for testing purposes
    txt_tru = open(TXT_DIR_TRU + img_name + ".txt", "r", encoding='UTF-8')
    txt_tru_content = txt_tru.read()

    #prepare the OCR result from original image for testing purposes
    txt_raw = open(TXT_DIR_RAW + img_name + ".txt", "r", encoding='UTF-8')
    txt_raw_content = txt_raw.read()

    #prepare the OCR result from B&W image for testing purposes
    txt_BW = open(TXT_DIR_BW + img_name + "_B&W.txt", "r", encoding='UTF-8')
    txt_BW_content = txt_BW.read()

    #calculate similarity index for the OCR result of the original image 
    print(img_name + ": " + str(Levenshtein.distance(txt_raw_content, txt_tru_content)), file = result_file_raw)
    #calculate similarity index for the OCR result of the pre-processed image 
    print(img_name + ": " + str(Levenshtein.distance(txt_BW_content, txt_tru_content)), file = result_file_BW)
    #test print(Levenshtein.distance(txt_tru_content, txt_tru_content), file = result_file_BW)


#test images from 1 to 20 vegan
for x in range(1, 21):
    img_name = "v" + str(x)

    #prepare the correct ingredients list for testing purposes
    txt_tru = open(TXT_DIR_TRU + img_name + ".txt", "r", encoding='UTF-8')
    txt_tru_content = txt_tru.read()

    #prepare the OCR result from original image for testing purposes
    txt_raw = open(TXT_DIR_RAW + img_name + ".txt", "r", encoding='UTF-8')
    txt_raw_content = txt_raw.read()

    #prepare the OCR result from B&W image for testing purposes
    txt_BW = open(TXT_DIR_BW + img_name + "_B&W.txt", "r", encoding='UTF-8')
    txt_BW_content = txt_BW.read()

    #calculate similarity index for the OCR result of the original image 
    print(img_name + ": " + str(Levenshtein.distance(txt_raw_content, txt_tru_content)), file = result_file_raw)
    #calculate similarity index for the OCR result of the pre-processed image 
    print(img_name + ": " + str(Levenshtein.distance(txt_BW_content, txt_tru_content)), file = result_file_BW)
    #test print(Levenshtein.distance(txt_tru_content, txt_tru_content), file = result_file_BW)


txt_tru.close()
txt_BW.close()
txt_raw.close()



result_file_raw.close()
result_file_BW.close()