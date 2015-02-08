#!/usr/bin/python

################################################################################
# sinc-java
# generate Java code ################################################################################
import codecs
import os.path

from sinc_ast import AstVisitor

java_data_types = { \
        'string':'String', \
        'unsigned':'int', \
        'int':'int', \
        'static':'static', \
        'constant':'final', \
}

class JavaVisitor(AstVisitor):
    def folder(self):
        self.paths = self.ast.package.uri.split(".")
        self.paths.reverse()
        for n in self.ast.package.ns:
            self.paths.append(n)
        return os.path.join('java', *self.paths)
    def extension(self):
        return '.java'
    def write_intro(self):
        packageName = ''
        for p in self.paths:
            packageName = packageName + p + '.'
        packageName = packageName[:-1]
        self.outfile.write('package ' + packageName + ';\n')
        self.outfile.write('public class ' + self.filename + ' {\n')
    def write_enumeration_name(self, name):
        self.outfile.write('public enum ' + name + ' {\n')
    def write_enumeration_entry(self, entry):
        self.outfile.write('\t' + entry + ',\n')
    def write_enumeration_close(self, name):
        self.outfile.write('}\n')
    def write_assignment(self, assignment):
        self.outfile.write('public ')
        self.write_typedecl(assignment.typedecl)
        self.outfile.write(assignment.name)
        self.outfile.write(' = ')
        self.outfile.write(assignment.value)
        self.outfile.write(';\n')
    def write_type(self, typename):
        if typename.base in java_data_types:
            self.outfile.write(java_data_types[typename.base] + ' ')
        else:
            self.outfile.write(typename.base + ' ')
        if typename.templates:
            self.outfile.write('<')
            for t in typename.templates:
                self.write_typedecl(self, t)
                self.outfile.write(',')
            self.outfile.write('> ')
    def write_typedecl(self, typedecl):
        for m in typedecl.modifiers:
            self.outfile.write(java_data_types[m] + ' ')
        self.write_type(typedecl.typename)
    def write_structure_name(self, name):
        self.outfile.write('public static class ' + name + '{\n')
    def write_declaration(self, declaration):
        self.outfile.write('\tpublic ')
        self.write_typedecl(declaration.typedecl)
        self.outfile.write(declaration.name)
        self.outfile.write(';\n')
    def write_structure_close(self, name):
        self.outfile.write('}\n')
    def write_outro(self):
        self.outfile.write('}\n')
