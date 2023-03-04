import string

def Jaccard_similarity(x,y):
    z=set(x).intersection(set(y))
    a=float(len(z))/(len(x)+len(y)-len(z))
    return a


def overlap_coefficient(x,y):
    z=set(x).intersection(set(y))
    a=float(len(z))/min(len(x),len(y))
    return a


a = ["olas", "cukurs", "piena", "maize", "ūdens"]
b = ["ūdens", "ols"]

#print(Jaccard_similarity(a,b))
#print(overlap_coefficient(a,b))

ingredient = "hello, ūdens    , cukurs)   , ol    '  ' as*, 'augi, piens (no laktozes})"

separate_words = [word.strip(string.punctuation) for word in ingredient.split()]
print(separate_words)               
separate_words = [s.strip() for s in separate_words if s != '' and s!= ' '] #remove extra spaces

print(separate_words)               