import re
import string
import Levenshtein

TXT_DIR_RAW = 'texts_processed/GS/' # directory storing OCR result from the original images
TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/post-processing_25%_GS_notfinal.txt' #location storing all of the results

LEV_limit = 0.25 #max difference, percentage (Levenshtein distance compared to the length of the string)

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

def remove_empty_ingredients(list):
    try:
        while True:
            list.remove("")
    except ValueError:
        pass
    return list


delimiters = ["(", ")", "[", "]", "{", "}", ":", "-", "—", ";", "."]

#get the actual ingredient list for validation
def clean_text_get_list(text):
    processed = re.sub("\d*[.,]?\d*\s*%", "", text) #remove 2,3% , 1.5 % utt.

    for char in delimiters:
        processed = processed.replace(char, ",")
    processed = processed.replace("-\n", "") #ignore "pārnesumi jaunā rindā"
    processed = processed.replace("–\n", "") #ignore "pārnesumi jaunā rindā"
    processed = processed.replace("\n", "") #ignore new lines
    processed = processed.replace("*", "") #ignore asterisks

    list_tru = processed.split(',') #make a list of all ingredients
    list_tru = [s.strip() for s in list_tru if s != '' and s!= ' '] #remove extra spaces
    
    return remove_empty_ingredients(list_tru)

#create a list of 3-word-long-ingredients from OCR text
def clean_text_get_list_3_word_ing(text):
    processed = re.sub("\d*[.,]?\d*\s*%", "", text) #remove 2,3% , 1.5 % utt.
    all_words_identified = [word.strip(string.punctuation) for word in processed.split()] #split into words and remove extra chars
    #all_words_identified = remove_empty_ingredients(all_words_identified)
    all_words_identified = [s.strip() for s in all_words_identified if s != '' and s!= ' '] #remove extra spaces and empty strings
    list = [all_words_identified[i] + " " + all_words_identified[i+1] + " " + all_words_identified[i+2] for i in range(0,len(all_words_identified)-2)]
    return list



def get_all_words(list):
    if(list == []): return ""
    text = ""
    #if(i == 0): i = 2
    for ing in list:
        if(ing == ""): continue
        list_ing = ing.split()
        text = text + list_ing[0] + " "
    last_ing = list[len(list)-1].split()
    last_ing.pop(0)
    for t in range(0, len(last_ing)):
        text = text + last_ing[t] + " "
    return text.split()
    
#split the given text into a list of i-words long ingredients
def split_text_into_ingredients(all_words_identified, i):
    if(i == 1):
        return all_words_identified
    elif(i == 2):
        list = [all_words_identified[i] + " " + all_words_identified[i+1] for i in range(0,len(all_words_identified)-1)]
        return list
    elif(i == 3):
        list = [all_words_identified[i] + " " + all_words_identified[i+1] + " " + all_words_identified[i+2] for i in range(0,len(all_words_identified)-2)]
        return list
    else:
        return []

#i - 0 means 2-word ing list needed, 1 - 1-word, 3 or 2 - 3-word
def get_ing_list(list, i):
    if(list == []): return []
    all_words_identified = get_all_words(list)
    k = 1
    if(i == 0): k = 2
    elif(i == 3 or i == 2): k = 3
    return split_text_into_ingredients(all_words_identified, k)
    

list_removed = []
#remove duplicates when an AB ingredient found in 2-word or 3-word list
def remove_duplicates(list_raw, list_removed, i):
    if(list_removed == []): return list_raw    
    if(i == 0): word_count = 2
    elif(i == 1): word_count = 1
    elif(i == 2): word_count = 0
    for word in list_removed:
        for k in range(0, word_count):
            for ing in list_raw:
                if(word in ing):
                    list_of_words = ing.split()
                    if(len(list_of_words) == 1):
                        try:
                            list_raw.remove(word)
                            break
                        except ValueError:
                            continue
                    try:
                        list_of_words.remove(word)
                        list_raw[list_raw.index(ing)] = ' '.join(list_of_words)
                        if(list_raw == ' '): list_raw.remove(' ')
                    except ValueError:
                        pass
    return list_raw, []

