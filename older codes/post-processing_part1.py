#what is the overlap between 2 strings? If one is subset of another, index is 1.
def overlap_index_char(str1, str2):
    common_chars = set(str1).intersection(str2)
    common_chars_nr = len(common_chars)
    print("Overlap:")
    print(common_chars_nr/min(len(str1), len(str2)))
    return common_chars_nr/min(len(str1), len(str2))
"""
def overlap_index_char(str1, str2):
    common_chars = ''.join(sorted(set(str1) & set(str2), key = str1.index))
    common_chars_nr = len(common_chars)
    print("Overlap:")
    print(common_chars_nr/min(len(str1), len(str2)))
    return common_chars_nr/min(len(str1), len(str2))
"""


TXT_DIR_RAW = 'texts_raw/' # directory storing OCR result from the original images
TXT_DIR_BW = 'texts_processed/B&W/' # directory storing OCR result from the pre-processed images
#TXT_DIR_ING = 'texts_processed/ingredients/' # directory storing post-processed text -> removed before "sastāvdaļas"
TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/' #directory storing all of the results
TXT_DIR_P1 = 'texts_processed/part1/' # directory storing post-processed text -> removed before "sastāvdaļas"

#"sastāvdaļas" was recognized in images and everything before that - erased
sastavdalas_erased = 0

#do post-processing for images from 1 to 20
for x in range(1, 21):
    img_name = "v" + str(x)

    #prepare the OCR result from original image for post-processing
    txt_raw = open(TXT_DIR_RAW + img_name + ".txt", "r", encoding='UTF-8')
    content_raw = txt_raw.read()
    txt_raw.close()
    content_raw = str.lower(content_raw)
    #i = content_raw.find("sastāvdaļas") #finds index at which the string starts

    #remove all characters before "sastāvdaļas"
    split_raw = content_raw.split("sastāvdaļas", 1)
    if len(split_raw) > 1: 
        sastavdalas_erased = 1
        raw_processed = split_raw[1]

    #remove first character if it is ":"
    if raw_processed[0] == ':':
        raw_processed = raw_processed[1:]

    #remove first character if it is " "
    if raw_processed[0] == ' ':
        raw_processed = raw_processed[1:]

    #remove all characters before "uzturvērtība, informācija par uzturvērtību, var saturēt, enerģētiskā vērtība,
    # 100 g/ml produkta uzturvērtība/vidēji satur, ražotājs, iepakots aizsargatmosfērā, ražots xx,
    # uzglabāt (ir arī sākumā), ieteicams līdz (ir arī sākumā), pēc atvēršanas izlietot, alergēni: xx"
    
    split_raw = raw_processed.split("var saturēt", 1)
    if len(split_raw) > 1: 
        raw_processed = split_raw[0]

    split_raw = raw_processed.split("uzturvērtība", 1)
    if len(split_raw) > 1: 
        raw_processed = split_raw[0]

    split_raw = raw_processed.split("informācija par uzturvērtību", 1)
    if len(split_raw) > 1: 
        raw_processed = split_raw[0]
    
    split_raw = raw_processed.split("enerģētiskā vērtība", 1)
    if len(split_raw) > 1: 
        raw_processed = split_raw[0]

    split_raw = raw_processed.split("100 g produkta", 1)
    if len(split_raw) > 1: 
        raw_processed = split_raw[0]

    split_raw = raw_processed.split("100 ml produkta", 1)
    if len(split_raw) > 1: 
        raw_processed = split_raw[0]

    #can be sure that first is the list of ingredients, and the rest is unnecessary
    if sastavdalas_erased == 1:
        split_raw = raw_processed.split("ražot", 1)
        if len(split_raw) > 1: 
            raw_processed = split_raw[0]

        split_raw = raw_processed.split("iepakots aizsargatmosfērā", 1)
        if len(split_raw) > 1: 
            raw_processed = split_raw[0]

        split_raw = raw_processed.split("ieteicams līdz", 1)
        if len(split_raw) > 1: 
            raw_processed = split_raw[0]
        
        split_raw = raw_processed.split("uzglabāt", 1)
        if len(split_raw) > 1: 
            raw_processed = split_raw[0]

        split_raw = raw_processed.split("pēc atvēršanas", 1)
        if len(split_raw) > 1: 
            raw_processed = split_raw[0]
   

    txt_raw_new = open(TXT_DIR_P1 + img_name + ".txt", 'w', encoding='UTF-8')
    print(raw_processed, file = txt_raw_new)
    txt_raw_new.close()
    sastavdalas_erased = 0