from lxml import etree

def categorise(xml_collation_result):

    with open(xml_collation_result, "r", encoding="utf-8") as inFile:
        root = etree.parse(inFile)
        
    #for each <app>
    for element in root.iter("app"):

        # create a list of <rdg>s content
        rdgs = [rdg.text for rdg in element.iter("rdg")] 
        
        # if <rdg>s have different contents, there is a variation
        # to check if they are equal, transform the list to set, which removes duplicates
        if (len(rdgs)> 1) and (len(set(rdgs)) != 1):
        
            # create lists of @lemmas, @pos and @msd
            lemmas = [rdg.get("lemma") for rdg in element.iter("rdg")]
            poss = [rdg.get("pos") for rdg in element.iter("rdg")]
            msds = [rdg.get("msd") for rdg in element.iter("rdg")]
        
            # if <rdg>s have same @lemma, @pos and @msd > diffGraph
            if (len(set(lemmas)) == 1) and (len(set(poss)) == 1) and (len(set(msds)) == 1):
                variationCategory = "diffGraph"
            # if <rdg>s have same @lemma, @pos, but different @msd > diffMorph
            elif (len(set(lemmas)) == 1) and (len(set(poss)) == 1):
                variationCategory = "diffMorph"
            # if <rdg>s have same @lemma, but different @pos and @msd > diffPos
            elif (len(set(lemmas)) == 1):
                variationCategory = "diffPos"
            else:
                variationCategory = "diffLemma"

            # add @ana to <app> to categorize the variation
            element.set("ana", variationCategory)

    categorisedOutput = str(etree.tostring(root, pretty_print=True, encoding="unicode"))

    return categorisedOutput


