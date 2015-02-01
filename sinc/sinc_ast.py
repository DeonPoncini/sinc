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

class Constant:
    def __init__(self, name, dataType, value):
        self.name = name
        self.dataType = dataType
        self.value = value

class Structure:
    def __init__(self, name):
        self.name = name
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

class Ast:
    def __init__(self, package):
        self.package = package
        self.enumerations = []
        self.constants = []
        self.structures = []

    def add_enum(self, enumeration):
        self.enumerations.append(enumeration)

    def add_constant(self, constant):
        self.constants.append(constant)

    def add_structure(self, structure):
        self.structures.append(structure)

class AstVisitor:
    def __init__(self, ast, outpath, filename):
        self.ast = ast
        self.outpath = outpath
        self.filename = filename
    def folder(self):
        pass
    def full_filename(self):
        pass
    def open_file(self):
        fullpath = os.path.join(self.outpath, self.folder())
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)
        self.outfile = codecs.open(os.path.join(fullpath, \
                self.full_filename()), 'w', 'utf-8')
    def write_intro(self):
        pass
    def write_package(self, package):
        pass
    def write_enumeration_name(self, name):
        pass
    def write_enumeration_entry(self, entry):
        pass
    def write_enumeration_close(self, name):
        pass
    def write_constant(self, dataType, name, value):
        pass
    def write_structure_name(self, name):
        pass
    def write_structure_element(self, dataType, name):
        pass
    def write_structure_close(self, name):
        pass
    def write_outro(self):
        pass
    def write_ast(self):
        self.open_file()
        self.write_intro()
        for n in self.ast.package.ns:
            self.write_package(n)

        for e in self.ast.enumerations:
            self.write_enumeration_name(e.name)
            for entry in e.entries:
                self.write_enumeration_entry(entry)
            self.write_enumeration_close(e.name)

        for c in self.ast.constants:
            self.write_constant(c.dataType, c.name, c.value)

        for s in self.ast.structures:
            self.write_structure_name(s.name)
            for e in s.elements:
                self.write_structure_element(e.dataType, e.name)
            self.write_structure_close(s.name)

        self.write_outro()

