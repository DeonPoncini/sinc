#!/usr/bin/python

################################################################################
# ast
# Abstract syntax tree
################################################################################

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
