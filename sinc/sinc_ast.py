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
        return ''
    def extension(self):
        return ''
    def open_file(self):
        fullpath = os.path.join(self.outpath, self.folder())
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)
        self.outfile = codecs.open(os.path.join(fullpath, \
                self.filename + self.extension()), 'w', 'utf-8')
    def include_type(self, includemap, includes, typedecl):
        if typedecl.typename.base in includemap:
            if not includemap[typedecl.typename.base] in includes:
                includes = includes + includemap[typedecl.typename.base]
        for t in typedecl.typename.templates:
            includes = includes + include_type(includes, t)
        return includes
    def write_includes(self, includemap):
        includes = ''
        for a in self.ast.assignments:
            includes = self.include_type(includemap, includes, a.typedecl)
        for s in self.ast.structures:
            for d in s.declarations:
                includes = self.include_type(includemap, includes, d.typedecl)
        return includes
    def write_intro(self):
        return ''
    def write_uri(self, uri):
        return ''
    def write_namespace(self, ns):
        return ''
    def write_enumeration_name(self, name):
        return ''
    def write_enumeration_entry(self, enumeration):
        return ''
    def write_enumeration_close(self, name):
        return ''
    def write_typedecl(self, typedecl):
        return ''
    def write_assignment(self, assignment):
        return ''
    def write_modifier(self, modifier):
        return ''
    def write_declaration(self, declaration):
        return ''
    def write_outro(self):
        return ''
    def write_ast(self):
        self.open_file()
        outstr = self.write_intro()

        outstr += self.write_uri(self.ast.package.uri)
        for n in self.ast.package.ns:
            outstr += self.write_namespace(n)

        for e in self.ast.enumerations:
            outstr += self.write_enumeration_name(e.name)
            for entry in e.entries:
                outstr += self.write_enumeration_entry(entry)
            outstr += self.write_enumeration_close(e.name)

        for a in self.ast.assignments:
            outstr += self.write_assignment(a)

        for s in self.ast.structures:
            outstr += self.write_structure_name(s.name)
            for d in s.declarations:
                outstr += self.write_declaration(d)
            outstr += self.write_structure_close(s.name)

        outstr += self.write_outro()
        self.outfile.write(outstr)

