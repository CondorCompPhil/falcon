import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.corpus import wordnet as wn

# print(wn.synsets('dog'))

'''
cane_lemmas = wn.lemmas("cane", lang="ita")
print(cane_lemmas)
'''

print(wn.lemmas("fanciullo", lang="ita")[0].synset().lemmas(lang="ita"))