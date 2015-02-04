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
        'static':'static', \
        'constant':'const', \
}

class CVisitor(AstVisitor):
    def folder(self):
        return 'c'
    def extension(self):
        return '.h'
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
    def write_namespace(self, ns):
        self.nsprefix = self.nsprefix + ns + '_'
    def write_enumeration_name(self, name):
        self.enum_name = name
        self.outfile.write('typedef enum {\n')
    def write_enumeration_entry(self, entry):
        self.outfile.write('\t' + self.nsprefix + self.enum_name + \
                '_' + entry + ',\n')
    def write_enumeration_close(self, name):
        self.outfile.write('} ' + self.nsprefix + name + ';\n')
    def write_assignment(self, assignment):
        self.write_typedecl(assignment.typedecl)
        self.outfile.write(assignment.name)
        self.outfile.write(' = ')
        self.outfile.write(assignment.value)
        self.outfile.write(';\n')
    def write_type(self, typename):
        if typename.base in c_data_types:
            self.outfile.write(c_data_types[typename.base] + ' ')
        else:
            self.outfile.write(self.nsprefix + typename.base + ' ')
    def write_typedecl(self, typedecl):
        for m in typedecl.modifiers:
            self.outfile.write(c_data_types[m] + ' ')
        self.write_type(typedecl.typename)
    def write_structure_name(self, name):
        self.outfile.write('typedef struct {\n')
    def write_declaration(self, declaration):
        self.outfile.write('\t')
        self.write_typedecl(declaration.typedecl)
        self.outfile.write(declaration.name)
        self.outfile.write(';\n')
    def write_structure_close(self, name):
        self.outfile.write('} ' + self.nsprefix + name + ';\n')
    def write_outro(self):
        self.outfile.write('#ifdef __cplusplus\n')
        self.outfile.write('}\n')
        self.outfile.write('#endif\n')
        self.outfile.write('#endif\n')
