#testing accuracy of page segmentation modes (PSMs)
import Levenshtein
import string

def Jaccard_similarity(x,y):
    if(len(x) == 0 or len(y) == 0):
        return 0
    z=set(x).intersection(set(y))
    a=float(len(z))/(len(x)+len(y)-len(z))
    return a

def overlap_coefficient(x,y):
    if(len(x) == 0 or len(y) == 0):
        return 0
    z=set(x).intersection(set(y))
    a=float(len(z))/min(len(x),len(y))
    return a

TXT_DIR_PSM3 = 'texts_processed/B&W/' # directory storing OCR result using PSM 3
TXT_DIR_PSM6 = 'texts_processed/GS/' # directory storing OCR result using PSM 6
TXT_DIR_PSM13 = 'texts_processed/BGremove/' # directory storing OCR result using PSM 13
TXT_DIR_RAW = 'texts_raw/' 

TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/' #directory storing all of the results

#code compares results from OCR to the correct ingredients list and returns Levenshtein and Jaccard similarity, as well as overlap coefficient
#for each test case, saves it in the result txt file
results = 'IMAGES'

#erase if there was content in the text files before and write title
result_file_psm3 = open(TXT_DIR_RSLTS + results + "_BW.txt", 'w')
print("Levenshtein; Jaccard; Overlap", file = result_file_psm3)

result_file_psm6 = open(TXT_DIR_RSLTS + results + "_GS.txt", 'w')
print("Levenshtein; Jaccard; Overlap", file = result_file_psm6)

result_file_psm13 = open(TXT_DIR_RSLTS + results + "_BGremove.txt", 'w')
print("Levenshtein; Jaccard; Overlap", file = result_file_psm13)

result_file_raw = open(TXT_DIR_RSLTS + results + "_raw.txt", 'w')
print("Levenshtein; Jaccard; Overlap", file = result_file_raw)

result_file_all = open(TXT_DIR_RSLTS + results + ".txt", 'w')
print("ID;raw L;raw J;raw O; BW Levenshtein;BW Jaccard;BW Overlap;GS Levenshtein;GS Jaccard;GS Overlap;GBremove Levenshtein;GBremove Jaccard;GBremove Overlap", file = result_file_all)

result_file_psm3.close()
result_file_psm6.close()
result_file_psm13.close()
result_file_all.close()
result_file_raw.close()

result_file_psm3 = open(TXT_DIR_RSLTS + results + "_BW.txt", 'a')
result_file_psm6 = open(TXT_DIR_RSLTS + results + "_GS.txt", 'a')
result_file_psm13 = open(TXT_DIR_RSLTS + results + "_BGremove.txt", 'a')
result_file_raw = open(TXT_DIR_RSLTS + results + "_raw.txt", 'a')
result_file_all = open(TXT_DIR_RSLTS + results + ".txt", 'a')


