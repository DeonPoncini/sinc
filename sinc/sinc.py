#!/usr/bin/python

################################################################################
# sinc
# reads a data XML file and generates code in various languages
################################################################################

import sys

from xml.dom import minidom

from sinc_common import Package, Enumeration, Constant, Structure
from sinc_c import write_c
from sinc_cpp import write_cpp
from sinc_java import write_java
from sinc_python import write_python

if len(sys.argv) < 3:
    print "Usage is: " + sys.argv[0] + " <data.xml> <outpath> "
    sys.exit(1)

dataDom = minidom.parse(sys.argv[1])
outPath = sys.argv[2]

# get the output file name
datas = dataDom.getElementsByTagName('data')
if len(datas) > 1:
    print "Only one data element allowed"
    sys.exit(1)

fileName = datas[0].getAttribute('name')

# get the package declaration
packages = dataDom.getElementsByTagName('package')

if len(packages) > 1:
    print "Only one package element allowed"
    sys.exit(1)

uri = packages[0].getAttribute('uri')
namespace = packages[0].getElementsByTagName('namespace')
nslist = []
for n in namespace:
    nslist.append(n.childNodes[0].nodeValue)
packageObj = Package(uri, nslist)

# parse all the enums
enumObjs = []
enums = dataDom.getElementsByTagName('enum')
for e in enums:
    name = e.getAttribute('name')
    entries = e.getElementsByTagName('entry')
    entryList = []
    for e1 in entries:
        entryList.append(e1.childNodes[0].nodeValue)
    enumObjs.append(Enumeration(name,entryList))

# parse all the constants
constantObjs = []
constants = dataDom.getElementsByTagName('constant')
for c in constants:
    name = c.getAttribute('name')
    dataType = c.getAttribute('type')
    value = c.childNodes[0].nodeValue
    constantObjs.append(Constant(name, dataType, value))

# parse all the structs
structObjs = []
structs = dataDom.getElementsByTagName('struct')
for s in structs:
    sname = s.getAttribute('name')
    elements = s.getElementsByTagName('element')
    elementList = []
    for e in elements:
        name = e.childNodes[0].nodeValue
        dataType = e.getAttribute('type')
        elementList.append(Constant(name, dataType, 0))
    structObjs.append(Structure(sname, elementList))

write_cpp(packageObj, enumObjs, constantObjs, structObjs, outPath, fileName)
write_c(packageObj, enumObjs, constantObjs, structObjs, outPath, fileName)
write_java(packageObj, enumObjs, constantObjs, structObjs, outPath, fileName)
write_python(packageObj, enumObjs, constantObjs, structObjs, outPath, fileName)

