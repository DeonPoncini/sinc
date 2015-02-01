#!/usr/bin/python

################################################################################
# sinc
# reads a data XML file and generates code in various languages
################################################################################

import sys

from xml.dom import minidom

from sinc_ast import Package, Enumeration, Constant, Structure, Ast
from sinc_c import write_c
from sinc_cpp import write_cpp
from sinc_java import write_java
from sinc_python import write_python

if len(sys.argv) < 3:
    print "Usage is: " + sys.argv[0] + " <data.xml> <outpath> "
    sys.exit(1)

dataDom = minidom.parse(sys.argv[1])
outPath = sys.argv[2]

# get the output file name
datas = dataDom.getElementsByTagName('data')
if len(datas) > 1:
    print "Only one data element allowed"
    sys.exit(1)

fileName = datas[0].getAttribute('name')

# get the package declaration
packages = dataDom.getElementsByTagName('package')

if len(packages) > 1:
    print "Only one package element allowed"
    sys.exit(1)

uri = packages[0].getAttribute('uri')
namespace = packages[0].getElementsByTagName('namespace')
package = Package(uri)
for n in namespace:
    package.add_namespace(n.childNodes[0].nodeValue)
ast = Ast(package)

# parse all the enums
enums = dataDom.getElementsByTagName('enum')
for e in enums:
    name = e.getAttribute('name')
    entries = e.getElementsByTagName('entry')
    enumeration = Enumeration(name)
    for e1 in entries:
        enumeration.add_entry(e1.childNodes[0].nodeValue)
    ast.add_enum(enumeration)

# parse all the constants
constants = dataDom.getElementsByTagName('constant')
for c in constants:
    name = c.getAttribute('name')
    dataType = c.getAttribute('type')
    value = c.childNodes[0].nodeValue
    ast.add_constant(Constant(name, dataType, value))

# parse all the structs
structs = dataDom.getElementsByTagName('struct')
for s in structs:
    name = s.getAttribute('name')
    elements = s.getElementsByTagName('element')
    structure = Structure(name)
    for e in elements:
        name = e.childNodes[0].nodeValue
        dataType = e.getAttribute('type')
        structure.add_element(Constant(name, dataType, 0))
    ast.add_structure(structure)

write_cpp(ast, outPath, fileName)
write_c(ast, outPath, fileName)
write_java(ast, outPath, fileName)
write_python(ast, outPath, fileName)

