#!usr/bin/env python
# -*- coding: utf-8 -*-


def choose_lemmatiser(path, lang, engine):

    if engine == "pie":
        from . import lemmatise_pie
        # Start pie lemmatisation

        content = lemmatise_pie.lemmatise(path, lang)
        documents = lemmatise_pie.xmlify(content)

    if engine == "treetagger":
        from . import lemmatise_treetagger
        content = lemmatise_treetagger.lemmatise(path, lang)
        
        from . import lemmatise_pie
        documents = lemmatise_pie.xmlify(content)
        
    return documents
