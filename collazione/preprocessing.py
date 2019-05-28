import glob
import os
from pie import utils
from pie.tagger import Tagger, lines_from_file
from jinja2 import Environment, PackageLoader, select_autoescape

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
                new_sent = []
                for t in sent:
                    token_dict =  {"form": t[0], "id": "w_"+str(tokenId), "order_id": str(tokenId)}
                    # and now add the different annotations from lemmatiser
                    for index in enumerate(tasks):
                        token_dict[index[1]] = t[1][index[0]]

                    new_sent.append(token_dict)
                    tokenId += 1

                content[wit].append(new_sent)

    return content


def xmlify(content):
    """
    Turns lemmatisation output into xml documents, for further processing
    :param content: lemmatisation output, such as processed by the lemmatise function
    :return:
    """

    env = Environment(
        loader=PackageLoader('collazione', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('geste.xml')

    documents = {}

    for wit in content:
        tokens = [t for sent in content[wit] for t in sent]
        # if format == "tei-geste": Right now only 1 format
        documents[wit] = template.render(tokens=tokens)

    return documents










