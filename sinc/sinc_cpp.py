#!/usr/bin/python

################################################################################
# sinc-cpp
# generate C++ code
################################################################################

import codecs
import os.path

from sinc_common import Ast

cpp_data_types = { \
        'string':'std::string', \
        'unsigned':'unsigned', \
        'int':'int', \
}

def write_cpp(ast, outPath, fileName):
    fullPath = os.path.join(outPath, 'cpp')
    if not os.path.exists(fullPath):
        os.makedirs(fullPath)
    outfile = codecs.open(os.path.join(fullPath, fileName + '.h'), 'w', 'utf-8')
    guard=""
    for n in ast.package.ns:
        guard = guard + n.upper() + '_'
    guard += fileName.upper() + '_H_CPP'
    outfile.write('#ifndef ' + guard + '\n')
    outfile.write('#define ' + guard + '\n')
    outfile.write('#include <string>\n')
    for n in ast.package.ns:
        outfile.write('namespace ' + n + ' {\n')

    # enumerations
    for e in ast.enumerations:
        outfile.write('enum class ' + e.name + ' {\n')
        for entry in e.entries:
            outfile.write('\t' + entry + ',\n')
        outfile.write('};\n')

    # constants
    for c in ast.constants:
        outfile.write('static const ' + cpp_data_types[c.dataType] + ' ' \
                + c.name + ' = ' + c.value + ';\n')

    # structs
    for s in ast.structures:
        outfile.write('struct ' + s.name + ' {\n')
        for e in s.elements:
            if e.dataType in cpp_data_types:
                outfile.write('\t' + cpp_data_types[e.dataType] + ' ' \
                        + e.name + ';\n')
            else:
                outfile.write('\t' + e.dataType + ' ' + e.name + ';\n')
        outfile.write('};\n')

    for n in ast.package.ns:
        outfile.write('}\n')

    outfile.write('#endif\n')

