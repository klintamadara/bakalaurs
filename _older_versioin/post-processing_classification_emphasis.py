import re
import Levenshtein

TXT_DIR_RAW = 'texts_raw/' # directory storing OCR result from the original images
TXT_DIR_BW = 'texts_processed/B&W/' # directory storing OCR result from the pre-processed images
TXT_DIR_P2 = 'texts_processed/part2_split_ingredients' # directory storing post-processed text -> splitting ingredients
TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/' #directory storing all of the results
TXT_DIR_P1 = 'texts_processed/part1/' # directory storing post-processed text -> removed before "sastāvdaļas"
#TXT_DIR_INGR_CHECK 

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
    processed = re.sub("\d*[.,]?\d*\s*%", "", text) #remove all 2,3%

    processed = processed.replace("(", ",")
    processed = processed.replace(")", ",")
    processed = processed.replace("[", ",")
    processed = processed.replace("]", ",")
    processed = processed.replace(":", ",")
    #processed = processed.replace("-", ",") fruktozes-glikozes sīrups, mono-
    processed = processed.replace(";", ",")
    processed = processed.replace(".", ",")
    processed = processed.replace("\n", "")
    # { } ??
    #"^\d*[.,]?\d*\s*%$"mg
    #"\d*[.,]?\d*\s*%"mg
    #print(processed)
    list_tru = processed.split(',') #make a list of all ingredients
    list_tru = [s.strip() for s in list_tru if s != '' and s!= ' '] #remove extra spaces
    #print(list_tru)
    return list_tru


#do post-processing for images from 1 to 20 for both non-vegan and vegan products
product_type = ["n","v"]
for t in product_type:
    for x in range(1, 21):
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

        #remove all characters before "sastāvdaļas"
        split_raw = raw_processed.split("sastāvdaļas", 1)
        if len(split_raw) > 1: 
            raw_processed = split_raw[1]

        """
        #todo: delete everything after until a stop (., \n)
        split_raw = raw_processed.split("var saturēt", 1)
        if len(split_raw) > 1: 
            raw_processed = split_raw[0]
        """
        list_raw = clean_text_get_list(raw_processed)

        #animal based ingredient list included in the product
        list_raw_n = []
        #loop through all ingredients and check if they are animal based
        for ingredient in list_raw:
            if ingredient in list_ingredients:
                list_raw_n.append(ingredient)
            #extra: ingredient contains animal product within
            else:
                for ing_animal in list_ingredients:
                    if ing_animal in ingredient:
                        list_raw_n.append(ingredient)
                        break #one keyword found is enough, put it in the list and move on
        
        #EXTRA Levenshtein comparison (high complexity)
        #will approve weird "ingredients" (because farther away from Latvian lan)
        #e.g., 'kakaom rrn ppāū PIENO sikeīgi maa autoru' (n4)
        for ingredient in list_raw:
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

        list_check_ingr_n = []
        ing_animal_overlap = []
        ing_animal_missed = []
        ing_animal_extra = []
        check_nr_total = 0
        check_nr_n = 0

        #extract check data from the manually prepared file for testing
        if(t == "v"):
            ing_animal_extra = list_raw_n
            list_check = list_ingredients_check[x-1+20].split(";")
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

"""
        #remove first character if it is ":"
        if raw_processed[0] == ':':
            raw_processed = raw_processed[1:]

        
    
"""

"""
        #print(list_tru)
        print("Nr of ingredients in the product:" + str(len(list_tru)))
        print("Ingredients in the product: ", *list_tru, sep = ",")
        print("Nr of ingredients identified: " + str(len(list_raw)))
        #print("All ingredients identified: ", *list_raw, sep = ",")
        print("Nr of animal based ingredients identified: " + str(len(list_raw_n)))
        #print(*list_raw_n, sep = ",")
        #print("Animal based ingredients: " + list_raw_n)
        #print(list_raw_n)
        #print(list_raw)
        """

        #print(img_name, ";", str(len(list_tru)), ";", *list_tru, ";", str(len(list_raw)), ";", *list_raw, ";", str(len(list_raw_n)), ";", *list_raw_n, sep = ",", file = txt_combined)
        #print(img_name, ";", str(len(list_tru)), ";", list_tru, ";", str(len(list_raw)), ";", list_raw, ";", str(len(list_raw_n)), ";", list_raw_n, file = txt_combined)
        