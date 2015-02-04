#!/usr/bin/python

################################################################################
# ast
# Abstract syntax tree
################################################################################

import codecs
import os.path

class Package:
    def __init__(self, uri):
        self.uri = uri
        self.ns = []

    def add_namespace(self, ns):
        self.ns.append(ns)

class Enumeration:
    def __init__(self, name):
        self.name = name
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

class Type:
    def __init__(self, base):
        self.base = base
        self.templates = []

    def add_template(self, template):
        self.templates.append(template)

class Typedecl:
    def __init__(self, typename):
        self.typename = typename
        self.modifiers = []

    def add_modifier(self, modifier):
        self.modifiers.append(modifier)

class Assignment:
    def __init__(self, name, typedecl, value):
        self.name = name
        self.typedecl = typedecl
        self.value = value

class Declaration:
    def __init__(self, name, typedecl):
        self.name = name
        self.typedecl = typedecl

class Structure:
    def __init__(self, name):
        self.name = name
        self.declarations = []

    def add_declaration(self, declaration):
        self.declarations.append(declaration)

class Ast:
    def __init__(self, package):
        self.package = package
        self.enumerations = []
        self.assignments = []
        self.structures = []

    def add_enum(self, enumeration):
        self.enumerations.append(enumeration)

    def add_assignment(self, assignment):
        self.assignments.append(assignment)

    def add_structure(self, structure):
        self.structures.append(structure)

class AstVisitor:
    def __init__(self, ast, outpath, filename):
        self.ast = ast
        self.outpath = outpath
        self.filename = filename
    def folder(self):
        pass
    def extension(self):
        pass
    def open_file(self):
        fullpath = os.path.join(self.outpath, self.folder())
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)
        self.outfile = codecs.open(os.path.join(fullpath, \
                self.filename + self.extension()), 'w', 'utf-8')
    def write_intro(self):
        pass
    def write_uri(self, uri):
        pass
    def write_namespace(self, ns):
        pass
    def write_enumeration_name(self, name):
        pass
    def write_enumeration_entry(self, enumeration):
        pass
    def write_enumeration_close(self, name):
        pass
    def write_typedecl(self, typedecl):
        pass
    def write_assignment(self, assignment):
        pass
    def write_modifier(self, modifier):
        pass
    def write_declaration(self, declaration):
        pass
    def write_outro(self):
        pass
    def write_ast(self):
        self.open_file()
        self.write_intro()

        self.write_uri(self.ast.package.uri)
        for n in self.ast.package.ns:
            self.write_namespace(n)

        for e in self.ast.enumerations:
            self.write_enumeration_name(e.name)
            for entry in e.entries:
                self.write_enumeration_entry(entry)
            self.write_enumeration_close(e.name)

        for a in self.ast.assignments:
            self.write_assignment(a)

        for s in self.ast.structures:
            self.write_structure_name(s.name)
            for d in s.declarations:
                self.write_declaration(d)
            self.write_structure_close(s.name)

        self.write_outro()

