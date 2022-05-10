import glob
import os
from typing import List, Dict
from collections import defaultdict
from jinja2 import Environment, PackageLoader, select_autoescape
from pie.utils import shutup
with shutup():
    from pie_extended.cli.utils import download, get_tagger, get_model, get_imports
    from pie_extended.utils import get_path

def check(module: str, force: bool = False) -> bool:
    """
    Check if a language model is installed, and install it if needed
    :param module: the language
    :param force:
    :return:
    """
    lemmatizer = get_model(module)
    return False not in [
        os.path.exists(
            get_path(module, file.name)
        )
        for file in lemmatizer.DOWNLOADS
    ] or force


Sentence = List
Token = Dict[str, str]

def lemmatise(path, model_spec) -> Dict[str, List[Sentence[Token]]]:

    """
        lemmatises raw text input, with the given model(s), using Pie(-extended).
        :param path: path to folder containing the texts
        :param model_spec: specification of the model, one of pie-extended's
        :return: a dictionary, with a list for each witness, containing a list for each sentence.
    """

    # handle install
    # lets check if we need to install or not
    if check(model_spec) is not True:
        for model in download(model_spec):
            download(model_spec)

    # get tagger
    with shutup():
        tagger = get_tagger(model_spec, batch_size=256, device="cpu", model_path=None)

    # import iterator and processor
    iterator, processor = getattr(get_imports(get_model(model_spec)), "get_iterator_and_processor")(max_tokens=256)

    # Get files content
    files = glob.glob(path + '/*.txt')
    content = defaultdict(list)
    for f in files:
        wit = os.path.splitext(os.path.split(f)[-1])[0]
        tok_id_diff = 0
        with open(f, 'r') as doc:
            for tok_id, token in enumerate(tagger.iter_tag_token(
                    data=doc.read(),
                    iterator=iterator,
                    processor=processor,
                    empty_token_on_sent_break=True
            )):
                if not content[wit]:
                    content[wit].append([])
                # token_dict = {"form": t[0], "id": "w_" + str(tokenId), "order_id": str(tokenId)}
                if token is None:
                    tok_id_diff -= 1
                    content[wit].append([])
                else:
                    content[wit][-1].append({
                        **token,
                        "id": f"w_{tok_id + tok_id_diff}",
                        "order_id": str(tok_id + tok_id_diff)
                    })

    return content


def xmlify(content):
    """
    Turns lemmatisation output into xml documents, for further processing
    :param content: lemmatisation output, such as processed by the lemmatise function
    :return:
    """

    env = Environment(
        loader=PackageLoader('falcon', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    #template = env.get_template('geste.xml')
    template = env.get_template('geste_with_sents.xml')

    documents = {}

    for wit in content:
        #tokens = [t for sent in content[wit] for t in sent]
        #sentences = [sent for sent in content[wit]]
        sentences = content[wit] #TODO: fix the getting of sentences
        # if format == "tei-geste": Right now only 1 format
        #documents[wit] = template.render(tokens=tokens)
        documents[wit] = template.render(sentences=sentences)

    return documents










