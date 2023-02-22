# bakalaurs
private

Mērķis: noteikt OCR precizitāti produktu sastāvdaļu nolasīšanā. 2 metrics:
1. Levenshtein -> checks OCR accuracy
    - should I compare between images units or characters within images?
2. Ingredients -> checks solution accuracy. Ultimately - F1 score/ accuracy formula?
Can it be approximate? Solution will identify animal based ingredients, but will not check the plant based (compare count out of total)?

What has been done:
1. OCR reads raw image/ B&W image
    - B&W image provides worse OCR result ;/
2. Removes everything before "sastāvdaļas" (and after "var saturēt", which can be in the middle), calculates Levenshtein.
3. Splits text into ingredients, splitting in , . ; - : ( ) \n
4. Compares with animal ingredient list and stores the result (all lists, their ingredients)



To do:
1. Remove % (regex?), preferable before creating list. Account for comma 1,5%; spaces (4 %; 1. 5%; 1,5 % etc.)
2. Update actual ingredients list
3. Count and define animal based ingredients in each non-vegan product
4. Similarity check based on % not identical check? What about complexity... Should I do both and compare? E330=6330
5. Implement/ try out other preprocessing techniques
6. Somehow (how?) compare lists - correct and identified. Based on counts? On key words?
7. (Optionally) compare different psms in the end
8. Exeption handling -> Kokosriekstu piens, kakao/riekstu sviests, bez ..  (when to do it?)
9. Add on animal based ingredient list


Questions/issues:
- Delimiters: which ones? Do I use - or not? What about :. They will delimit the same ingredient sometimes
- Should I do inferential statistical methods? Which ones
- Perfectly, I would create my algorithm based on 100 examples, and test it with another 100 examples...
- What should be the metrics? Absolute, relative (% of chars unrecognized?.. Levenshtein)
- Levenshtein... Is it a right metric? psm13 had the best results but most were empty results (adding the necessary 300 characters apparently gives better Levenshtein result than deleting extra 400 characters/ changing the wrong ones)
- "Izlietot līdz"/"Uzturvērtība" u.tml - can be anywhere within text. Also "var saturēt" can be in the middle. Ignore it?




psm3    psm6            psm13
raw     raw+B&W+post    raw

psm6:
B&W -> vs tru
GS -> prepared texts + images