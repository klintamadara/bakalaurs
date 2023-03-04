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

TXT_DIR_PSM3 = 'texts_raw/psm3/' # directory storing OCR result using PSM 3
TXT_DIR_PSM6 = 'texts_raw/' # directory storing OCR result using PSM 6
TXT_DIR_PSM13 = 'texts_raw/psm13/' # directory storing OCR result using PSM 13
TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/' #directory storing all of the results

#code compares results from OCR to the correct ingredients list and returns Levenshtein and Jaccard similarity, as well as overlap coefficient
#for each test case, saves it in the result txt file
results = 'PSMs'

#erase if there was content in the text files before and write title
result_file_psm3 = open(TXT_DIR_RSLTS + results + "_psm3.txt", 'w')
print("PSM3 Levenshtein; PSM3 Jaccard; PSM3 Overlap", file = result_file_psm3)

result_file_psm6 = open(TXT_DIR_RSLTS + results + "_psm6.txt", 'w')
print("PSM6 Levenshtein; PSM6 Jaccard; PSM6 Overlap", file = result_file_psm6)

result_file_psm13 = open(TXT_DIR_RSLTS + results + "_psm13.txt", 'w')
print("PSM13 Levenshtein; PSM13 Jaccard; PSM13 Overlap", file = result_file_psm13)

result_file_all = open(TXT_DIR_RSLTS + results + ".txt", 'w')
print("ID;PSM3 Levenshtein;PSM3 Jaccard;PSM3 Overlap;PSM6 Levenshtein;PSM6 Jaccard;PSM6 Overlap;PSM13 Levenshtein;PSM13 Jaccard;PSM13 Overlap", file = result_file_all)

result_file_psm3.close()
result_file_psm6.close()
result_file_psm13.close()
result_file_all.close()

result_file_psm3 = open(TXT_DIR_RSLTS + results + "_psm3.txt", 'a')
result_file_psm6 = open(TXT_DIR_RSLTS + results + "_psm6.txt", 'a')
result_file_psm13 = open(TXT_DIR_RSLTS + results + "_psm13.txt", 'a')
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

        #create lists, separating text in words. Remove unnecessary spaces and other redundant characters
        words_separate_psm3 = [s.strip(string.punctuation) for s in txt_psm3_content.split()]
        words_separate_psm3 = [s.strip() for s in words_separate_psm3 if s != '' and s!= ' ']

        words_separate_psm6 = [s.strip(string.punctuation) for s in txt_psm6_content.split()]
        words_separate_psm6 = [s.strip() for s in words_separate_psm6 if s != '' and s!= ' ']

        words_separate_psm13 = [s.strip(string.punctuation) for s in txt_psm13_content.split()]
        words_separate_psm13 = [s.strip() for s in words_separate_psm13 if s != '' and s!= ' ']

        words_separate_tru = [s.strip(string.punctuation) for s in txt_tru_content.split()]
        words_separate_tru = [s.strip() for s in words_separate_tru if s != '' and s!= ' ']

        #calculate similarity scores and write them to file 
        Levenshtein_psm3 = str(Levenshtein.distance(txt_psm3_content, txt_tru_content))
        Levenshtein_psm6 = str(Levenshtein.distance(txt_psm6_content, txt_tru_content))
        Levenshtein_psm13 = str(Levenshtein.distance(txt_psm13_content, txt_tru_content))

        Jaccard_psm3 = str(Jaccard_similarity(words_separate_psm3, words_separate_tru))
        Jaccard_psm6 = str(Jaccard_similarity(words_separate_psm6, words_separate_tru))
        Jaccard_psm13 = str(Jaccard_similarity(words_separate_psm13, words_separate_tru))

        overlap_psm3 = str(overlap_coefficient(words_separate_psm3, words_separate_tru))
        overlap_psm6 = str(overlap_coefficient(words_separate_psm6, words_separate_tru))
        overlap_psm13 = str(overlap_coefficient(words_separate_psm13, words_separate_tru))
        """
        Jaccard_psm3 = str(round(Jaccard_similarity(words_separate_psm3, words_separate_tru),4))
        Jaccard_psm6 = str(round(Jaccard_similarity(words_separate_psm6, words_separate_tru),4))
        Jaccard_psm13 = str(round(Jaccard_similarity(words_separate_psm13, words_separate_tru),4))

        overlap_psm3 = str(round(overlap_coefficient(words_separate_psm3, words_separate_tru),4))
        overlap_psm6 = str(round(overlap_coefficient(words_separate_psm6, words_separate_tru),4))
        overlap_psm13 = str(round(overlap_coefficient(words_separate_psm13, words_separate_tru),4))
        """
        print(img_name + ";" + Levenshtein_psm3 + ";" + Jaccard_psm3 + ";" + overlap_psm3, file = result_file_psm3)
        print(img_name + ";" + Levenshtein_psm6 + ";" + Jaccard_psm6 + ";" + overlap_psm6, file = result_file_psm6)
        print(img_name + ";" + Levenshtein_psm13 + ";" + Jaccard_psm13 + ";" + overlap_psm13, file = result_file_psm13)

        print(img_name + ";" + Levenshtein_psm3 + ";" + Jaccard_psm3 + ";" + overlap_psm3 + ";" + Levenshtein_psm6 + ";" + Jaccard_psm6 + ";" + overlap_psm6 + ";" + Levenshtein_psm13 + ";" + Jaccard_psm13 + ";" + overlap_psm13, file = result_file_all)


txt_tru.close()
txt_psm13.close()
txt_psm6.close()
txt_psm3.close()
result_file_psm3.close()
result_file_psm6.close()
result_file_psm13.close()
result_file_all.close()