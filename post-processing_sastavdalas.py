

TXT_DIR_RAW = 'texts_raw/' # directory storing OCR result from the original images
TXT_DIR_BW = 'texts_processed/B&W/' # directory storing OCR result from the pre-processed images
TXT_DIR_ING = 'texts_processed/ingredients/' # directory storing post-processed text -> removed before "sastāvdaļas"
TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/' #directory storing all of the results

#do post-processing for images from 1 to 20
for x in range(1, 21):
    img_name = "n" + str(x)

    #prepare the OCR result from original image for post-processing
    txt_raw = open(TXT_DIR_RAW + img_name + ".txt", "r", encoding='UTF-8')
    content_raw = txt_raw.read()
    txt_raw.close()
    content_raw = str.lower(content_raw)
    #print(content_raw)
    #print("\nPēcapstrāde:")
    #i = content_raw.find("sastāvdaļas") #finds index at which the string starts

    #remove all characters before "sastāvdaļas"
    split_raw = content_raw.split("sastāvdaļas", 1)
    #print(split_raw)
    if len(split_raw) > 1: 
        raw_processed = split_raw[1]

    #remove first character if it is ":"
    if raw_processed[0] == ':':
        raw_processed = raw_processed[1:]

    #remove first character if it is " "
    if raw_processed[0] == ' ':
        raw_processed = raw_processed[1:]

    txt_raw_new = open(TXT_DIR_ING + img_name + ".txt", 'w', encoding='UTF-8')
    print(raw_processed, file = txt_raw_new)
    txt_raw_new.close()

    #print(raw_processed)