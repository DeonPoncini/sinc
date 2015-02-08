
################################################################################
# sinc-java
# generate Java code
################################################################################

import codecs
import os.path

from sinc_ast import AstVisitor

class PythonVisitor(AstVisitor):
    def folder(self):
        return 'python'
    def extension(self):
        return '.py'
    def write_intro(self):
        # create an enum type
        return '#!/usr/bin/python\n' +\
            'def enum(*sequential, **named):\n' +\
            '\tenums = dict(zip(sequential, range(len(sequential))),' +\
            '**named)\n' +\
            '\treverse = dict((key, value) for key, value in ' +\
            'enums.iteritems())\n' +\
            '\tenums[\'reverse_mapping\'] = reverse\n' +\
            '\treturn type(\'Enum\', (), enums)\n'
    def write_enumeration_name(self, name):
        self.ret = ''
        return name + ' = enum('
    def write_enumeration_entry(self, entry):
        self.ret = self.ret + '\'' + entry + '\','
        return ''
    def write_enumeration_close(self, name):
        self.ret = self.ret[:-1]
        return self.ret + ')\n'
    def write_assignment(self, assignment):
        return assignment.name + ' = ' + assignment.value + '\n'
    def write_structure_name(self, name):
        self.struct_elements = []
        return 'class ' + name + ':\n' +\
            '\tdef __init__(self'
    def write_declaration(self, declaration):
        self.struct_elements.append(declaration.name)
        return ', ' + declaration.name
    def write_structure_close(self, name):
        ret = '):\n'
        for n in self.struct_elements:
            ret = ret + '\t\tself.' + n + ' = ' + n + '\n'
        return ret
