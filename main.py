import collazione.core as coll
import collazione.preprocessing as prepr
import sys
import collatex
import argparse

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('folder_path', help="unix string")
    parser.add_argument('--collate', action='store_true')
    parser.add_argument('--lemmatise', action='store_true')
    args = parser.parse_args()

    if args.lemmatise:
        # path = "./data/preproc/chevLyon/txt"
        # model_spec = "<models/fro_lemma-pos.tar,lemma><models/fro_lemma-pos.tar,pos>"
        content = prepr.lemmatise(args.folder_path, "<models/fro_lemma-pos.tar,lemma><models/fro_lemma-pos.tar,pos>")


    if args.collate:
        if not args.lemmatise:
            # then we need to load an xml annotated folder
            #path = "./data/input/chevLyon/xml"
            json_input = coll.load_annotated_folder(args.folder_path)

        table = collatex.collate(json_input, output="table", layout="vertical", segmentation=False, near_match=True)
        xml_output = coll.table_to_xml(table)

        with open("out.xml", 'w') as f:
            print(xml_output, file=f)

        with open("out.txt", 'w') as f:
            print(table, file=f)
