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
        self.guard=""
        for n in self.ast.package.ns:
            self.guard = self.guard + n.upper() + '_'
        self.guard += self.filename.upper() + '_H_C'
        self.nsprefix = ""
        return '#ifndef ' + self.guard + '\n' +\
            '#define ' + self.guard + '\n' +\
            '#ifdef __cplusplus\n' +\
            'extern "C" {\n' +\
            '#endif\n'
    def write_namespace(self, ns):
        self.nsprefix = self.nsprefix + ns + '_'
        return ''
    def write_enumeration_name(self, name):
        self.enum_name = name
        return 'typedef enum {\n'
    def write_enumeration_entry(self, entry):
        return '\t' + self.nsprefix + self.enum_name +\
                '_' + entry + ',\n'
    def write_enumeration_close(self, name):
        return '} ' + self.nsprefix + name + ';\n'
    def write_assignment(self, assignment):
        return self.write_typedecl(assignment.typedecl) +\
            assignment.name + ' = ' + assignment.value + ';\n'
    def write_type(self, typename):
        if typename.base in c_data_types:
            return c_data_types[typename.base] + ' '
        else:
            return self.nsprefix + typename.base + ' '
    def write_typedecl(self, typedecl):
        self.ret = ''
        for m in typedecl.modifiers:
            self.ret = self.ret + c_data_types[m] + ' '
        return self.ret + self.write_type(typedecl.typename)
    def write_structure_name(self, name):
        return 'typedef struct {\n'
    def write_declaration(self, declaration):
        return '\t' +\
            self.write_typedecl(declaration.typedecl) + declaration.name + ';\n'
    def write_structure_close(self, name):
        return '} ' + self.nsprefix + name + ';\n'
    def write_outro(self):
        return '#ifdef __cplusplus\n' +\
            '}\n' +\
            '#endif\n' +\
            '#endif\n'
