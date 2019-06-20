import lemm_coll.collation as coll
import lemm_coll.lemmatise as lemm
import collatex

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('folder_path', help="unix string")
    parser.add_argument('--collate', action='store_true')
    parser.add_argument('--lemmatise', action='store_true')
    parser.add_argument('lang', action = 'store', choices = ['fro', 'spo']) # choices generate error messages if arg is not correct, can be useful
    parser.add_argument('engine', action = 'store', choices = ['pie', 'freeling']) 
    args = parser.parse_args()


 
    if args.lemmatise:
        # path = "./data/preproc/chevLyon/txt"
        lemm.chooseLemmatiser(args.folder_path, args.lang, args.engine)

        
    if args.collate:
        # then we need to load an xml annotated folder
        #path = "./data/input/chevLyon/xml"
        json_input = coll.load_annotated_folder(args.folder_path)

        table = collatex.collate(json_input, output="table", layout="vertical", segmentation=False, near_match=True)
        xml_output = coll.table_to_xml(table)

        with open(args.folder_path + "out.xml", 'w') as f:
            print(xml_output, file=f)

        with open(args.folder_path + "out.txt", 'w') as f:
            print(table, file=f)
