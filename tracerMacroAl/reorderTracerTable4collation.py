
import csv
import pandas as pd


# from Tracer output create table with only identifiers and texts
with open("roudTracer.csv", 'r') as in_file, open("roudTracer_onlyRelevantData.csv", 'w') as out_file:
	outdata = []
	reader = csv.reader(in_file, delimiter="\t")
	writer = csv.writer(out_file, delimiter="\t")
	for row in reader:
		outdata.append([row[0] + ". " + row[4], row[1] + ". " + row[5]])
	writer.writerows(outdata)

# create list of all cells
with open("roudTracer_onlyRelevantData.csv", 'r') as in_file:
	reader = csv.reader(in_file, delimiter="\t")
	listAllCells = []
	for idx, row in enumerate(reader):
	    rowDict={}
	    i = idx
	    A = row[0]
	    B = row[1]
	    rowDict["i"]=i
	    rowDict["a"]=A
	    rowDict["b"]=B
	    listAllCells.append(rowDict)


# reorder table
with open("roudTracer_onlyRelevantData.csv", 'r') as in_file, open("roudTracer_onlyRelevantData_FINAL.csv", 'w') as out_file:
	reader = csv.reader(in_file, delimiter="\t")
	writer = csv.writer(out_file, delimiter="\t")
	newFile = []
	for idx, row in enumerate(reader):
		A = row[0]
		B = row[1]
		# how many times A occurs. Literally, how long is the list of occurrences
		Aocc = [element for element in listAllCells if (element['a'] == A or element['b'] == A)]
		Bocc = [element for element in listAllCells if (element['a'] == B or element['b'] == B)]
		if (len(Aocc) < 2 and len(Bocc) < 2):
			newFile.append(row)
		else:
			ArepItems = []
			BrepItems = []
			for x in Aocc:
				ArepItems.append(x['a'])
				BrepItems.append(x['b'])
			newLineAocc = set(ArepItems + BrepItems)
			
			for x in Bocc:
				ArepItems.append(x['a'])
				BrepItems.append(x['b'])
			newLineBocc = set(ArepItems + BrepItems)
			newLine = (newLineAocc & newLineBocc) # merge sets only distinct
			newFile.append(newLine)
			
	#deduplicate newFile
	seen = set() # 
	for row in newFile:
		row = tuple(row)
		if row in seen: continue 
		seen.add(row)
		writer.writerow(row)


# iterate over reorder table





    