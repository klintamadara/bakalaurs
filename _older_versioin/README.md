# bakalaurs
private

Mērķis: noteikt OCR precizitāti produktu sastāvdaļu nolasīšanā. 
Possible metrics:
1. Levenshtein -> checks OCR accuracy
    - should I compare between images units or characters within images?
2. Ingredients -> checks solution accuracy. Ultimately - F1 score/ accuracy formula?
    2.1. Whether product has been correctly flagged as vegan/non-vegan (ultimate goal)
    2.2. Nr of animal ingredients identified correctly.
    2.3. Nr of all ingredients identified correctly. In general, solution will identify animal based ingredients, but will not check the plant based. But for testing purposes all ingredients can be checked based on solution's definition of "ingredient" (splitting in delimiters). That's how OCR accuracy is checked.


What has been done:
1. OCR reads raw image/ B&W image
    - B&W image provides worse OCR result ;/
2. Removes everything before "sastāvdaļas" (and after "var saturēt", which can be in the middle), calculates Levenshtein.
3. Splits text into ingredients, splitting in , . ; [ ] : ( ) \n. What about - (removed from list), * (atzīmē izcelsmi, piem, bio. Arī (s)* - par eļļām (n19))
4. Compares with animal ingredient list and stores the result (all lists, their ingredients)

Others done:
- Remove % (regex?), preferable before creating list. Account for comma 1,5%; spaces (4 %; 1. 5%; 1,5 % etc.)


To do:
1. var saturētolu --> exception handling. levenshtein? built-in manual check? How to know where "var saturēt" ends? Hm, "var saturēt" mentions only allergens, i.e. olu, soju, pienu, riekstus u.tml. - maybe can use that? (although there's still much variation with words and their possible sequence).
Could ignore spaces, but at the same time it makes it harder to catch unwanted false positives (pienskābe, kukurūzu krakmolas, tūrgi hemeste pāritolu)
2. Update actual ingredients list
3. Count and define animal based ingredients in each non-vegan product
4. Similarity check based on % not identical check? What about complexity... Should I do both and compare? E330=6330 -> can I make an assumption that >6000 means E...? Alt levenshtein check 1 (but will correct only for non-vegan products)
5. Implement/ try out other preprocessing techniques
6. Somehow (how?) compare lists - correct and identified. Based on counts? On key words?
7. (Optionally) compare different psms in the end
8. Exeption handling -> Kokosriekstu piens, kakao/riekstu sviests, pienskābe, (dabiski) nav ... bez ..  When to do it? while raw text, identical search would be easier/faster. Could also check ones an "animal ingredient" found, whether next to it there aren't these exception keywords
9. Add on animal based ingredient list


Questions/issues:
- Delimiters: which ones? Do I use - or not? What about :. They will delimit the same ingredient sometimes
- Vai jābūt identiskiem, lai ieskaitītu? Piem, sastāvdaļa "saldais krējums" nolasīšanas dēļ kļūst par sastāvdaļu "krējums" - keyword "krējums" tiek atpazīts... vai arī vājpiena pulveris kļūst par vājpiena. olu pulveris -> olu pamira etiķis. Domāju, ka jāieskaita, jo svarīgi tieši atpazīt atslēgvārdus. Bet nav gluži identiska sastāvdaļa... Another metric?
- Should I do inferential statistical methods? Which ones
- Perfectly, I would create my algorithm based on 100 examples, and test it with another 100 examples...
- What should be the metrics? Absolute, relative (% of chars unrecognized?.. Levenshtein)
- Levenshtein... Is it a right metric? psm13 had the best results but most were empty results (adding the necessary 300 characters apparently gives better Levenshtein result than deleting extra 400 characters/ changing the wrong ones)
- "Izlietot līdz"/"Uzturvērtība" u.tml - can be anywhere within text. Also "var saturēt" can be in the middle. Ignore it?
- kakavos sviestas -> LT. sviesta flags this ingredient.
- Is it ok to use Levenshtein library?



Segmentation modes:
psm3 -> raw     some results blank
psm13 -> raw    results mostly blank
psm6 -> raw+B&W+GS+post-processing.

psm6:
B&W -> vs tru, Levenshtein
GS -> need to test (prepared texts + images)
BGremove -> need to test
noise -> made a bit blurry image...
thresholding -> code doesn't work