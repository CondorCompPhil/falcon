from lxml import etree
import difflib

def listEvaluation(gt, out, print_diff = False):
    '''
    CHECK ALIGNMENT
    Compare XML files by transforming them to lists of //rdg content
    and apply edit distance to the lists
    Lemmatization cannot be checked with this approach
    :param gt: path to ground truth (the expected result)
    :param out: path to tree to evaluate
    :param print_diff: boolean, whether to print comparison string
    :return: a measure of the lists similarity as a float in the range [0, 1].
    '''
    # read XML with automatically generated results
    rootA = etree.parse(gt).getroot()

    # read XML with manual ideal results
    rootB = etree.parse(out).getroot()

    # transform both into lists
    listA = _etree_to_list(rootA)
    listB = _etree_to_list(rootB)

    '''
    compare the lists
    ratio()
    returns a measure of the lists similarity as a float in the range [0, 1].
    '''
    sm = difflib.SequenceMatcher(None, listA, listB)
    print("Similarity: {}".format(round(sm.ratio(), 3)))

    if print_diff:
        # And visualise
        d = difflib.Differ()
        print("\n".join(list(d.compare(listA, listB))))


def _etree_to_list(root):
    """
    Turns a collation in etree to a list for evaluation purposes
    :param root: root element of the collation tree to turn into list
    :return: a list
    """
    # TODO: handle imbrication when necessary (for now, just one app level)
    myList = []
    for app in root.iter("app"):
        for rdg in  app.xpath(".//rdg/text()"):
            myList.append(rdg)
        myList.append("|") # separator between apps -> keep it or not?

    return myList
