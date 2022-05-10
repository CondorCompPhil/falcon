#!usr/bin/env python
# -*- coding: utf-8 -*-


def choose_lemmatiser(path, lang, engine):

    if engine == "pie":
        from . import lemmatise_pie
        # Start pie lemmatisation

        content = lemmatise_pie.lemmatise(path, lang)
        documents = lemmatise_pie.xmlify(content)
        for doc in documents:
            with open(path + '/' + doc + ".xml", 'w') as f:
                f.write(documents[doc])

    if engine == "freeling":
        if lang == "spo":
            from . import lemmatise_freeling_spo
            lemmatise_freeling_spo.freeling_spo(path)
