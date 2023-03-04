#import pandas as pd

TXT_DIR_RSLTS = 'results/' #directory storing all of the results

#code compares results from OCR to the correct ingredients list and returns Levenshtein and Jaccard similarity, as well as overlap coefficient
#for each test case, saves it in the result txt file
results = 'PSMs'

#erase if there was content in the text files before and write title
#result_file = open(TXT_DIR_RSLTS + results + ".txt", "r")
#results = result_file.read()

data = "0.67	0.42	0.00	0.00	0.68	0.55	0.84	0.59	0.02	0.00	0.00	0.35	0.63	0.78	0.62	0.33	0.29	0.45	0.58	0.12	0.00	0.76	0.00	0.00	0.07	0.64	0.64	0.00	0.40	0.31	0.47	0.00	0.75	0.34	0.00	0.00	0.71	0.86	0.94	0.00	0.00	0.68	0.00	0.77	0.83	0.89	0.88	0.77	0.56	0.48	0.80	0.96	0.77	0.76	0.74	0.79	0.80	0.02	0.00	0.93	0.75	0.25	0.44	0.31	0.76	0.00	0.50	0.68	0.19	0.08	0.00	0.75	0.75	0.07	0.82	0.94	0.62	0.66	0.37	0.70	0.77	0.70	0.73	0.72	0.86	0.47	0.55	0.02	0.74	0.00	0.65	0.83	0.37	0.85	0.76	0.00	0.94	0.00	0.68	0.76	0.90	0.63	0.44	0.00	1.00	0.63	0.73	0.75	0.91	0.91	0.67	0.00	0.71	0.00	0.72	0.63	0.70	0.00	0.73	0.09	0.00	0.67	0.64	0.00	0.06	0.69	0.73	0.79	0.79	0.73	0.90	0.19	0.64	0.91	0.85	0.88	0.76	0.00	0.50	0.67	0.67	0.81	0.81	0.83	1.00	0.00	0.69	0.70	0.53	0.70	0.35	0.83	0.38	0.63	0.06	0.00	0.83	0.53	0.70	0.80	0.05	0.49	0.00	0.20	0.18	0.00	0.00	0.50	0.00	0.33	0.00	0.80	0.89	0.92	0.57	0.33	0.00	0.40	0.00	0.67	0.69	0.75	0.00	0.00	0.80	0.00	0.90	0.00	0.50	0.00	0.60	0.08	0.82	0.00	0.69	0.11	0.69	0.83	0.00	0.77"
list = data.split()
print(list)

my_data = pd.Series(data)
my_data.hist()