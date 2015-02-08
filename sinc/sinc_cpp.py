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
        return '#ifndef ' + guard + '\n' +\
            '#define ' + guard + '\n' +\
            '#include <string>\n'
    def write_namespace(self, ns):
        return 'namespace ' + ns + ' {\n'
    def write_enumeration_name(self, name):
        return 'enum class ' + name + ' {\n'
    def write_enumeration_entry(self, entry):
        return '\t' + entry + ',\n'
    def write_enumeration_close(self, name):
        return '};\n'
    def write_assignment(self, assignment):
        return self.write_typedecl(assignment.typedecl) +\
            assignment.name + ' = ' + assignment.value + ';\n'
    def write_type(self, typename):
        ret = ''
        if typename.base in cpp_data_types:
            ret = ret + cpp_data_types[typename.base] + ' '
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
            ret = ret + cpp_data_types[m] + ' '
        return ret + self.write_type(typedecl.typename)
    def write_structure_name(self, name):
        return 'struct ' + name + ' {\n'
    def write_declaration(self, declaration):
        return '\t' + self.write_typedecl(declaration.typedecl) +\
            declaration.name + ';\n'
    def write_structure_close(self, name):
        return '};\n'
    def write_outro(self):
        ret = ''
        for n in self.ast.package.ns:
            ret = ret + '}\n'
        return ret + '#endif\n'
