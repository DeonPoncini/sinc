#!/usr/bin/python

################################################################################
# sinc-c
# generate C code
################################################################################

import codecs
import os.path

from sinc_ast import AstVisitor

c_data_types = { \
        'string':'char*', \
        'unsigned':'unsigned', \
        'int':'int', \
}

class CVisitor(AstVisitor):
    def folder(self):
        return 'c'
    def full_filename(self):
        return self.filename + '.h'
    def write_intro(self):
        guard=""
        for n in self.ast.package.ns:
            guard = guard + n.upper() + '_'
        guard += self.filename.upper() + '_H_C'
        self.outfile.write('#ifndef ' + guard + '\n')
        self.outfile.write('#define ' + guard + '\n')
        self.outfile.write('#ifdef __cplusplus\n')
        self.outfile.write('extern "C" {\n')
        self.outfile.write('#endif\n')
        self.nsprefix = ""
    def write_package(self, package):
        self.nsprefix = self.nsprefix + package + '_'
    def write_enumeration_name(self, name):
        self.enum_name = name
        self.outfile.write('typedef enum {\n')
    def write_enumeration_entry(self, entry):
        self.outfile.write('\t' + self.nsprefix + self.enum_name + \
                '_' + entry + ',\n')
    def write_enumeration_close(self, name):
        self.outfile.write('} ' + self.nsprefix + name + ';\n')
    def write_constant(self, dataType, name, value):
        self.outfile.write('static const ' + c_data_types[dataType] + ' ' \
                + self.nsprefix + name + ' = ' + value + ';\n')
    def write_structure_name(self, name):
        self.outfile.write('typedef struct {\n')
    def write_structure_element(self, dataType, name):
        if dataType in c_data_types:
            self.outfile.write('\t' + c_data_types[dataType] + \
                    ' ' + name + ';\n')
        else:
            self.outfile.write('\t' + self.nsprefix + dataType + \
                    ' ' + name + ';\n')
    def write_structure_close(self, name):
        self.outfile.write('} ' + self.nsprefix + name + ';\n')
    def write_outro(self):
        self.outfile.write('#ifdef __cplusplus\n')
        self.outfile.write('}\n')
        self.outfile.write('#endif\n')
        self.outfile.write('#endif\n')
