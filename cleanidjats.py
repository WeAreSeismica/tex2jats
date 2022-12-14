 #!/usr/bin/env python
"""
    By Thea Ragon
    04/02/2022
"""

import sys
import re

def cleanid(xmlname):
        
    special_characs = "\"#$%&*+/:;<=>?@[\]^`{|}~"
    special_characs2 = ["<",">","&"]
    xml_code2=['&#60;','&#62;','&#38;']
    
    def codepoints(stri):
        out = ''
        for c in stri: 
            if c in special_characs:
                out = out+'{:04X}'.format( ord(c) )
            else:
                out = out+c
        return out
    
    def func(matchobj):
        m =  matchobj.group(1)
        out = 'id="'+codepoints(m)+'"'
        return out
    
    with open(xmlname+'.xml', 'r') as fi:
        xml = fi.read()
    
    xml_new = re.sub('id=\"(.*?)\"', func, xml, flags = re.M)
        
    with open(xmlname+'.xml', 'w') as fi:
        xml = fi.write(xml_new)
        
    ## clean special characters
    with open(xmlname+'.xml', 'r') as fi:
        xml_new = fi.read()
    
    for i,c in enumerate(special_characs2):
        try:
            xml_new = re.sub(r' \{} '.format(c), ' {} '.format(xml_code2[i]), xml_new, flags = re.M)
            xml_new = re.sub(r' {} '.format(c), ' {} '.format(xml_code2[i]), xml_new, flags = re.M)
        except:
            pass
        
    with open(xmlname+'.xml', 'w') as fi:
        xml = fi.write(xml_new)
        
if __name__ == '__main__':
    
    cleanid(sys.argv[1])
    

