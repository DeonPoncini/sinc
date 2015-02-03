#!/usr/bin/python

################################################################################
# sinc
# reads a data XML file and generates code in various languages
################################################################################

import sys

from lxml import etree

from sinc_ast import Package, Enumeration, Constant, Structure, Ast
from sinc_c import CVisitor
from sinc_cpp import CppVisitor
from sinc_java import JavaVisitor
from sinc_python import PythonVisitor

if len(sys.argv) < 4:
    print "Usage is: " + sys.argv[0] + " <xml> <outpath> <schema>"
    sys.exit(1)

doc = etree.parse(sys.argv[1])
outPath = sys.argv[2]
xmlschema_doc = etree.parse(sys.argv[3])
xmlschema = etree.XMLSchema(xmlschema_doc)

if not xmlschema.validate(doc):
    xmlschema.assertValid(doc)
    sys.exit(1)

root = doc.getroot()
fileName = root.attrib['name']

# get the package declaration
packages = doc.findall('package')

uri = packages[0].findall('uri')[0].text
namespace = packages[0].findall('namespaces')[0].findall('namespace')
package = Package(uri)
for n in namespace:
    package.add_namespace(n.text)
ast = Ast(package)

# parse all the enums
enums = root.findall('enum')
for e in enums:
    name = e.findall('name')[0].text
    entries = e.findall('entries')[0]
    entry = entries.findall('entry')
    enumeration = Enumeration(name)
    for e1 in entry:
        enumeration.add_entry(e1.text)
    ast.add_enum(enumeration)

# parse all the constants
constants = root.findall('assignment')
for c in constants:
    name = c.findall('name')[0].text
    dataType = c.findall('typedecl')[0].findall('type')[0].findall('base')[0].text
    value = c.findall('value')[0].text
    ast.add_constant(Constant(name, dataType, value))

# parse all the structs
structs = root.findall('struct')
for s in structs:
    name = s.findall('name')[0].text
    declarations = s.findall('declarations')[0]
    declaration = declarations.findall('declaration')
    structure = Structure(name)
    for d in declaration:
        name = d.findall('name')[0].text
        dataType = d.findall('typedecl')[0].findall('type')[0].findall('base')[0].text
        structure.add_element(Constant(name, dataType, 0))
    ast.add_structure(structure)

cppVisitor = CppVisitor(ast, outPath, fileName)
cppVisitor.write_ast()

cVisitor = CVisitor(ast, outPath, fileName)
cVisitor.write_ast()

javaVisitor = JavaVisitor(ast, outPath, fileName)
javaVisitor.write_ast()

pythonVisitor = PythonVisitor(ast, outPath, fileName)
pythonVisitor.write_ast()
