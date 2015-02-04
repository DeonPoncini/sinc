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
        'static':'static', \
        'constant':'const', \
}

class CppVisitor(AstVisitor):
    def folder(self):
        return 'cpp'
    def extension(self):
        return '.h'
    def write_intro(self):
        guard=""
        for n in self.ast.package.ns:
            guard = guard + n.upper() + '_'
        guard += self.filename.upper() + '_H_CPP'
        self.outfile.write('#ifndef ' + guard + '\n')
        self.outfile.write('#define ' + guard + '\n')
        self.outfile.write('#include <string>\n')
    def write_namespace(self, ns):
        self.outfile.write('namespace ' + ns + ' {\n')
    def write_enumeration_name(self, name):
        self.outfile.write('enum class ' + name + ' {\n')
    def write_enumeration_entry(self, entry):
        self.outfile.write('\t' + entry + ',\n')
    def write_enumeration_close(self, name):
        self.outfile.write('};\n')
    def write_assignment(self, assignment):
        self.write_typedecl(assignment.typedecl)
        self.outfile.write(assignment.name)
        self.outfile.write(' = ')
        self.outfile.write(assignment.value)
        self.outfile.write(';\n')
    def write_type(self, typename):
        if typename.base in cpp_data_types:
            self.outfile.write(cpp_data_types[typename.base] + ' ')
        else:
            self.outfile.write(typename.base + ' ')
        if typename.templates:
            self.outfile.write('<')
            for t in typename.templates:
                self.outfile.write(t + ',')
            self.outfile.write('> ')
    def write_typedecl(self, typedecl):
        for m in typedecl.modifiers:
            self.outfile.write(cpp_data_types[m] + ' ')
        self.write_type(typedecl.typename)
    def write_structure_name(self, name):
        self.outfile.write('struct ' + name + ' {\n')
    def write_declaration(self, declaration):
        self.outfile.write('\t')
        self.write_typedecl(declaration.typedecl)
        self.outfile.write(declaration.name)
        self.outfile.write(';\n')
    def write_structure_close(self, name):
        self.outfile.write('};\n')
    def write_outro(self):
        for n in self.ast.package.ns:
            self.outfile.write('}\n')
        self.outfile.write('#endif\n')
