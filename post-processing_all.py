import re
import string

TXT_DIR_RAW = 'texts_raw/' # directory storing OCR result from the original images
TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/post-processing_all.txt' #location storing all of the results

#prepare animal based ingredient list
txt_file = open("list.txt", "r", encoding='UTF-8')
file_content = txt_file.read()
list_ingredients = file_content.split("\n")
txt_file.close()

#prepare animal based ingredient check list for each product
txt_file = open("text_actual_animal_ingr_check.txt", "r", encoding='UTF-8')
file_content = txt_file.read()
list_ingredients_check = file_content.split("\n") #each line format: type;nr;nr;ingredients
txt_file.close()

#prepare document in which to write
txt_combined = open(TXT_DIR_RSLTS, 'w', encoding='UTF-8')
print("IMG;Ingr nr total - file;Ingr nr;Ingr nr identified;Ingr list;Ingr identified;Nr AB ingr - file;Nr AB ingr identified;AB ingr list - file;AB ingr list identified;Overlap (TP);Missed (FN);Extra (FP);AB ingr overlap (TP);AB ingr missed (FN);Wrongly flagged (FP)", 
file = txt_combined)

delimiters = ["(", ")", "[", "]", "{", "}", ":", "-", ";", "."]
#create a list from OCR text
def clean_text_get_list(text):
    processed = re.sub("\d*[.,]?\d*\s*%", "", text) #remove 2,3% , 1.5 % utt.

    for char in delimiters:
        processed = processed.replace(char, ",")
    processed = processed.replace("-\n", "") #ignore "pārnesumi jaunā rindā"
    processed = processed.replace("–\n", "") #ignore "pārnesumi jaunā rindā"
    processed = processed.replace("\n", "") #ignore new lines
    processed = processed.replace("*", "") #ignore new lines

    list_tru = processed.split(',') #make a list of all ingredients
    list_tru = [s.strip() for s in list_tru if s != '' and s!= ' '] #remove extra spaces
    #remove empty ingredients
    try:
        while True:
            list_tru.remove("")
    except ValueError:
        pass
    return list_tru


#do post-processing for images from 1 to 20 for both non-vegan and vegan products
product_type = ["n","v"]
for t in product_type:
    for x in range(1, 101):
        img_name = t + str(x)

        #prepare the actual ingredients list for testing purposes
        txt_tru = open(TXT_DIR_TRU + img_name + ".txt", "r", encoding='UTF-8')
        content_tru = str.lower(txt_tru.read()) #lowercase
        txt_tru.close()
        list_tru = clean_text_get_list(content_tru)

        #prepare the OCR result from original image for post-processing
        txt_raw = open(TXT_DIR_RAW + img_name + ".txt", "r", encoding='UTF-8')
        content_raw = txt_raw.read()
        txt_raw.close()
        raw_processed = str.lower(content_raw)

        raw_processed = raw_processed.replace("]", "}")
        raw_processed = raw_processed.replace("[", "{")
        raw_processed = raw_processed.replace(")", "}")
        raw_processed = raw_processed.replace("(", "{")

        #FEATURE POST-PR: remove all characters before "sastāvdaļas" or sastāvs
        beginning = ""
        #split text for processing, removing all punctuation signs first,
        #if there are any on the beginning or end of the words
        all_words_identified = [word.strip(string.punctuation) for word in raw_processed.split()]
        #iterate over all words
        for word in all_words_identified:
            if(word == "sastāvdaļas" or word == "sastāvs"):
                beginning = word
        if(beginning != ""): #beginning of ingredient list has been identified
            split_raw = raw_processed.split(beginning, 1) #remove everything before that
            if len(split_raw) > 1: 
                raw_processed = split_raw[1]
            else:
                raw_processed = split_raw[0]
        
        #FEATURE POST-PR. common OCR error -> E numbers identified as a numerical value (E = 6). Fixing that
        for word in all_words_identified:
            if(word.isdigit()):
                number = int(word)
                if(number >= 6100 and number <= 61999):
                    new_E = "e" + str(number - 6000)
                    raw_processed = raw_processed.replace(word, new_E)

        #FEATURE POST-PR. Exception handling. When mentions of animal based ingredients should be ignored
        exact_match_exception = ["bez", "nav", "saturēt", "nesatur"]
        for exception in exact_match_exception: #assess each exception key word
            if exception in all_words_identified: #if present in the text
                raw_processed = re.sub("\s*" + exception + "[^;.{}():-]*", "", raw_processed) #remove the whole word. Includes, e.g., "kokosriekstu piens"

        #FEATURE POST-PR. Exception handling. When mentions of animal based ingredients should be ignored
        exact_match_exception_ing = ["kakao sviests", "riekstu sviests", "riekstu piens", "zirņu piens", "cūku pupas"]
        for exception in exact_match_exception_ing: #assess each exception key word
            if exception in raw_processed: #if present in the text
                raw_processed = re.sub("\w*" + exception + "\w*", "", raw_processed) #remove the whole word. Includes, e.g., "kokosriekstu piens"

        #SPLITTING into a list of ingredients
        list_raw = clean_text_get_list(raw_processed)
        
        list_raw_n = [] #animal based ingredient identified in the product
        #loop through all ingredients and check if they are animal based
        for ingredient in list_raw:
            if ingredient in list_ingredients:
                list_raw_n.append(ingredient)
            else: #ingredient contains animal product keyword within -> also counts
                separate_ingredients = [word.strip(string.punctuation) for word in ingredient.split()]
                for word in separate_ingredients:
                    if word in list_ingredients:
                        list_raw_n.append(ingredient)
                        break #one keyword found is enough, put it in the list and move on

        list_check_ingr_n = []
        ing_animal_overlap = []
        ing_animal_missed = []
        ing_animal_extra = []
        check_nr_total = 0
        check_nr_n = 0

        #extract check data from the manually prepared file for testing
        if(t == "v"):
            ing_animal_extra = list_raw_n
            list_check = list_ingredients_check[x+100].split(";")
        else: #"n"
            list_check = list_ingredients_check[x].split(";")

        #make sure to look at the correct product(compare IDs)
        if(list_check[0] != img_name):
            print("Something doesn't add up. Can't check and compare animal ingredients list")
        else:
            check_nr_total = list_check[1] #total nr of ingredients check
            check_nr_n = list_check[2] #nr of animal based ingredients check
            
            if(t == "n"):
                list_check_ingr_n = list_check[3].split(",") #check animal based ingredient list
                ing_animal_missed = list_check_ingr_n
                for detected_ingr in list_raw_n:
                    if detected_ingr in list_check_ingr_n:
                        ing_animal_overlap.append(detected_ingr)
                        ing_animal_missed.remove(detected_ingr)
                    else:
                        ing_animal_extra.append(detected_ingr)
       
        print(img_name, check_nr_total, str(len(list_tru)), str(len(list_raw)), list_tru, list_raw, check_nr_n, str(len(list_raw_n)), list_check_ingr_n, list_raw_n, str(len(ing_animal_overlap)), str(len(ing_animal_missed)), str(len(ing_animal_extra)), ing_animal_overlap, ing_animal_missed, ing_animal_extra, sep = ";", file = txt_combined)

txt_combined.close()