#calculate scores for 200 images, both non-vegan (n) and vegan (v) products (100 samples each)
product_type = ["n", "v"]
for t in product_type:
    for x in range(1, 101):
        img_name = t + str(x)

        #prepare the correct ingredients list for testing purposes
        txt_tru = open(TXT_DIR_TRU + img_name + ".txt", "r", encoding='UTF-8')
        txt_tru_content = txt_tru.read()

        #prepare the OCR result from psm3 for testing purposes
        txt_psm3 = open(TXT_DIR_PSM3 + img_name + ".txt", "r", encoding='UTF-8')
        txt_psm3_content = txt_psm3.read()
        #prepare the OCR result from psm6 for testing purposes
        txt_psm6 = open(TXT_DIR_PSM6 + img_name + ".txt", "r", encoding='UTF-8')
        txt_psm6_content = txt_psm6.read()
        #prepare the OCR result from psm13 image for testing purposes
        txt_psm13 = open(TXT_DIR_PSM13 + img_name + ".txt", "r", encoding='UTF-8')
        txt_psm13_content = txt_psm13.read()
        #prepare the OCR result from psm13 image for testing purposes
        txt_raw = open(TXT_DIR_RAW + img_name + ".txt", "r", encoding='UTF-8')
        txt_raw_content = txt_raw.read()

        #create lists, separating text in words. Remove unnecessary spaces and other redundant characters
        words_separate_psm3 = [s.strip(string.punctuation) for s in txt_psm3_content.split()]
        words_separate_psm3 = [s.strip() for s in words_separate_psm3 if s != '' and s!= ' ']

        words_separate_psm6 = [s.strip(string.punctuation) for s in txt_psm6_content.split()]
        words_separate_psm6 = [s.strip() for s in words_separate_psm6 if s != '' and s!= ' ']

        words_separate_psm13 = [s.strip(string.punctuation) for s in txt_psm13_content.split()]
        words_separate_psm13 = [s.strip() for s in words_separate_psm13 if s != '' and s!= ' ']

        words_separate_raw = [s.strip(string.punctuation) for s in txt_raw_content.split()]
        words_separate_raw = [s.strip() for s in words_separate_raw if s != '' and s!= ' ']


        words_separate_tru = [s.strip(string.punctuation) for s in txt_tru_content.split()]
        words_separate_tru = [s.strip() for s in words_separate_tru if s != '' and s!= ' ']

        #calculate similarity scores and write them to file 
        Levenshtein_psm3 = str(Levenshtein.distance(txt_psm3_content, txt_tru_content))
        Levenshtein_psm6 = str(Levenshtein.distance(txt_psm6_content, txt_tru_content))
        Levenshtein_psm13 = str(Levenshtein.distance(txt_psm13_content, txt_tru_content))
        Levenshtein_raw = str(Levenshtein.distance(txt_raw_content, txt_tru_content))

        Jaccard_psm3 = str(Jaccard_similarity(words_separate_psm3, words_separate_tru))
        Jaccard_psm6 = str(Jaccard_similarity(words_separate_psm6, words_separate_tru))
        Jaccard_psm13 = str(Jaccard_similarity(words_separate_psm13, words_separate_tru))
        Jaccard_raw = str(Jaccard_similarity(words_separate_raw, words_separate_tru))

        overlap_psm3 = str(overlap_coefficient(words_separate_psm3, words_separate_tru))
        overlap_psm6 = str(overlap_coefficient(words_separate_psm6, words_separate_tru))
        overlap_psm13 = str(overlap_coefficient(words_separate_psm13, words_separate_tru))
        overlap_raw = str(overlap_coefficient(words_separate_raw, words_separate_tru))

   
        print(img_name + ";" + Levenshtein_psm3 + ";" + Jaccard_psm3 + ";" + overlap_psm3, file = result_file_psm3)
        print(img_name + ";" + Levenshtein_psm6 + ";" + Jaccard_psm6 + ";" + overlap_psm6, file = result_file_psm6)
        print(img_name + ";" + Levenshtein_psm13 + ";" + Jaccard_psm13 + ";" + overlap_psm13, file = result_file_psm13)
        print(img_name + ";" + Levenshtein_raw + ";" + Jaccard_raw + ";" + overlap_raw, file = result_file_raw)

        print(img_name + ";" + Levenshtein_raw + ";" + Jaccard_raw + ";" + overlap_raw + ";" + Levenshtein_psm3 + ";" + Jaccard_psm3 + ";" + overlap_psm3 + ";" + Levenshtein_psm6 + ";" + Jaccard_psm6 + ";" + overlap_psm6 + ";" + Levenshtein_psm13 + ";" + Jaccard_psm13 + ";" + overlap_psm13, file = result_file_all)


txt_tru.close()
txt_psm13.close()
txt_psm6.close()
txt_psm3.close()
result_file_psm3.close()
result_file_psm6.close()
result_file_psm13.close()
result_file_all.close()