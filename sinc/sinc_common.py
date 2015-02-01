#!/usr/bin/python

################################################################################
# common
# common data structures
################################################################################

# data structures
class Package:
    def __init__(self, uri, ns):
        self.uri = uri
        self.ns = ns

class Enumeration:
    def __init__(self, name, entries):
        self.name = name
        self.entries = entries

class Constant:
    def __init__(self, name, dataType, value):
        self.name = name
        self.dataType = dataType
        self.value = value

class Structure:
    def __init__(self, name, elements):
        self.name = name
        self.elements = elements
