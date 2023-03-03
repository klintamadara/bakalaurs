# bakalaurs
private

post-processing_no:
no post prociessing

post-processing_all:
exact match

post-processing_all_1:
Levenshtein 1

post-processing_all_2:
Levenshtein <= 25% no vārda

What:
- saturēt, nesatur
- AB ingredients
- koko sviests utt.
- sastāvdaļas?

Mērķis: noteikt OCR precizitāti produktu sastāvdaļu nolasīšanā. 


What has been done:
1. OCR reads raw image/ B&W image
    - B&W image provides worse OCR result ;/
2. Removes everything before "sastāvdaļas" (and after "var saturēt", which can be in the middle), calculates Levenshtein.
3. Splits text into ingredients, splitting in , . ; [ ] : ( ) \n. What about - (removed from list), * (atzīmē izcelsmi, piem, bio. Arī (s)* - par eļļām (n19))
4. Compares with animal ingredient list and stores the result (all lists, their ingredients)

Others done:
- Remove % (regex?), preferable before creating list. Account for comma 1,5%; spaces (4 %; 1. 5%; 1,5 % etc.)



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