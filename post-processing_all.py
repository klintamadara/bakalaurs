import re
import string
import Levenshtein

TXT_DIR_RAW = 'texts_raw/' # directory storing OCR result from the original images
TXT_DIR_BW = 'texts_processed/B&W/' # directory storing OCR result from the pre-processed images
TXT_DIR_P2 = 'texts_processed/part2_split_ingredients' # directory storing post-processed text -> splitting ingredients
TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/' #directory storing all of the results
TXT_DIR_P1 = 'texts_processed/part1/' # directory storing post-processed text -> removed before "sastāvdaļas"
#TXT_DIR_INGR_CHECK 

delimiters = ["(", ")", "[", "]", "{", "}", ":", "-", ";", "."]
#Python delimiters: (    )    [    ]    {    }   ,    :    .    `    =    ;

#what is the overlap between 2 strings? If one is subset of another, index is 1.
def overlap_index_char(str1, str2):
    common_chars = ''.join(sorted(set(str1) & set(str2), key = str1.index))
    common_chars_nr = len(common_chars)
    return common_chars_nr/min(len(str1), len(str2))

#find position of the first occurence of a delimiter in a string
def find_end(str):
    end = float('inf')
    for char in delimiters:
        position = str.find(char)
        if(position < end and position != -1):
            end = position
    if(end == float('inf')):
        end = -1
    return end

def delete_occurences(raw_processed, exception):
    position = raw_processed.find(exception) #where it is located in the string
    #remove it while it exists in the string as a word (not within a word, e.g., "bezdibenis")
    if(position == 0):
        char_before = ""
    else:
        char_before = raw_processed[position - 1]
    if(position + len(exception) >= len(raw_processed)):
        char_after = ""
    else:
        char_after = raw_processed[position + len(exception)]
    print(exception)
    print(position)
    print(char_before.isalpha())
    print(char_after.isalpha())
    while((position > -1 and char_before.isalpha() == False and char_after.isalpha() == False)):
        print("yess")
        split_exc = raw_processed.split(exception, 1) #remove everything before that
        #locate and find where the related words (AB ingredients) end
        if len(split_exc) > 1: 
            tail = split_exc[1]
        else:
            tail = split_exc[0] #exception key word was the first (or last?) word in the string
        end_delimiter = find_end(tail)
        if(end_delimiter == -1 or end_delimiter == 0): #couldn't find an appropriate delimiter or it was the first char, i.e., everything after key word is assumed to be relevant (dismissable)
            raw_processed = split_exc[0]
        else:
            split_tail_list = tail.split(tail[end_delimiter - 1],1) #split so that delimiter is kept
            if len(split_tail_list) > 1: 
                split_tail = split_tail_list[1]
            else:
                split_tail = split_tail_list[0]
            raw_processed = split_exc[0] + split_tail #combine info before and after the exception
        position = raw_processed.find(exception) #find next occurence
        if(position == -1): #no more occurences
            break
        elif(position == 0): #in the beginning, no char before the key word
            char_before = ""
        else:
            char_before = raw_processed[position - 1]
        if(position + len(exception) >= len(raw_processed)): #key word at the end
            char_after = ""
        else:
            char_after = raw_processed[position + len(exception)]
    return raw_processed





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
txt_combined = open(TXT_DIR_RSLTS + "split_ingredients_comparison_all.txt", 'w', encoding='UTF-8')
print("IMG;Ingr nr total - file;Ingr nr;Ingr nr identified;Ingr list;Ingr identified;Nr AB ingredients - file;Nr AB ingredients identified;AB ingr list - file;AB ingr list identified;Overlap;Missed;Extra;AB ingr overlap;AB ingr missed (only in file);False positives (ingr wrongly flagged as AB)", 
file = txt_combined)

def clean_text_get_list(text):
    processed = re.sub("\d*[.,]?\d*\s*%", "", text) #remove 2,3% , 1.5 % utt.

    for char in delimiters:
        processed = processed.replace(char, ",")

    processed = processed.replace("-\n", "") #ignore "pārnesumi jaunā rindā"
    processed = processed.replace("–\n", "") #ignore "pārnesumi jaunā rindā"
    processed = processed.replace("\n", "") #ignore new lines

    list_tru = processed.split(',') #make a list of all ingredients
    list_tru = [s.strip() for s in list_tru if s != '' and s!= ' '] #remove extra spaces
    #print(list_tru)
    return list_tru


