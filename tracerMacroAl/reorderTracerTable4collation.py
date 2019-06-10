
import csv

# from Tracer output create table with only identifiers and texts
with open("roudTracer.csv", 'r') as in_file, open("roudTracer_onlyRelevantData.csv", 'w') as out_file:
	outdata = []
	reader = csv.reader(in_file, delimiter="\t")
	writer = csv.writer(out_file, delimiter="\t")
	'''
	for each row put together the first text (col4) and its index (col0)
	and the second text (col5) and its index (col1). These cols are in Tracer output
	'''
	for row in reader:
		outdata.append([row[0] + ". " + row[4], row[1] + ". " + row[5]])
	writer.writerows(outdata)


####################################
#
# NEED TO SORT FIRST??
#
####################################

# reorder table
with open("roudTracer_onlyRelevantData.csv", 'r') as in_file, open("roudTracer_onlyRelevantData_reordered.csv", 'w') as out_file:
	reader = csv.reader(in_file, delimiter="\t")
	writer = csv.writer(out_file, delimiter="\t")
	
	# create an empty list
	reorderedList = []
	for idx, row in enumerate(reader):
		'''
		each row is like this: ['text1', 'text2']
		function adds index (idx) to each row
		A takes value of text1 and B takes value of text2
		'''
		i = idx    
		A = row[0] 
		B = row[1] 
		'''
		A and B are added to the reorderedList only if they aren't there already, using 'not in'
		The index is added only if A and B are both added.
		If only A or only B are added, their row index is not added, so they follow the previous index.
		Indexes will be used below to create the new lines
		'''
		# add new index only if new ('else'), otherwise will be added to previous one
		if (A in reorderedList and B not in reorderedList):
			reorderedList.append(B)
		elif (B in reorderedList and A not in reorderedList):
			reorderedList.append(A)
		elif (A in reorderedList and B in reorderedList):
			continue
		else: # if A and B not in reorderedList
			reorderedList.append(i)
			reorderedList.append(A)
			reorderedList.append(B)

#this is not efficient, creates useless duplicates
	newFile = []
	for x in reorderedList:
		if type(x) == int:
			newLine = []
			newLine.append(x)
		else:
			newLine.append(x)
		newFile.append(newLine)
	
#deduplicate newFile
	seen = set() # 
	for row in newFile:
		row = tuple(row)
		if row in seen: continue 
		seen.add(row)
		writer.writerow(row)






    