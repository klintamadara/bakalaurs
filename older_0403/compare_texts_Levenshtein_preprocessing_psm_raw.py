#testing accuracy of page segmentation modes (PSMs)
import Levenshtein

TXT_DIR_PSM3 = 'texts_raw/psm3/' # directory storing OCR result using PSM 3
TXT_DIR_PSM6 = 'texts_raw/' # directory storing OCR result using PSM 6
TXT_DIR_PSM13 = 'texts_raw/psm13/' # directory storing OCR result using PSM 13
TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/' #directory storing all of the results

#code compares results from OCR to the correct ingredients list and returns Levenshtein index
#for each test case, saves it in the result txt file
results = 'similarity_Levenshtein'

#erase if there was content in the text files before and write title
result_file_psm3 = open(TXT_DIR_RSLTS + results + "_psm3.txt", 'w')
print("PSM13 Levenshtein; PSM13 Jaccard; PSM13 Overlap", file = result_file_psm3)

result_file_psm13 = open(TXT_DIR_RSLTS + results + "_psm13.txt", 'w')
print("PSM13 Levenshtein; PSM13 Jaccard; PSM13 Overlap", file = result_file_psm13)

result_file_psm3.close()
result_file_psm13.close()

result_file_raw = open(TXT_DIR_RSLTS + results + "_psm3.txt", 'a')
result_file_BW = open(TXT_DIR_RSLTS + results + "_psm13.txt", 'a')

product_type = ["n", "v"]

##test images from 1 to 20 non vegan for both non-vegan and vegan products
for t in product_type:
    for x in range(1, 21):
        img_name = t + str(x)

        #prepare the correct ingredients list for testing purposes
        txt_tru = open(TXT_DIR_TRU + img_name + ".txt", "r", encoding='UTF-8')
        txt_tru_content = txt_tru.read()

        #prepare the OCR result from psm3 for testing purposes
        txt_psm3 = open(TXT_DIR_PSM3 + img_name + ".txt", "r", encoding='UTF-8')
        txt_psm3_content = txt_psm3.read()

        #prepare the OCR result from psm13 image for testing purposes
        txt_psm13 = open(TXT_DIR_PSM13 + img_name + ".txt", "r", encoding='UTF-8')
        txt_psm13_content = txt_psm13.read()

        #calculate similarity index for the OCR result of the original image 
        print(img_name + ": " + str(Levenshtein.distance(txt_psm3_content, txt_tru_content)), file = result_file_psm3)
        #calculate similarity index for the OCR result of the pre-processed image 
        print(img_name + ": " + str(Levenshtein.distance(txt_psm13_content, txt_tru_content)), file = result_file_BW)
        #test print(Levenshtein.distance(txt_tru_content, txt_tru_content), file = result_file_BW)

txt_tru.close()
txt_psm13.close()
txt_psm3.close()
result_file_raw.close()
result_file_BW.close()