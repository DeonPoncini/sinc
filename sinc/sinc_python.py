
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
    def full_filename(self):
        return self.filename + '.py'
    def write_intro(self):
        self.outfile.write('#!/usr/bin/python\n')
        # create an enum type
        self.outfile.write('def enum(*sequential, **named):\n')
        self.outfile.write('\tenums = dict(zip(sequential, range(len(sequential))),')
        self.outfile.write('**named)\n')
        self.outfile.write('\treverse = dict((key, value) for key, value in ')
        self.outfile.write('enums.iteritems())\n')
        self.outfile.write('\tenums[\'reverse_mapping\'] = reverse\n')
        self.outfile.write('\treturn type(\'Enum\', (), enums)\n')
    def write_enumeration_name(self, name):
        self.outfile.write(name + ' = enum(')
        self.outstr = ''
    def write_enumeration_entry(self, entry):
        self.outstr = self.outstr + '\'' + entry + '\','
    def write_enumeration_close(self, name):
        self.outstr = self.outstr[:-1]
        self.outfile.write(self.outstr + ')\n')
    def write_constant(self, dataType, name, value):
        self.outfile.write(name + ' = ' + value + '\n')
    def write_structure_name(self, name):
        self.outfile.write('class ' + name + ':\n')
        self.outfile.write('\tdef __init__(self')
        self.struct_elements = []
    def write_structure_element(self, dataType, name):
        self.outfile.write(', ' + name)
        self.struct_elements.append(name)
    def write_structure_close(self, name):
        self.outfile.write('):\n')
        for n in self.struct_elements:
            self.outfile.write('\t\tself.' + n + ' = ' + n + '\n')
