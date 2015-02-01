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
}

class JavaVisitor(AstVisitor):
    def folder(self):
        self.paths = self.ast.package.uri.split(".")
        self.paths.reverse()
        for n in self.ast.package.ns:
            self.paths.append(n)

        return os.path.join('java', *self.paths)
    def full_filename(self):
        return self.filename + '.java'
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
    def write_constant(self, dataType, name, value):
        self.outfile.write('public static final ' + java_data_types[dataType] + \
                ' ' + name + ' = ' + value + ';\n')
    def write_structure_name(self, name):
        self.outfile.write('public static class ' + name + '{\n')
    def write_structure_element(self, dataType, name):
        if dataType in java_data_types:
            self.outfile.write('\tpublic ' + java_data_types[dataType] + ' ' \
                    + name + ';\n')
        else:
            self.outfile.write('\tpublic ' + dataType + ' ' + name + ';\n')
    def write_structure_close(self, name):
        self.outfile.write('}\n')
    def write_outro(self):
        self.outfile.write('}\n')
