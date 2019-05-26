#!usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import json


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
        <xsl:text>{"t": "</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>", "xml:id": "</xsl:text>
        <xsl:value-of select="@xml:id"/>
        <xsl:text>", "lemma": "</xsl:text>
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

