#!/usr/bin/env python3

from xml.dom.minidom import parseString

from Airgun import Airgun

airgun = Airgun()
xml = airgun.get_xml_str()

print("Content-type: text/xml\n")
print(parseString(xml).toprettyxml())
