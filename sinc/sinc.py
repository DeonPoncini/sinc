#!/usr/bin/python

################################################################################
# sinc
# reads a data XML file and generates code in various languages
################################################################################

import sys

from lxml import etree

from sinc_ast import Package, Enumeration, Type, Typedecl, \
        Assignment, Declaration, Structure, Ast

from sinc_c import CVisitor
from sinc_cpp import CppVisitor
from sinc_java import JavaVisitor
from sinc_python import PythonVisitor

def read_package(p):
    uri = p.findall('uri')[0].text
    namespace = p.findall('namespaces')[0].findall('namespace')
    package = Package(uri)
    for n in namespace:
        package.add_namespace(n.text)
    return package

def read_enumeration(e):
    name = e.findall('name')[0].text
    entries = e.findall('entries')[0]
    entry = entries.findall('entry')
    enumeration = Enumeration(name)
    for e1 in entry:
        enumeration.add_entry(e1.text)
    return enumeration

def read_type(t):
    base = t.findall('base')[0].text
    templates = t.findall('templates')
    typename = Type(base)
    if templates:
        template = templates[0].findall('typedecl')
        for t1 in template:
            typename.append(read_typedecl(t1))
    return typename

def read_typedecl(t):
    typename = read_type(t.findall('type')[0])
    typedecl = Typedecl(typename)
    modifiers = t.findall('modifiers')
    if modifiers:
        modifier = modifiers[0].findall('modifier')
        for m in modifier:
            typedecl.add_modifier(m.text)
    return typedecl

def read_assignment(a):
    name = a.findall('name')[0].text
    typedecl = read_typedecl(a.findall('typedecl')[0])
    value = a.findall('value')[0].text
    return Assignment(name, typedecl, value)

def read_declaration(d):
    name = d.findall('name')[0].text
    typedecl = read_typedecl(d.findall('typedecl')[0])
    return Declaration(name, typedecl)

def read_structs(s):
    name = s.findall('name')[0].text
    structure = Structure(name)
    declarations = s.findall('declarations')
    if declarations:
        declaration = declarations[0].findall('declaration')
        for d in declaration:
            structure.add_declaration(read_declaration(d))
    return structure

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
filename = root.attrib['name']

packages = root.findall('package')
ast = Ast(read_package(packages[0]))

enums = root.findall('enum')
for e in enums:
    ast.add_enum(read_enumeration(e))

assignments = root.findall('assignment')
for a in assignments:
    ast.add_assignment(read_assignment(a))

structs = root.findall('struct')
for s in structs:
    ast.add_structure(read_structs(s))

cppVisitor = CppVisitor(ast, outPath, filename)
cppVisitor.write_ast()

cVisitor = CVisitor(ast, outPath, filename)
cVisitor.write_ast()

javaVisitor = JavaVisitor(ast, outPath, filename)
javaVisitor.write_ast()

pythonVisitor = PythonVisitor(ast, outPath, filename)
pythonVisitor.write_ast()
