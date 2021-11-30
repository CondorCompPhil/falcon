from collatex import *
import glob, os

def collateSimple(path):
	collation = Collation()

	'''
	for each txt in the folder:
		take name of the file
		take content of the file
		add it to collation
	'''

	sources = glob.glob(path+'/*.txt')

	for wit in sources:
		witName = os.path.basename(wit).split(".")[0]
		witContent = open(wit, encoding="utf-8").read()
		collation.add_plain_witness(witName, witContent)
	alignment_table = collate(collation, output="tei", segmentation=False, near_match=True)
	with open( path.split("sources")[0]+ "/simple.xml", 'w') as outFile:
		outFile.write(alignment_table)

