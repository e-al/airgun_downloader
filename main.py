#!/usr/bin/env python3
__author__ = 'last5bits'

from xml.dom.minidom import parseString

from Airgun import Airgun

airgun = Airgun()
xml = airgun.get_xml_str()

print("Content-type: text/xml\n")
print(parseString(xml).toprettyxml())

with open("test.xml", "w") as f:
    f.write("Content-type: text/xml\n")
    f.write(parseString(xml).toprettyxml())
    f.close()