#do post-processing for images from 1 to 20 for both non-vegan and vegan products
product_type = ["n"]#,"v"]
for t in product_type:
    for x in range(1, 101):
        img_name = t + str(x)
        list_removed = []

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

        #manipulation of brackets for allowing regex functions later in the code
        raw_processed = raw_processed.replace("]", "}")
        raw_processed = raw_processed.replace("[", "{")
        raw_processed = raw_processed.replace(")", "}")
        raw_processed = raw_processed.replace("(", "{")
        raw_processed = raw_processed.replace(";", ",")

        #POST-PR: remove all characters before "sastāvdaļas" or sastāvs
        beginning = ""
        #split text in words for processing, removing all punctuation chars if there are any on the beginning or end of the words
        all_words_identified = [word.strip(string.punctuation) for word in raw_processed.split()]
        all_words_identified = [s.strip() for s in all_words_identified if s != '' and s!= ' '] #remove extra spaces and empty strings
        #all_words_identified = remove_empty_ingredients(all_words_identified)
        
        #iterate over all words
        for word in all_words_identified:
            if(word == "sastāvdaļas" or word == "sastāvs"):
                beginning = word
        if(beginning == ""): #identical match has not been found
            for word in all_words_identified: #do similarity check - if similar enough, assume it is the beginning of ingredient list
                if(Levenshtein.distance(word, "sastāvdaļas")/len("sastāvdaļas") <= LEV_limit):
                    beginning = word
                elif(Levenshtein.distance(word, "sastāvs") /len("sastāvs") <= LEV_limit):
                    beginning = word
        if(beginning != ""): #beginning of ingredient list has been identified
            split_raw = raw_processed.split(beginning, 1) #remove everything before that
            if len(split_raw) > 1: 
                raw_processed = split_raw[1]
            else:
                raw_processed = split_raw[0]
        
        #POST-PR. common OCR error -> E numbers identified as a numerical value (E = 6). Fixing that
        for word in all_words_identified:
            if(word.isdigit()):
                number = int(word)
                if(number >= 6100 and number <= 61999):
                    new_E = "e" + str(number - 6000)
                    raw_processed = raw_processed.replace(word, new_E)

        #POST-PR. Exception handling. When mentions of animal based ingredients should be ignored
        exact_match_exception = ["bez", "nav", "saturēt", "nesatur"]
        for exception in exact_match_exception: #assess each exception key word
            if exception in all_words_identified: #if present in the text
                raw_processed = re.sub("\s*" + exception + "[^;.{}():-]*", "", raw_processed) #remove the whole word. Includes, e.g., "kokosriekstu piens"

        #POST-PR. Levenshtein Exception handling. When mentions of animal based ingredients should be ignored
        exact_match_exception = ["saturēt", "nesatur"]
        for exception in exact_match_exception: #assess each exception key word
            for word in all_words_identified:
                if(Levenshtein.distance(word, exception) /len(exception) <= LEV_limit):
                    raw_processed = re.sub("\s*" + word + "[^;.{}():-]*", "", raw_processed) #remove the whole word. Includes, e.g., "kokosriekstu piens"


        exact_match_exception_ing = ["kakao sviests", "riekstu sviests", "riekstu piens", "zirņu piens", "cūku pupas", "kakao sviesta", "riekstu sviesta", "riekstu piena", "zirņu piena", "cūku pupu", "sēklu sviests", "sēklu sviesta"]
        #POST-PR. Exception handling. When mentions of animal based ingredients should be ignored
        for exception in exact_match_exception_ing: #assess each exception key word
            if exception in raw_processed: #if present in the text
                raw_processed = re.sub("\w*" + exception + "\w*", "", raw_processed) #remove the whole word. Includes, e.g., "kokosriekstu piens"

        #SPLITTING into a list of ingredients
        list_raw = clean_text_get_list_3_word_ing(raw_processed)
        #print(list_raw)
        #POST-PR. Levenshtein exception handling. When mentions of animal based ingredients should be ignored
        #loop through all ingredients and check if they are exceptions
        for i in range (0,3): #loop 3 times - for 3-word, 2-word, 1-word ingredients
            for ingredient in list_raw:
                for exception in exact_match_exception_ing:
                    if(Levenshtein.distance(ingredient, exception) /len(exception) <= LEV_limit):
                        list_raw.remove(ingredient)
                        list_removed = ingredient.split()
                        list_raw, list_removed = remove_duplicates(list_raw, list_removed, i)
                        break #move on to next ingredient
            list_raw = get_ing_list(list_raw, i)
            list_removed = []
                
        

        list_raw = get_ing_list(list_raw, 3)
        list_removed = []
        #print(list_raw)
        #FEATURE
        list_raw_n = [] #animal based ingredients identified in the product
        list_similars = [] #list of tuples when match is <100% - (ing identified, animal based ingredient from the check list)
        for i in range(0,3):
            #loop through all ingredients and check if they are animal based
            for ingredient in list_raw:
                if ingredient in list_ingredients:
                    list_raw_n.append(ingredient)
                    list_raw.remove(ingredient)
                    list_removed = ingredient.split()                
                    list_raw, list_removed = remove_duplicates(list_raw, list_removed, i)
            list_raw = get_ing_list(list_raw, i)
        #print(list_raw)


        #POST-PR Levenshtein comparison (high complexity)
        #will approve weird "ingredients" (because farther away from Latvian lang)
        #e.g., 'kakaom rrn ppāū PIENO sikeīgi maa autoru' (n4)
        for i in range(0,3):                
            for ingredient in list_raw: #each identified ingredient
                if ingredient not in list_raw_n:
                    for ing_animal in list_ingredients:
                            #'vajpiena piem o7 es adalami' -> Levenshtein is high because of all of the extra words
                            if(Levenshtein.distance(ingredient, ing_animal) /len(ingredient) <= LEV_limit): #how similar should be?
                                list_raw_n.append(ingredient)
                                list_raw.remove(ingredient)
                                list_raw, list_removed = remove_duplicates(list_raw, ingredient.split(), i)
                                list_similars.append((ingredient, ing_animal))
                                break
            list_raw = get_ing_list(list_raw, i)

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
            print("Something doesn't add up. Can't check and compare animal ingredients list because samples are given different")
            print(list_check[0])
            print(img_name)
        else:
            check_nr_total = list_check[1] #total nr of ingredients check
            check_nr_n = list_check[2] #nr of animal based ingredients check
            #print(list_raw_n)
            if(t == "n"): #non-vegan product
                list_check_ingr_n = list_check[3].split(",") #check animal based ingredient list
                ing_animal_missed = list_check_ingr_n.copy() #missed - AB ingredients in the product not recognized by the solution
                for detected_ingr in list_raw_n: #loop through all the AB ingreidents "found"
                    if detected_ingr in ing_animal_missed: #if they are actually in the product, it is a match (TP)
                        #print(detected_ingr)  
                        try:
                            ing_animal_missed.remove(detected_ingr)
                            ing_animal_overlap.append(detected_ingr)
                            continue
                        except ValueError: #sometimes there can be dublicates, if, e.g., word is the same in several languages. Only one of the times it is a correct identification
                            ing_animal_extra.append(detected_ingr) #add as wrongly flagged ingredient
                    else:
                        found = 0  
                        #print(ing_animal_missed)                                
                        for ing in ing_animal_missed: #maybe identified ingredient contains extra words
                            if(ing in detected_ingr): #if they overlap, it is a match
                                ing_animal_missed.remove(ing)
                                ing_animal_overlap.append(detected_ingr)
                                found = 1
                                break
                            elif(detected_ingr in ing):
                                #print(detected_ingr)
                                #print(ing)
                                ing_animal_missed.remove(ing)
                                ing_animal_overlap.append(detected_ingr)
                                found = 1
                                break
                        if(found == 1): continue
                        for tuple in list_similars: #because of OCR errors, correctly identified ingredients might have spelling mistakes
                            if(tuple[0] == detected_ingr and found == 0):                                
                                for ing in ing_animal_missed: #look at the AB ingredients in the product not yet matched
                                    if((tuple[1] in ing) or (ing in tuple[1])): #if identified ingredient is one of them
                                        ing_animal_missed.remove(ing)
                                        ing_animal_overlap.append(detected_ingr)
                                        list_similars.remove(tuple)
                                        found = 1
                                        break
                            if(found == 1): break
                        #elif overlap coefficient of chars >75%?
                        if(found == 0):
                            ing_animal_extra.append(detected_ingr)
        #print(ing_animal_missed)
        print(img_name, check_nr_total, str(len(list_tru)), str(len(list_raw)), list_tru, [raw_processed], check_nr_n, str(len(list_raw_n)), list_check_ingr_n, list_raw_n, str(len(ing_animal_overlap)), str(len(ing_animal_missed)), str(len(ing_animal_extra)), ing_animal_overlap, ing_animal_missed, ing_animal_extra, sep = ";", file = txt_combined)

txt_combined.close()