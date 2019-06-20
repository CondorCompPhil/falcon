#!usr/bin/env python
# -*- coding: utf-8 -*-

from . import lemmatise_pie
from . import lemmatise_freeling_spo

def chooseLemmatiser(path, lang, engine):

    if lang == "fro" and engine == "pie":
        content = lemmatise_pie.lemmatise(path, "<models/fro_lemma-pos.tar,lemma><models/fro_lemma-pos.tar,pos><models/fro_morph.tar,morph>")
        documents = lemmatise_pie.xmlify(content)
        for doc in documents:
            with open(path + '/' + doc + ".xml", 'w') as f:
                f.write(documents[doc])


    if lang == "spo" and engine == "freeling":
        lemmatise_freeling_spo.freeling_spo(path)

    '''
    if lang == "sp" and engine == "pie":
        content = lemmatise_pie.lemmatise(path, "PATH TO OTHER MODELS")
        documents = lemmatise_pie.xmlify(content)
        for doc in documents:
            with open(path + '/' + doc + ".xml", 'w') as f:
                f.write(documents[doc])

    '''