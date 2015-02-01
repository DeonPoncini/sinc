#!/usr/bin/python

################################################################################
# sinc-cpp
# generate C++ code
################################################################################

import codecs
import os.path

from sinc_ast import AstVisitor

cpp_data_types = { \
        'string':'std::string', \
        'unsigned':'unsigned', \
        'int':'int', \
}

class CppVisitor(AstVisitor):
    def folder(self):
        return 'cpp'
    def full_filename(self):
        return self.filename + '.h'
    def write_intro(self):
        guard=""
        for n in self.ast.package.ns:
            guard = guard + n.upper() + '_'
        guard += self.filename.upper() + '_H_CPP'
        self.outfile.write('#ifndef ' + guard + '\n')
        self.outfile.write('#define ' + guard + '\n')
        self.outfile.write('#include <string>\n')
    def write_package(self, package):
        self.outfile.write('namespace ' + package + ' {\n')
    def write_enumeration_name(self, name):
        self.outfile.write('enum class ' + name + ' {\n')
    def write_enumeration_entry(self, entry):
        self.outfile.write('\t' + entry + ',\n')
    def write_enumeration_close(self, name):
        self.outfile.write('};\n')
    def write_constant(self, dataType, name, value):
        self.outfile.write('static const ' + cpp_data_types[dataType] + ' ' \
                + name + ' = ' + value + ';\n')
    def write_structure_name(self, name):
        self.outfile.write('struct ' + name + ' {\n')
    def write_structure_element(self, dataType, name):
            if dataType in cpp_data_types:
                self.outfile.write('\t' + cpp_data_types[dataType] + ' ' \
                        + name + ';\n')
            else:
                self.outfile.write('\t' + dataType + ' ' + name + ';\n')
    def write_structure_close(self, name):
        self.outfile.write('};\n')
    def write_outro(self):
        for n in self.ast.package.ns:
            self.outfile.write('}\n')

        self.outfile.write('#endif\n')