#do post-processing for images from 1 to 20 for both non-vegan and vegan products
product_type = ["n"]#,"v"]
for t in product_type:
    for x in range(1, 2):
        img_name = t + str(x)
        #print("\n" + img_name)

        #prepare the actual ingredients list for testing purposes
        txt_tru = open(TXT_DIR_TRU + img_name + ".txt", "r", encoding='UTF-8')
        content_tru = txt_tru.read()
        txt_tru.close()
        list_tru = clean_text_get_list(content_tru)

        #prepare the OCR result from original image for post-processing
        txt_raw = open(TXT_DIR_RAW + img_name + ".txt", "r", encoding='UTF-8')
        content_raw = txt_raw.read()
        txt_raw.close()
        raw_processed = str.lower(content_raw)
        #i = content_raw.find("sastāvdaļas") #finds index at which the string starts

        #!!!!!!!!!!!!!!!!!!!
        raw_processed = "cukurs, olbaltums, milti. Var saturēt kakao. piens"

        #FEATURE POST-PR: remove all characters before "sastāvdaļas" or sastāvs
        beginning = ""
        #split text for processing, removing all punctuation signs first,
        #if there are any on the beginning or end of the words
        all_words_identified = [word.strip(string.punctuation) for word in raw_processed.split()]
        #iterate over all words
        for word in all_words_identified:
            if(word == "x   sastāvdaļas" or word == "sastāvs"):
                beginning = word
        if(beginning == ""): #identical match has not been found
            for word in all_words_identified: #do similarity check - if similar enough, assume it is the beginning of ingredient list
                if(Levenshtein.distance(word, "sastāvdaļas") <= 1):
                    beginning = word
                elif(Levenshtein.distance(word, "sastāvs") <= 1):
                    beginning = word
        if(beginning != ""): #beginning of ingredient list has been identified
            split_raw = raw_processed.split(beginning, 1) #remove everything before that
            raw_processed = split_raw[1]
        
        #FEATURE POST-PR. common OCR error -> E numbers identified as a numerical value (E = 6). Fixing that
        for word in all_words_identified:
            if(word.isdigit()):
                number = int(word)
                if(number >= 6100 and number <= 61999):
                    new_E = "e" + str(number - 6000)
                    raw_processed = raw_processed.replace(word, new_E)

        #FEATURE POST-PR. Exception handling. When mentions of animal based ingredients should be ignored
        exact_match_exception = ["bez", "nav"]
        for exception in exact_match_exception: #assess each exception key word
            if exception in all_words_identified: #if present in the text
                raw_processed = delete_occurences(raw_processed, exception)
        
        approx_match_exception = ["Var saturēt", "nesatur"]
        for exception in approx_match_exception:
            if(overlap_index_char(exception, raw_processed) >= 0.85):
                print()
                print("yes")
                raw_processed = delete_occurences(raw_processed, exception)

        print(raw_processed)


        """
        if(overlap_index_char(" bez ", raw_processed) == 1):
            split_ = raw_processed.split(" bez ", 1) #remove everything before that
            raw_processed = split_raw[1]
            find_end
        """
        """
        #todo: delete everything after until a stop (., \n)
        split_raw = raw_processed.split("var saturēt", 1)
        if len(split_raw) > 1: 
            raw_processed = split_raw[0]
        """
        #SPLITTING into a list of ingredients
        list_raw = clean_text_get_list(raw_processed)

        #DELETE list_raw = ["piens", "ogas", "pienskābe", "cāļa", "kviešu milti", "piena pulveris", "baltums olu"]
        
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

        """
        #EXTRA Levenshtein comparison (high complexity)
        #will approve weird "ingredients" (because farther away from Latvian lang)
        #e.g., 'kakaom rrn ppāū PIENO sikeīgi maa autoru' (n4)
        for ingredient in list_raw: #each identified ingredient
            if ingredient not in list_raw_n:
                for ing_animal in list_ingredients:
                        #'vajpiena piem o7 es adalami' -> Levenshtein is high because of all of the extra words
                        if(Levenshtein.distance(ingredient, ing_animal) <= 1): #how similar should be?
                            list_raw_n.append(ingredient)
                            break
                        else:
                            separate_words = ingredient.split()
                            for word in separate_words:
                                if(Levenshtein.distance(word, ing_animal) <= 1): #how similar should be?
                                    list_raw_n.append(ingredient)
                                    break
        """

        list_check_ingr_n = []
        ing_animal_overlap = []
        ing_animal_missed = []
        ing_animal_extra = []
        check_nr_total = 0
        check_nr_n = 0

        #extract check data from the manually prepared file for testing
        if(t == "v"):
            ing_animal_extra = list_raw_n
            list_check = list_ingredients_check[x+50].split(";")
        else: #"n"
            list_check = list_ingredients_check[x-1].split(";")

        #make sure to look at the correct product(compare IDs)
        if(list_check[0] != img_name):
            print("Something doesn't add up. Can't check and compare animal ingredients list")
        else:
            check_nr_total = list_check[1] #total nr of ingredients check
            check_nr_n = list_check[2] #nr of animal based ingredients check
            
            if(t == "n"):
                list_check_ingr_n = list_check[3].split(",") #check animal based ingredient list
                for detected_ingr in list_raw_n:
                    if detected_ingr in list_check_ingr_n:
                        ing_animal_overlap.append(detected_ingr)
                    else:
                        ing_animal_extra.append(detected_ingr)
                for ingr in list_check_ingr_n:
                    if(ingr not in list_raw_n):
                        ing_animal_missed.append(ingr)
        """
        print(list_raw_n)
        print(list_check_ingr_n)
        print(ing_animal_overlap)
        print(ing_animal_missed)
        print(ing_animal_extra)
        """
        print(img_name, check_nr_total, str(len(list_tru)), str(len(list_raw)), list_tru, list_raw, check_nr_n, str(len(list_raw_n)), list_check_ingr_n, list_raw_n, str(len(ing_animal_overlap)), str(len(ing_animal_missed)), str(len(ing_animal_extra)), ing_animal_overlap, ing_animal_missed, ing_animal_extra, sep = ";", file = txt_combined)


txt_combined.close()