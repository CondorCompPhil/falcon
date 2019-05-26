import collazione.core as coll
import sys
import collatex


if __name__ == "__main__":

    #path = "./data/input/chevLyon/xml"
    path = sys.argv[1]

    json_input = coll.load_folder(path)

    table = collatex.collate(json_input, output="table", layout="vertical", segmentation=False, near_match=True)

    xml_output = coll.table_to_xml(table)

    with open("out.xml", 'w') as f:
        print(xml_output, file=f)

    with open("out.txt", 'w') as f:
        print(table, file=f)

