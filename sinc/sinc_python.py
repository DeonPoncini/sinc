#!/usr/bin/python

################################################################################
# sinc-java
# generate Java code
################################################################################

import codecs
import os.path

def write_python(ast, outPath, fileName):
    fullPath = os.path.join(outPath, 'python')
    if not os.path.exists(fullPath):
        os.makedirs(fullPath)
    outfile = codecs.open(os.path.join(fullPath, fileName + '.py'), 'w', 'utf-8')

    outfile.write('#!/usr/bin/python\n')
    # create an enum type
    outfile.write('def enum(*sequential, **named):\n')
    outfile.write('\tenums = dict(zip(sequential, range(len(sequential))),')
    outfile.write('**named)\n')
    outfile.write('\treverse = dict((key, value) for key, value in ')
    outfile.write('enums.iteritems())\n')
    outfile.write('\tenums[\'reverse_mapping\'] = reverse\n')
    outfile.write('\treturn type(\'Enum\', (), enums)\n')

    # enumerations
    for e in ast.enumerations:
        outfile.write(e.name + ' = enum(')
        outstr = ''
        for entry in e.entries:
            outstr = outstr + '\'' + entry + '\','
        outstr = outstr[:-1]
        outfile.write(outstr + ')\n')

    # constants
    for c in ast.constants:
        outfile.write(c.name + ' = ' + c.value + '\n')

    # structs
    for s in ast.structures:
        outfile.write('class ' + s.name + ':\n')
        outfile.write('\tdef __init__(self')
        for e in s.elements:
            outfile.write(', ' + e.name)
        outfile.write('):\n')
        for e in s.elements:
            outfile.write('\t\tself.' + e.name + ' = ' + e.name + '\n')

