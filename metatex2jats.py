 #!/usr/bin/env python
"""
    By Thea Ragon
    04/02/2022
"""

import sys
import re
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, "en_US") 


def tex2jats(texname):
    
    with open(texname+'.tex') as fi:
        tex = fi.read()
        
    strings = ["title",           
               "publisheddate",
               "author\[([0-50]{1})\]",
               "orcid",
               "thanks",
               "affil\[([0-50]{1})\]",
               "credit",
               "doi",
               "editorname",
               "copyedname",
               "typesetname",
               "prodname"]
    
    meta = []
    for stri in strings:
        pattern = re.compile(stri+r'{(.*?)}')
        if 'author' in stri:
            pattern = re.compile(stri+r'{(.*?)(\n)')
        if 'credit' in stri:
            pattern = re.compile(stri+r'{(.*?)}'+r'{(.*?)}')
        match = re.findall(pattern, tex)
        meta.append(match)
    
    title = meta[0][0]
    doi = meta[7][0]
    pmid = ''
    publisherid = ''
    
    editor_givenname = meta[8][0].split(' ')[0]
    editor_surname = meta[8][0].split(' ')[1]
    copyed_givenname = meta[9][0].split(' ')[0]
    copyed_surname = meta[9][0].split(' ')[1]
    
    formats = ["%B %d, %Y", "%B %d %Y", "%d %B %Y", "%b %d %Y", "%m/%d/%Y", "%m %d %Y"]
    dd = meta[1][0]
    for format in formats:
        try:
            date = datetime.strptime(dd, format).strftime("%Y-%m-%d")
            day = datetime.strptime(dd, format).strftime("%d")
            month = datetime.strptime(dd, format).strftime("%m")
            year = datetime.strptime(dd, format).strftime("%Y")
        except ValueError:
            pass
    author = [meta[2][i][1] for i in range(len(meta[2]))]
    surname = [name.split(' ')[1] for name in author]
    givenname = [name.split(' ')[0] for name in author]
    orcid = meta[3]
    
    affil = []
    for i in [meta[2][j][0] for j in range(len(meta[2]))]:
        for k in range(len(meta[5])):
            if meta[5][k][0] == i:
                affil.append(meta[5][k][1])
    
    corres = meta[4]
    
    outname = texname+'_metadata.jats'
    with open(outname, 'w') as fi:
        fi.write('''<front>
<journal-meta>
<journal-id></journal-id>
<journal-title-group>
<journal-title>Seismica</journal-title>
</journal-title-group>
<issn></issn>
<publisher>
<publisher-name></publisher-name>
</publisher>
</journal-meta>
<article-meta>
''')
        fi.write('''<title-group>
<article-title>{}</article-title>
</title-group>'''.format(title))
        fi.write('''<pub-date publication-format="print" date-type="pub" iso-8601-date="{}">
<day>{}</day><month>{}</month><year>{}</year>
</pub-date>
'''.format(date, day, month, year))
        fi.write('<article-id pub-id-type="publisher-id">{}</article-id>\n'.format(publisherid))
        fi.write('<article-id pub-id-type="doi">{}</article-id>\n'.format(doi))
        fi.write('<article-id pub-id-type="pmid">{}</article-id>\n'.format(pmid))
        
        fi.write('<contrib-group>\n')
        for i in range(len(author)):
            if i == 0:
                fi.write('''<contrib contrib-type="author">
<contrib-id contrib-id-type="orcid">{}</contrib-id>
<name name-style="western">
<surname>{}</surname>
<given-names>{}</given-names>
</name>
<aff>{}</aff>
<email>{}</email>
</contrib>
'''.format(orcid[i], surname[i], givenname[i], affil[i], corres[0].split(' ')[-1]))
            else:
                fi.write('''<contrib contrib-type="author">
<contrib-id contrib-id-type="orcid">{}</contrib-id>
<name name-style="western">
<surname>{}</surname>
<given-names>{}</given-names>
</name>
<aff>{}</aff>
</contrib>
'''.format(orcid[i], surname[i], givenname[i], affil[i]))
        
        fi.write('''<contrib contrib-type="editor">
<name name-style="western">
<surname>{}</surname>
<given-names>{}</given-names>
</name>
<role>Editor</role>
</contrib>
'''.format(editor_surname,editor_givenname))
    
        fi.write('''<contrib contrib-type="editor">
<name name-style="western">
<surname>{}</surname>
<given-names>{}</given-names>
</name>
<role>Copy-Editing, Typesetting</role>
</contrib>
'''.format(copyed_surname,copyed_givenname))
    
        fi.write('''</contrib-group>
</article-meta>
</front>
''')
    
    ## extract credits
    credit = ''
    for i in range(len(meta[6])):
        credit = credit+meta[6][i][0]+': '+meta[6][i][1]+'. '
        
    credname = texname+'_credits.jats'
    with open(credname, 'w') as fi:
        fi.write('''<sec id="author-contributions">
<title>Author contributions</title>
<p>{}</p>
</sec>
'''.format(credit))

    ## extract table
    special_characs = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    def codepoints(stri):
        out = ''
        for c in stri:
            if c in special_characs:
                out = out+'{:04X}'.format( ord(c) )
            else:
                out = out+c
        return out
    
    table_list = re.findall(r'(?s).begin{table}(.*?)end{table}', tex)
    pat = [r'\\label', r'\\caption']
    for i in range(len(table_list)):
        table = table_list[i]
        tab_meta=[]
        for stri in pat:
            pattern = re.compile(stri+r'{(.*?)}')
            match = re.findall(pattern, table)
            tab_meta.append(match)
        label = codepoints(tab_meta[0][0])
        caption = tab_meta[1][0]
        # match main tex
        textab = re.findall(r'(?s).begin{tabular}(.*?)end{tabular}', table)
        main = textab[0]
        # write to file
        tabname = texname+'_tab'+str(i+1)+'.xml'
        with open(tabname, 'w') as fi:
            fi.write('''<table-wrap id="{}">
<caption>
<p>{}</p>
</caption>
<table frame="box" rules="all" cellpadding="5">
<tbody>
<!--INCLUDE HTML TABLE HERE TRANSLATED FROM {} FILE TO HTML -->
<!-- !!! without the potentials "table" tags -->
</tbody>
</table>
</table-wrap>
    '''.format(label, caption, 'tab'+str(i+1)+'.tex'))
    
        tabname = texname+'_tab'+str(i+1)+'.tex'
        with open(tabname, 'w') as fi:
            fi.write('{}'.format(main))

if __name__ == '__main__':
    
    tex2jats(sys.argv[1])
    

