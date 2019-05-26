#!usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
from collatex import *
import json
import graphviz

def XMLtoJson(id,xmlInput):
    # converts an XML tokenised and annotated input to JSON for collation
    witness = {}
    witness['id'] = id
    monXSL = etree.XML('''
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs"
    version="1.0">

    <xsl:output method="text"/>

    <xsl:template match="/">
        <xsl:apply-templates
            select="descendant::tei:w"/>
    </xsl:template>

    <xsl:template match="tei:w">
        <xsl:text>{"form": "</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>", "xml:id": "</xsl:text>
        <xsl:value-of select="@xml:id"/>
        <xsl:text>", "t": "</xsl:text>
        <xsl:value-of select="@lemma"/>
        <xsl:text>", "POS": "</xsl:text>
        <xsl:value-of select="substring-before(@type, '|')"/>
        <xsl:text>", "morph": "</xsl:text>
        <xsl:value-of select="substring-after(@type, '|')"/>
        <xsl:text>"}</xsl:text>
        <xsl:if test="following::tei:w">
            <xsl:text>, </xsl:text>
        </xsl:if>
    </xsl:template>
</xsl:stylesheet>
    ''')
    monXSL = etree.XSLT(monXSL)
    witness['tokens'] = json.loads( '[' +str(monXSL(xmlInput)) +']')
    return witness


#Redefining a core function to have other attributes
def table_to_xml(table):
    readings = []
    for column in table.columns:
        app = etree.Element('app')
        for key, value in sorted(column.tokens_per_witness.items()):
            child = etree.Element('rdg')
            child.attrib['wit'] = "#" + key
            child.text = "".join(str(item.token_data["form"]) for item in value)
            #TODO: redéfinir pour accepter un nombre arbitraire d'éléments et faire ça proprement
            #TODO: apparemment, aussi, il ne veut pas d'xml:id
            child.attrib['id'] = "".join(str(item.token_data["xml:id"]) for item in value)
            child.attrib['lemma'] = "".join(str(item.token_data["t"]) for item in value)
            child.attrib['POS'] = "".join(str(item.token_data["POS"]) for item in value)
            child.attrib['morph'] = "".join(str(item.token_data["morph"]) for item in value)
            app.append(child)
        # Without the encoding specification, outputs bytes instead of a string
        result = etree.tostring(app, encoding="unicode")
        readings.append(result)
    return "<root>" + "".join(readings) + "</root>"
