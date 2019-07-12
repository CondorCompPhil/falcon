#coding utf-8

import json
import itertools
from xml.etree import ElementTree as ET




def table_automaticDictionary(graph, dirName):

    #====================================================
    #
    #  BUILD HTML TABLE
    #
    #====================================================

    dataIn = json.loads(graph)

    ## HEAD OF THE TABLE

    # there is an x inside the script pointing to jquery because if it's empty it will 
    # automatically be written as a closed empty tag in the output and would not work
    html = """<html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"></meta>
        <title>Test collation with normalized tokens</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js">x</script>
        <script type="text/javascript">  
                $(document).ready(function(){
                    $("tr[type='orig']").click(function(){
                        $(this).next().toggle();
                    });
                });
        </script>
        <style>
             tr[type="normAll"] {display: none;}
             tr[type="norm"] {display: none;}
             td, th {padding: 20px;border: 1px solid grey; width:100px}
             table {border-collapse: collapse;}
             .variant {background-color:yellow}
             .invariant {background-color:lightgray}
             .formal_variant {background-color:darkgray}
        </style>
        </head>"""

    html += """<body>
                    <div style="font-size:1.1em; margin: 50px">
                        <p>This table has been automatically generated.
                            <br/>The code and the documentation are available <a href="https://github.com/elespdn/collation_spelling" target="_blank">here</a>.
                            <br/>In order to see the token used for the alignment, just click on a cell.
                        </p>
                        <p>Legend:
                            <ul>
                                <li>
                                    <span class="variant">Substantive variant</span>
                                </li>
                                <li>
                                    <span class="formal_variant">Formal variant</span>
                                </li>
                                <li>
                                    <span class="invariant">Invariant</span>
                                </li>
                            </ul>
                        </p>
                    </div><table border="1"><thead><tr>"""  
    for x in dataIn['table']:
	    if x[0] is not None:
		    witName = x[0][0]['_sigil']    # define the witness name
		    html += "<th>"+witName+"</th>"    # write the witness name in the head of the table
    html += "</tr></thead><tbody>"  ## close thead


    for i in range(len(x)):  # for 'i' in the length of the witness  
        istr = str(i)   # from int to string, otherwise the following does not work

        ## CREATE ROW FOR ORIGINAL TOKEN (@type='orig') - 
        ## EACH <td> HAS THE ORIGINAL TOKEN AS CONTENT AND THE NORMALIZED FORM IN @ana
        html += "<tr type='orig' id='row"+istr+"_orig'>"  
        for x in dataIn['table']:   # for each witness
            element = x[i]   # take the first (then at the next iteration take the second, etc.)
            if element is not None: 
                for elementList in element:
                    origToken = elementList['t'].strip()  # strip used for deleting whitespaces
                    normToken = elementList['n'].strip()
            else:
                origToken = ' - '
                normToken = '_'
            html += '<td ana="'+normToken+'">' + origToken+'</td>'  # write the original token in a cell
            ## close tbody
        html += '</tr>'



        ## CREATE ROW FOR NORMALIZED TOKEN - DISPLAY   @type='norm'
        html += "<tr type='norm' id='row"+istr+"_norm'>"  
        for x in dataIn['table']:   # for each witness
            element = x[i]   # take the first (then at the next iteration take the second, etc.)
            if element is not None: 
                for elementList in element:
                    normToken = elementList['n'].strip()
            else:
                normToken = '_'
            html += "<td>"+normToken+"</td>"  # write the original token in a cell
        html += "</tr>"

    ## CLOSE BODY - END OF THE TABLE    
    html += "</tbody></table></body></html>"
 

    #====================================================
    #
    #  ANALYSE AND RENDER HTML TABLE
    #
    #====================================================

    ## One classes for each row should be added: variant, invariant, formal_variant

    createdTable = html
    root = ET.fromstring(createdTable)
    for tr in root.iter('tr'):  ## iterate over rows
        if ((tr.get('type'))== "orig") and (tr is not None):
            
            listTdText = []   ## open empty lists
            listTdPos = []
            listTdLemma = []

            
            for td in tr.iter('td'):  ## iterate over cells in a row
                
                tdText = td.text
                listTdText.append(tdText)  ## and put their texts in a list (listTdText)
                
                #je ne comprends pas ici : fait buguer le script ! Fonctionne sans LI (06/06/2019) // fonctionne lorsque script normal, pas dans jupyter !
                tdPos = td.get('ana').split('_')[0]
                #tdPos1 = td.get('ana')
                #print(tdPos1)
                #tdPos = tdPos1.split('_')[1]
                listTdPos.append(tdPos)    ## and put their pos in a list (listTdPos)
                
                tdLemma = td.get('ana').split('_')[1]
                #tdLemma1 = td.get('ana')
                #tdLemma = tdLemma1.split('_')[0]
                listTdLemma.append(tdLemma)   ## and put their lemmas in a list (listTdLemma)

            numberOfWits = len(listTdText) 
            ## number of witnesses, we need it later
            listTdLemmaAlternatives = []  
            ## create list of all alternatives lemma (can be more than the number of the
            ## witnesses if there is ambiguity for some lemmas)
            for item in listTdLemma:
                for subitem in item.split('|'):
                    listTdLemmaAlternatives.append(subitem)
                    
            if listTdText.count(listTdText[0]) == len(listTdText):  ## if the texts (original token) are equal
                tr.set('class', 'invariant')     ## invariant
            else:
                for i in range(len(listTdLemmaAlternatives)):  # for each item in the list of all alternative lemmas
                    if (listTdLemmaAlternatives.count(listTdLemmaAlternatives[i]) == numberOfWits) and (listTdPos.count(listTdPos[0]) == len(listTdPos)): 
                    ## if pos are equal and
                    ## if one lemma occurs a number of time equal to the number of the witnesses
                        tr.set('class', 'formal_variant')
                        break
                    else:
                        tr.set('class', 'variant')
            
            
    tree = ET.tostring(root, encoding="unicode")
    outFile = open('results/'+ dirName + '_table_automaticDictionary.html', 'w')
    outFile.write(tree)
