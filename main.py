from ast import arg
import falcon.collation as coll
import falcon.lemmatise as lemm
import falcon.categorise as categ
import falcon.simple as simple
import collatex
import os

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('folder_path', help="folder containing the files to collate") #TODO: change to path of all the files, like folder/*
    parser.add_argument('--simple', action='store_true', help="do a simple collation from txt files without lemmatisation")
    # TODO: do that by default if no lemmatisation and if from txt
    parser.add_argument('--collate', action='store_true', help="collate the files")
    parser.add_argument('--lemmatise', action='store_true', help="lemmatise the files")
    parser.add_argument('--lang', action='store', choices=['fro', 'spo'], default='fro', help="language to use for lemmatisation")  # choices generate
    # error messages if arg is not correct, can be useful
    parser.add_argument('--engine', action='store', choices=['pie', 'freeling'], default='pie', help="lemmatisation engine to use")
    parser.add_argument('--output_dir', action='store', default='out',
                        help="name of the output directory (default 'out')")
    parser.add_argument('--categorise', action='store_true', help="categorise the variants resulted from the collation")
    args = parser.parse_args()

    # create output dir
    os.makedirs(args.output_dir, exist_ok=True)

    if args.simple:
        alignment_table = simple.collateSimple(args.folder_path)
        os.makedirs(args.output_dir+"/coll", exist_ok=True)
        with open(args.output_dir+"/coll"+"/simple.xml", 'w') as outFile:
            outFile.write(alignment_table)

    if args.lemmatise:
        # path = "./data/preproc/chevLyon/txt"
        documents = lemm.choose_lemmatiser(args.folder_path, args.lang, args.engine)
        os.makedirs(args.output_dir + "/lemmat", exist_ok=True)
        for doc in documents:
            with open(args.output_dir + "/lemmat/" + doc + ".xml", 'w') as f:
                f.write(documents[doc])
        
    if args.collate:
        # if we did not just wrote it
        if args.lemmatise is not True:
            # then we need to load an xml annotated folder
            # path = "./data/input/chevLyon/xml"
            json_input = coll.load_annotated_folder(args.folder_path)

        else:
            json_input = coll.load_annotated_folder(args.output_dir+"/lemmat/")

        table = collatex.collate(json_input, output="table", layout="vertical", segmentation=False, near_match=True)
        xml_output = coll.table_to_xml(table)

        os.makedirs(args.output_dir + "/coll", exist_ok=True)

        with open(args.output_dir + "/coll" + "/out.xml", 'w') as f:
            print(xml_output, file=f)

        with open(args.output_dir + "/coll" + "/out.table", 'w') as f:
            print(table, file=f)

    if args.categorise:

        if args.collate is not True:
            # use the specified folder path which should include collation results in XML (<app>, <rdg>)
            xml_to_be_categorised = args.folder_path
        else:
            # use the collation results from previous step
            xml_to_be_categorised = args.output_dir + "/coll/out.xml"

        # assign a category to each <app> containing variant <rdg>s
        categ_xml_output = categ.categorise(xml_to_be_categorised)

        os.makedirs(args.output_dir + "/categ", exist_ok=True)

        with open(args.output_dir + "/categ/out.xml", "w", encoding="utf-8") as f:
            print(categ_xml_output, file=f)

