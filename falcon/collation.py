#!usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import etree
import json
import glob
import os

def XMLtoJson(siglum, xmlinput):
    """
    Converts an XML tokenised and annotated input to JSON for collation
    :param siglum: identifier of the witness (a string)
    :param xmlinput: XML input (an etree XML document)
    :return: JSON content to be used for collation
    """
    witness = {"id": siglum}
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
        <xsl:text>", "pos": "</xsl:text>
        <xsl:choose>
            <xsl:when test="@pos">
                <xsl:value-of select="@pos"/>
            </xsl:when>
            <xsl:when test="contains(@type, '|')">
                <xsl:value-of select="substring-before(@type, '|')"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="@type"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>", "morph": "</xsl:text>
        <xsl:choose>
            <xsl:when test="@msd">
                <xsl:value-of select="@msd"/>
            </xsl:when>
            <xsl:when test="contains(@type, '|')">
                <xsl:value-of select="substring-after(@type, '|')"/>
            </xsl:when>
            <xsl:otherwise/>
        </xsl:choose>
        <xsl:text>"}</xsl:text>
        <xsl:if test="following::tei:w">
            <xsl:text>, </xsl:text>
        </xsl:if>
    </xsl:template>
</xsl:stylesheet>
    ''')
    monXSL = etree.XSLT(monXSL)
    witness['tokens'] = json.loads('[' + str(monXSL(xmlinput)) + ']')
    return witness


def table_to_xml(table):
    """
    Redefining a core collatex function to have other attributes
    :param table: a collatex table
    :return: an XML collated document, with all the attributes existing in the input
    """
    readings = []
    for column in table.columns:
        app = etree.Element('app')
        for key, value in sorted(column.tokens_per_witness.items()):
            child = etree.Element('rdg')
            child.attrib['wit'] = "#" + key
            child.text = "".join(str(item.token_data["form"]) for item in value)
            # TODO: redéfinir pour accepter un nombre arbitraire d'éléments et faire ça proprement
            # TODO: apparemment, aussi, il ne veut pas d'xml:id
            child.attrib['id'] = "".join(str(item.token_data["xml:id"]) for item in value)
            child.attrib['lemma'] = "".join(str(item.token_data["t"]) for item in value)
            child.attrib['pos'] = "".join(str(item.token_data["pos"]) for item in value)
            child.attrib['msd'] = "".join(str(item.token_data["morph"]) for item in value)
            app.append(child)
        # Without the encoding specification, outputs bytes instead of a string
        result = etree.tostring(app, encoding="unicode")
        readings.append(result)
    return "<root>" + "".join(readings) + "</root>"


def load_annotated_folder(path):
    """
    Loads an entire directory containing files in the expected xml input format.
    :param path: path to the directory containing the files
    :return: a dictionary containing a witnesses key, containing pairs with identifier and xml content
    """
    files = glob.glob(path+'/*.xml')
    content = {}
    for f in files:
        with open(f, 'r') as myFile:
            content[os.path.splitext(os.path.split(f)[-1])[0]] = etree.parse(myFile)

    output = {'witnesses': [XMLtoJson(c, content[c]) for c in content]}

    return output
