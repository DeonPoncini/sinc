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
        return 'package ' + packageName + ';\n' +\
            'public class ' + self.filename + ' {\n'
    def write_enumeration_name(self, name):
        return 'public enum ' + name + ' {\n'
    def write_enumeration_entry(self, entry):
        return '\t' + entry + ',\n'
    def write_enumeration_close(self, name):
        return '}\n'
    def write_assignment(self, assignment):
        return 'public ' + self.write_typedecl(assignment.typedecl) +\
            assignment.name + ' = ' + assignment.value + ';\n'
    def write_type(self, typename):
        ret = ''
        if typename.base in java_data_types:
            ret = ret + java_data_types[typename.base] + ' '
        else:
            ret = ret + typename.base + ' '
        if typename.templates:
            ret = ret + '<'
            for t in typename.templates:
                ret = ret + self.write_typedecl(t)
                ret = ret + ','
            ret = ret[:-1]
            ret = ret + '> '
        return ret
    def write_typedecl(self, typedecl):
        ret = ''
        for m in typedecl.modifiers:
            ret = ret + java_data_types[m] + ' '
        return ret + self.write_type(typedecl.typename)
    def write_structure_name(self, name):
        return 'public static class ' + name + '{\n'
    def write_declaration(self, declaration):
        return '\tpublic ' + self.write_typedecl(declaration.typedecl) +\
            declaration.name + ';\n'
    def write_structure_close(self, name):
        return '}\n'
    def write_outro(self):
        return '}\n'
