TXT_DIR_RAW = 'texts_raw/' # directory storing OCR result from the original images
TXT_DIR_BW = 'texts_processed/B&W/' # directory storing OCR result from the pre-processed images
TXT_DIR_P2 = 'texts_processed/part2_split_ingredients' # directory storing post-processed text -> splitting ingredients
TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/' #directory storing all of the results
TXT_DIR_P1 = 'texts_processed/part1/' # directory storing post-processed text -> removed before "sastāvdaļas"

#prepare animal based ingredient list
txt_file = open("list.txt", "r", encoding='UTF-8')
file_content = txt_file.read()
list_ingredients = file_content.split("\n")
txt_file.close()

#prepare document in which to write
txt_combined = open(TXT_DIR_RSLTS + "split_ingredients_comparison_all.txt", 'w', encoding='UTF-8')
print("Nr of ingredients in the product;Ingredients in the product;Nr of ingredients identified;Ingredients identified;Nr of animal based ingredients identified;Animal based ingredients identified", 
file = txt_combined)

product_type = ["n", "v"]

#do post-processing for images from 1 to 20 for both non-vegan and vegan products
for t in product_type:
    for x in range(1, 21):
        img_name = t + str(x)
        #print("\n" + img_name)

        #prepare the actual ingredients list for testing purposes
        txt_tru = open(TXT_DIR_TRU + img_name + ".txt", "r", encoding='UTF-8')
        content_tru = txt_tru.read()
        txt_tru.close()
        tru_processed = content_tru.replace("(", ",")
        tru_processed = tru_processed.replace(")", ",")
        tru_processed = tru_processed.replace(":", ",")
        tru_processed = tru_processed.replace("-", ",")
        tru_processed = tru_processed.replace(";", ",")
        tru_processed = tru_processed.replace(".", ",")
        tru_processed = tru_processed.replace("\n", "")
        
        list_tru = tru_processed.split(',') #make a list of all ingredients
        list_tru = [s.strip() for s in list_tru if s != '' and s!= ' '] #remove extra spaces
        #print(list_tru)

        #prepare the OCR result from original image for post-processing
        txt_raw = open(TXT_DIR_RAW + img_name + ".txt", "r", encoding='UTF-8')
        content_raw = txt_raw.read()
        txt_raw.close()
        content_raw = str.lower(content_raw)
        raw_processed = content_raw
        #i = content_raw.find("sastāvdaļas") #finds index at which the string starts

        #remove all characters before "sastāvdaļas"
        split_raw = content_raw.split("sastāvdaļas", 1)
        if len(split_raw) > 1: 
            raw_processed = split_raw[1]
        #remove first character if it is ":"
        if raw_processed[0] == ':':
            raw_processed = raw_processed[1:]

        split_raw = raw_processed.split("var saturēt", 1)
        if len(split_raw) > 1: 
            raw_processed = split_raw[0]

        raw_processed = raw_processed.replace("(", ",")
        raw_processed = raw_processed.replace(")", ",")
        raw_processed = raw_processed.replace(":", ",")
        raw_processed = raw_processed.replace("-", ",")
        raw_processed = raw_processed.replace(";", ",")
        raw_processed = raw_processed.replace(".", ",")
        raw_processed = raw_processed.replace("\n", "")

        list_raw = raw_processed.split(',') #make a list of all ingredients
        list_raw = [s.strip() for s in list_raw if s != '' and s!= ' '] #remove extra spaces


        #animal based ingredient list included in the product
        list_raw_n = []
        #loop through all ingredients and check if they are animal based
        for ingredient in list_raw:

            if ingredient in list_ingredients:
                list_raw_n.append(ingredient)

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
        print(img_name, str(len(list_tru)), list_tru, str(len(list_raw)), list_raw, str(len(list_raw_n)), list_raw_n, sep = ";", file = txt_combined)


txt_combined.close()