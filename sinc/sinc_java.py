#!/usr/bin/python

################################################################################
# sinc-java
# generate Java code
################################################################################

import codecs
import os.path

java_data_types = { \
        'string':'String', \
        'unsigned':'int', \
        'int':'int', \
}

def write_java(ast, outPath, fileName):
    paths = ast.package.uri.split(".")
    paths.reverse()
    for n in ast.package.ns:
        paths.append(n)

    fullPath = os.path.join(outPath,'java', *paths)
    if not os.path.exists(fullPath):
        os.makedirs(fullPath)
    outfile = codecs.open(os.path.join(fullPath, fileName + '.java'),
            'w', 'utf-8')

    packageName = ''
    for p in paths:
        packageName = packageName + p + '.'
    packageName = packageName[:-1]
    outfile.write('package ' + packageName + ';\n')

    # outer class
    outfile.write('public class ' + fileName + ' {\n')

    # enumerations
    for e in ast.enumerations:
        outfile.write('public enum ' + e.name + ' {\n')
        for entry in e.entries:
            outfile.write('\t' + entry + ',\n')
        outfile.write('}\n')

    # constants
    for c in ast.constants:
        outfile.write('public static final ' + java_data_types[c.dataType] + \
                ' ' + c.name + ' = ' + c.value + ';\n')

    # structs
    for s in ast.structures:
        outfile.write('public static class ' + s.name + '{\n')
        for e in s.elements:
            if e.dataType in java_data_types:
                outfile.write('\tpublic ' + java_data_types[e.dataType] + ' ' \
                        + e.name + ';\n')
            else:
                outfile.write('\tpublic ' + e.dataType + ' ' + e.name + ';\n')
        outfile.write('}\n')

    # close class
    outfile.write('}\n')

