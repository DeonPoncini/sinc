#!/usr/bin/python

from lxml import etree

xmlschema_doc = etree.parse('schema.xsd')
xmlschema = etree.XMLSchema(xmlschema_doc)

doc = etree.parse('example.xml')
print xmlschema.assertValid(doc)
