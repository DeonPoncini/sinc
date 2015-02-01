#!/usr/bin/python

################################################################################
# sinc-c
# generate C code
################################################################################

import codecs
import os.path

c_data_types = { \
        'string':'char*', \
        'unsigned':'unsigned', \
        'int':'int', \
}

def write_c(ast, outPath, fileName):
    fullPath = os.path.join(outPath, 'c')
    if not os.path.exists(fullPath):
        os.makedirs(fullPath)
    outfile = codecs.open(os.path.join(fullPath, fileName + '.h'), 'w', 'utf-8')
    guard=""
    for n in ast.package.ns:
        guard = guard + n.upper() + '_'
    guard += fileName.upper() + '_H_C'
    outfile.write('#ifndef ' + guard + '\n')
    outfile.write('#define ' + guard + '\n')
    outfile.write('#ifdef __cplusplus\n')
    outfile.write('extern "C" {\n')
    outfile.write('#endif\n')
    nsprefix = ""
    for n in ast.package.ns:
        nsprefix = nsprefix + n + '_'

    # enumerations
    for e in ast.enumerations:
        outfile.write('typedef enum {\n')
        for entry in e.entries:
            outfile.write('\t' + nsprefix + e.name + '_' + entry + ',\n')
        outfile.write('} ' + nsprefix + e.name + ';\n')

    # constants
    for c in ast.constants:
        outfile.write('static const ' + c_data_types[c.dataType] + ' ' \
                + nsprefix + c.name + ' = ' + c.value + ';\n')

    # structs
    for s in ast.structures:
        outfile.write('typedef struct {\n')
        for e in s.elements:
            if e.dataType in c_data_types:
                outfile.write('\t' + c_data_types[e.dataType] + ' ' \
                        + e.name + ';\n')
            else:
                outfile.write('\t' + nsprefix + e.dataType + ' ' + e.name + ';\n')
        outfile.write('} ' + nsprefix + s.name + ';\n')

    outfile.write('#ifdef __cplusplus\n')
    outfile.write('}\n')
    outfile.write('#endif\n')
    outfile.write('#endif\n')
