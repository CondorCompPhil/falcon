
import treetaggerwrapper, os, csv, glob
from collections import defaultdict
from typing import List, Dict


Sentence = List
Token = Dict[str, str]

def lemmatise(dirName, lang) -> Dict[str, List[Sentence[Token]]]:     

    content = defaultdict(list)
    
    # OPEN FILES IN DIRECTORY
    files = glob.glob(dirName + '/*.txt')
    
    for witness in files:
        wit = os.path.splitext(os.path.split(witness)[-1])[0]
        with open(witness, 'r') as witnessText:
            witText = witnessText.read()

            # TAG
            tagger = treetaggerwrapper.TreeTagger(TAGLANG=lang)
            tags = tagger.tag_text(witText)  # LIST WITH TAGGED WORDS
    
            tok_id = 0
            for tag in tags:
                token = tag.split('\t')[0]
                pos = tag.split('\t')[1]
                lemma = tag.split('\t')[2]
                item = {'form': token, 'lemma': lemma, 'POS': pos }
                tok_id = tok_id + 1
                ##### TO DO: add order_id

                if not content[wit]:
                    content[wit].append([])
                if token is None:
                    content[wit].append([])
                else:
                    content[wit][-1].append({
                        **item,
                        "id": f"w_{tok_id}",
                    })

    return content