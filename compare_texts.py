import Levenshtein

TXT_DIR_RAW = 'texts_raw/' # directory storing OCR result from the original images
TXT_DIR_BW = 'texts_processed/B&W/' # directory storing OCR result from the pre-processed images
TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/' #directory storing all of the results

#code compares results from OCR to the correct ingredients list and returns Levenshtein index
#for each test case, saves it in the result txt file
results = 'similarity_Levenshtein'
result_file_raw = open(TXT_DIR_RSLTS + results + "_B&W.txt", 'w')
result_file_BW = open(TXT_DIR_RSLTS + results + "_B&W.txt", 'w')


testnr = 'n1'
#img_name = "n" + str(x) #non-vegan products
#img_name_v = "v" + str(x) #vegan products

#prepare the correct ingredients list for testing purposes
txt_tru = open(TXT_DIR_TRU + testnr + ".txt", "r", encoding='UTF-8')
txt_tru_content = txt_tru.read()

#prepare the OCR result from original image for testing purposes
txt_raw = open(TXT_DIR_RAW + testnr + ".txt", "r", encoding='UTF-8')
txt_raw_content = txt_raw.read()

#prepare the OCR result from B&W image for testing purposes
txt_BW = open(TXT_DIR_BW + testnr + ".txt", "r", encoding='UTF-8')
txt_BW_content = txt_BW.read()

#calculate similarity index for the OCR result of the original image 
print(Levenshtein.distance(txt_raw_content, txt_tru_content), file = result_file_raw)
#calculate similarity index for the OCR result of the pre-processed image 
print(Levenshtein.distance(txt_BW_content, txt_tru_content), file = result_file_BW)

txt_raw.close()
txt_tru.close()
txt_BW.close()


result_file_raw.close()
result_file_BW.close()