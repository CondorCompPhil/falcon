import glob
import os
from pie import utils
from pie.tagger import Tagger, lines_from_file
from flask import render_template


def lemmatise(path, model_spec):
    """
    lemmatises raw text input, with the given model(s), using Pie.
    :param path: path to folder containing the texts
    :param model_spec: specification of the model(s), in Pie syntax
    :return: a dictionary, with a list for each witness, containing a list for each sentence.
    """
    tagger = Tagger()

    for model, tasks in utils.model_spec(model_spec):
        tagger.add_model(model, *tasks)
        print(" - model: {}".format(model))
        tasks = tasks or tagger.models[-1][0].label_encoder.tasks
        print(" - tasks: {}".format(", ".join(tasks)))

    # Get files content
    files = glob.glob(path + '/*.txt')
    content = {}
    for f in files:
        wit = os.path.splitext(os.path.split(f)[-1])[0]
        content[wit] = []
        tokenId = 1

        for chunk in utils.chunks(lines_from_file(f), 200):
            sents, lengths = zip(*chunk)
            tagged, tasks = tagger.tag(sents, lengths)
            for sent in tagged:
                # cannot use comprehension because need to define id ?
                # content[wit].append([{"form": t[0], "lemma": t[1][0], "POS": t[1][1], "morph": ''} for t in sent])
                new_sent = []
                for t in sent:
                    new_sent.append({"form": t[0], "lemma": t[1][0], "POS": t[1][1],
                                     "morph": '', "id": "w_"+str(tokenId), "order_id": str(tokenId)})
                    tokenId += 1

                content[wit].append(new_sent)

    return content


def xmlify(content):
    """
    Turns lemmatisation output into xml documents, for further processing
    :param content: lemmatisation output, such as processed by the lemmatise function
    :return:
    """

    for wit in content:
        tokens = [t for sent in content[wit] for t in sent]
        # if format == "tei-geste": Right now only 1 format
        response = render_template("templates/geste.xml", tokens=tokens)










