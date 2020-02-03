import sys
from falcon import *
import falcon.lemmatise_pie as lemmatise_pie

if __name__ == "__main__":
    content = {}
    for file in sys.argv[1:]:
        wit = file
        content[wit] = []
        tokenId = 1
        #tasks = ('lemma', 'pos', 'morph')
        with open(file, 'r') as f:
            # pop first line (header)
            tasks = f.readline().rstrip().split('\t')
            sent = []
            for line in f.readlines():
                t = line.rstrip().split('\t')
                if not t == ['']:
                    token_dict =  {"form": t[0], "id": "w_"+str(tokenId), "order_id": str(tokenId)}
                    # and now add the different annotations from lemmatiser
                    for index in enumerate(tasks):
                        token_dict[index[1]] = t[index[0]]
                    
                    sent.append(token_dict)
                    tokenId += 1

                else:
                    content[wit].append(sent)
                    sent = []

    documents = lemmatise_pie.xmlify(content)
    for doc in documents:
        with open(doc + ".xml", 'w') as f:
            f.write(documents[doc])