"""
import treetaggerwrapper, os, csv, re


def tag_poslemma(dirName):     
    
    # TAGGED-ALL
    writer=csv.writer(open('dictionaries/taggedAll_' + dirName + '.csv', 'w'))
    
    # OPEN FILES IN DIRECTORY
    for witness in os.listdir('data/' + dirName):
        if witness.endswith(".txt"):
            with open('data/' + dirName + '/' + witness) as wit:
                witText = wit.read()

                # TAG USING FRO
                taggerFro = treetaggerwrapper.TreeTagger(TAGLANG='froBfm')
                tagsFro = taggerFro.tag_text(witText)  # LIST WITH TAGGED WORDS (FRO)

                # TAG USING STEIN
                taggerStein = treetaggerwrapper.TreeTagger(TAGLANG='stein')
                tagsSteinDirt = taggerStein.tag_text(witText) # dirst, because has too much info and symbols
                tagsSteinStr = '\n'.join(tagsSteinDirt)  # list to string  
                # CLEAN OUTPUT STEIN
                patterns = [('_.*', ''),
                            ('\d.*', ''),
                          # ('\|.*', ''), so that the different output possibilities are saved
                            ('�', 'ö'),  # encoding problem, but it does not seem to depend on the TreeTaggerWrapper, nor on the script. Maybe on the lexicon? Anyway, this is not real solution but works
                            ('<nolem>', 'UNKNOWN')]
                for (p1,p2) in patterns:
                    p = re.compile(p1)
                    tagsSteinStr = p.sub(p2, tagsSteinStr)
                tagsStein = tagsSteinStr.split('\n')  # LIST WITH TAGGED WORDS (STEIN)
                
                for itemFro, itemStein in zip(tagsFro, tagsStein):
                    token = itemFro.split('\t')[0]
                    pos = itemFro.split('\t')[1]
                    lemma = itemStein.split('\t')[2]
                    item = token + '\t' + pos + '_' + lemma
                    writer.writerow([item]) # populate the file with items (made by token, pos and lemma)
                    

    # TAGGED-DISTINCT
    reader=csv.reader(open('dictionaries/taggedAll_' + dirName + '.csv', 'r'), delimiter='\t')
    writer=csv.writer(open('dictionaries/taggedDistinct_' + dirName + '.csv', 'w'), delimiter=',')
    entries = set()
    writer.writerow(['Original', 'Normalised'])
    for row in reader:
        key = (row[0], row[1]) 
        if key not in entries:
            writer.writerow(row)
            entries.add(key)
"""