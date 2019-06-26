from lxml import etree

def categorise(xml_input):
    xml_data = etree.XML(xml_input)
    output = []
    features = ['lemma', 'pos', 'msd']

    for app in xml_data.findall('//app'):
        myApp = etree.Element("app")

        lemmas = {rdg.get("lemma") for rdg in app.findall("./rdg")}
        if len(lemmas) > 1:
            myApp.attrib["type"] = "lexical"

        else:





