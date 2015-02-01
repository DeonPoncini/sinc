#!/usr/bin/python

################################################################################
# sinc-cpp
# generate C++ code
################################################################################

import codecs
import os.path

cpp_data_types = { \
        'string':'std::string', \
        'unsigned':'unsigned', \
        'int':'int', \
}

def write_cpp(packageObj, enumObjs, constantObjs, structObjs, \
        outPath, fileName):
    fullPath = os.path.join(outPath, 'cpp')
    if not os.path.exists(fullPath):
        os.makedirs(fullPath)
    outfile = codecs.open(os.path.join(fullPath, fileName + '.h'), 'w', 'utf-8')
    guard=""
    for n in packageObj.ns:
        guard = guard + n.upper() + '_'
    guard += fileName.upper() + '_H_CPP'
    outfile.write('#ifndef ' + guard + '\n')
    outfile.write('#define ' + guard + '\n')
    outfile.write('#include <string>\n')
    for n in packageObj.ns:
        outfile.write('namespace ' + n + ' {\n')

    # enumerations
    for e in enumObjs:
        outfile.write('enum class ' + e.name + ' {\n')
        for entry in e.entries:
            outfile.write('\t' + entry + ',\n')
        outfile.write('};\n')

    # constants
    for c in constantObjs:
        outfile.write('static const ' + cpp_data_types[c.dataType] + ' ' \
                + c.name + ' = ' + c.value + ';\n')

    # structs
    for s in structObjs:
        outfile.write('struct ' + s.name + ' {\n')
        for e in s.elements:
            if e.dataType in cpp_data_types:
                outfile.write('\t' + cpp_data_types[e.dataType] + ' ' \
                        + e.name + ';\n')
            else:
                outfile.write('\t' + e.dataType + ' ' + e.name + ';\n')
        outfile.write('};\n')

    for n in packageObj.ns:
        outfile.write('}\n')

    outfile.write('#endif\n')

