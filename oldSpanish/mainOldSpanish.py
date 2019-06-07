import lemm_coll.freeling_oldSpanish as freel
import lemm_coll.core as coll
import collatex

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('folder_path', help="unix string")
    parser.add_argument('--collate', action='store_true')
    parser.add_argument('--lemmatise', action='store_true')
    args = parser.parse_args()

    if args.lemmatise:
        # path = "./data/lucanor"
        freel.freeling_oldSp(args.folder_path)
        
    
    if args.collate:
        #path = "./data/lucanor"
        json_input = coll.load_annotated_folder(args.folder_path)

        table = collatex.collate(json_input, output="table", layout="vertical", segmentation=False, near_match=True)
        xml_output = coll.table_to_xml(table)

        with open(args.folder_path+"/out.xml", 'w') as f:
            print(xml_output, file=f)

        with open(args.folder_path+"/out.txt", 'w') as f:
            print(table, file=f)
