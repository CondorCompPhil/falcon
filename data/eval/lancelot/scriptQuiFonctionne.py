#!usr/bin/env python
# -*- coding: utf-8 -*-

from collatex import *
collation = Collation()
import csv, re, os
from fonction_Elena import *

try:
    os.mkdir("results")
except OSError:
    pass


# les fonctions originales ne marchaient pas : on utilise bêtement des listes

"""
tag_poslemma('data/Lanc')  # ex: create_poslemma('example1')
print("taggedAll and taggedDistinct created in folder Dictionaries/ !")
"""

liste = []

with open("data/Ao.csv") as csvfile:
    #par rapport au code d'origine : rajout du delimiteur car sinon ne fonctionne pas (soit \t soit ;)
    reader = csv.reader(csvfile, delimiter=";")
    print(type(reader))
    for row in reader:
        dico={}
        o = row[0]
        print(o)
        n = row[1]
        dico["t"]=o
        dico["n"]=n
        liste.append(dico)

print(liste)
liste2 = []

with open("data/Ez.csv") as csvfile:
    #par rapport au code d'origine : rajout du delimiteur car sinon ne fonctionne pas (soit \t soit ;)
    reader = csv.reader(csvfile, delimiter=";")
    print(type(reader))
    for row in reader:
        dico={}
        o = row[0]
        print(o)
        n = row[1]
        dico["t"]=o
        dico["n"]=n
        liste2.append(dico)

print(liste2)


witness_A = { "id": "A", "tokens":liste }
witness_B = { "id": "B", "tokens":liste2 }

input = { "witnesses": [ witness_A, witness_B] }

print(input)

table = collate(input, output='html2', segmentation=False)
print(table)
graphSvg = collate(input, output='svg', segmentation=False)
print(graphSvg)

graph_automaticDictionary = collate(input, output='json', segmentation=False)
table_automaticDictionary(graph_automaticDictionary, 'data')
print('external table created!')