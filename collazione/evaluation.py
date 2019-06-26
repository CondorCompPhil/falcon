from lxml import etree
import difflib

def listEvaluation(gt, out):
    '''
    CHECK ALIGNMENT
    Compare XML files by transforming them to lists of //rdg content
    and apply edit distance to the lists
    Lemmatization cannot be checked with this approach
    :param gt: path to ground truth (the expected result)
    :param out: path to tree to evaluate
    :return: a measure of the lists similarity as a float in the range [0, 1].
    '''
    # read XML with automatically generated results
    treeA = etree.parse(gt)
    rootA = treeA.getroot()

    # read XML with manual ideal results
    treeB = etree.parse(out)
    rootB = treeB.getroot()

    # transform both into lists
    listA = rootA.xpath(".//rdg/text()")
    listB = rootB.xpath(".//rdg/text()")

    '''
    compare the lists
    ratio()
    returns a measure of the lists similarity as a float in the range [0, 1].
    '''
    sm = difflib.SequenceMatcher(None, listA, listB)
    print("Similarity: {}".format(sm.ratio()))

