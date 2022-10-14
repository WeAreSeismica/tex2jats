 #!/usr/bin/env python
"""
    By Thea Ragon
    04/02/2022
"""

import sys
import re

def cleanxref(xmlname):
       
    def fig_sub(match):
        if 'ref-type' in match.group(3):
            return match
        else:
            sub = r'{}{}<xref ref-type="fig" alt{}'.format(match.group(1), match.group(2), match.group(3))
            return sub
    
    def tab_sub(match):
        if 'ref-type' in match.group(3):
            return match
        else:
            sub = r'{}{}<xref ref-type="table" alt{}'.format(match.group(1), match.group(2), match.group(3))
            return sub
    
    with open(xmlname+'.xml', 'r') as fi:
        xml = fi.read()
    
    xml_new = xml
    for i in range(20):
        # for figures
        regex = r"((?:<xref ref-type=\"fig\".{10,50}<\/xref>){1})([\S\d\n\t ]{1,5})<xref alt(.{10,50}<\/xref>)"
        xml_new = re.sub(regex, fig_sub, xml_new, flags = re.IGNORECASE)
    
        # for figures
        regex = r"((?:<xref ref-type=\"table\".{10,50}<\/xref>){1})([\S\d\n\t ]{1,5})<xref alt(.{10,50}<\/xref>)"
        xml_new = re.sub(regex, tab_sub, xml_new, flags = re.IGNORECASE)

    with open(xmlname+'.xml', 'w') as fi:
        xml = fi.write(xml_new)
        
if __name__ == '__main__':
    
    cleanxref(sys.argv[1])
    

