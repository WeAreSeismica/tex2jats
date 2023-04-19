 #!/usr/bin/env python
"""
    By Thea Ragon
    04/02/2022
"""

import sys
import re
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, "en_US.UTF-8") 


def tex2jats(texname):
    
    with open(texname+'.tex') as fi:
        tex = fi.read()
        
    strings = ["title",           
               "publisheddate",
               r"author\[ *([0-50]{1})((?: *, *[0-50]{1})*) *\]{ *(.*?) *(\n)",
               "orcid",
               "thanks",
               r"affil\[([0-50]{1})\]",
               "credit",
               "dois",
               "prodedname",
               "handedname",
               "copyedname",
               "reviewername",
               "translatorname"]
    
    meta = []
    for stri in strings:
        if 'author' in stri:
            pattern = re.compile(stri)
        elif 'credit' in stri:
            pattern = re.compile(stri+r'{(.*?)}'+r'{(.*?)}')
        elif 'thanks' in stri:
            pattern = re.compile(r'(author\[[\S\n\t\v ]*?\][\S\n\t\v ]*?)thanks{(.*?)}')
        elif 'reviewername' in stri or 'translatorname' in stri:
            pattern = re.compile(r'\n(.*?)'+stri+r'{(.*?)}')
        else:
            pattern = re.compile(stri+r'{(.*?)}')
        match0 = re.findall(pattern, tex)
        meta.append(match0)
    
    title = meta[0][0]
    doi = meta[7][0]
    pmid = ''
    publisherid = ''
    
    prod_editor_givenname = ' '.join(meta[8][0].split(' ')[:-1])
    prod_editor_surname = meta[8][0].split(' ')[-1]
    hand_editor_givenname = ' '.join(meta[9][0].split(' ')[:-1])
    hand_editor_surname = meta[9][0].split(' ')[-1]
    copyed_givenname = ' '.join(meta[10][0].split(' ')[:-1])
    copyed_surname = meta[10][0].split(' ')[-1]
    
    print(meta)
    print(meta[11][0][1])
    try:
        if '%' not in meta[11][0][0]:
            reviewers = meta[11][0][1].split('\\\\')
            reviewer_givenname = [reviewers[i].split(' ')[0] for i in range(len(reviewers))]
            reviewer_surname = [reviewers[i].split(' ')[-1] for i in range(len(reviewers))]
        else:
            reviewer_givenname = None
            reviewer_surname = None
    except:
        reviewer_givenname = None
        reviewer_surname = None
    try:
        if '%' not in meta[12][0][0]:
            translators = meta[12][0][1].split('\\\\')
            translator_givenname = [translators[i].split(' ')[0] for i in range(len(translators))]
            translator_surname = [translators[i].split(' ')[-1] for i in range(len(translators))]
        else:
            translator_givenname = None
            translator_surname = None
    except:
        translator_givenname = None
        translator_surname = None
    
    formats = ["%B %d, %Y", "%B %d %Y", "%d %B %Y", "%b %d %Y", "%m/%d/%Y", "%m %d %Y"]
    dd = meta[1][0]
    date, year = None, None
    for format in formats:
        try:
            date = datetime.strptime(dd, format).strftime("%Y-%m-%d")
            day = datetime.strptime(dd, format).strftime("%d")
            month = datetime.strptime(dd, format).strftime("%m")
            year = datetime.strptime(dd, format).strftime("%Y")
        except ValueError:
            pass
    author = [meta[2][i][-2] for i in range(len(meta[2]))]
    surname = [name.split(' ')[-1] for name in author]
    givenname = [name.split(' ')[0:-1] for name in author]
    givenname = [' '.join(givenname[i]) for i in range(len(givenname))]
    orcid = meta[3]
    
    ## AFFILIATIONS
    ## note: the OJS JATS reader is not working well, the only thing it reads is the role. 
    ## Hence all affiliations are parsed as a role, but it's bad JATS
    ## there are two other solutions below that are commented
    
    ## sol1,  get text affils, not needed anymore but keep it just in case
    # firstaffil = []
    # for i in [meta[2][j][0] for j in range(len(meta[2]))]:
    #     for k in range(len(meta[5])):
    #         if meta[5][k][0] == i:
    #             firstaffil.append(meta[5][k][1])
    
    # otheraffil = []
    # for affs in [meta[2][j][1] for j in range(len(meta[2]))]:
    #     affs = affs.replace(' ','').split(',')
    #     otheraff = []
    #     for i in affs:
    #         if len(i) > 0:
    #             for k in range(len(meta[5])):
    #                 if meta[5][k][0] == i:
    #                     otheraff.append(meta[5][k][1])    
    #     otheraffil.append(otheraff)
    
    # # sol2, get affil numbers, not working with OJS
    # affil = []
    # for i in range(len(meta[2])):
    #     affs = []
    #     affs.append(meta[2][i][0])
    #     otheraff = meta[2][i][1].replace(' ','').split(',')
    #     for j in otheraff:
    #         if len(j) > 0:
    #             affs.append(j)
    #     affil.append(affs)
        
    # affil_id = [' '.join(affil[i]) for i in range(len(affil))]
    # affil_sup = [','.join(affil[i]) for i in range(len(affil))]
    
    # affil_address = meta[5]
    
    # sol3, get affil as roles
    firstaffil = []
    for i in [meta[2][j][0] for j in range(len(meta[2]))]:
        for k in range(len(meta[5])):
            if meta[5][k][0] == i:
                firstaffil.append(meta[5][k][1])
    
    otheraffil = []
    for affs in [meta[2][j][1] for j in range(len(meta[2]))]:
        affs = affs.replace(' ','').split(',')
        otheraff = []
        for i in affs:
            if len(i) > 0:
                for k in range(len(meta[5])):
                    if meta[5][k][0] == i:
                        otheraff.append(meta[5][k][1])    
        otheraffil.append(otheraff)
    otheraffil = [', '.join(otheraffil[i]) for i in range(len(otheraffil))]
        
    # get corresponding author
    corres = meta[4][0][1]
    corres_id = len(re.findall('author', meta[4][0][0]))
    
    outname = texname+'_metadata.jats'
    with open(outname, 'w') as fi:
        fi.write('''<front>
<journal-meta>
<journal-id></journal-id>
<journal-title-group>
<journal-title>Seismica</journal-title>
</journal-title-group>
<issn>2816-9387</issn>
<publisher>
<publisher-name></publisher-name>
</publisher>
</journal-meta>
<article-meta>
''')
        fi.write('''<title-group>
<article-title>{}</article-title>
</title-group>'''.format(title))
        if date is not None:
            fi.write('''<pub-date publication-format="print" date-type="pub" iso-8601-date="{}">
                <day>{}</day><month>{}</month><year>{}</year>
                </pub-date>
                '''.format(date, day, month, year))
        fi.write('<article-id pub-id-type="publisher-id">{}</article-id>\n'.format(publisherid))
        fi.write('<article-id pub-id-type="doi">{}</article-id>\n'.format(doi))
        fi.write('<article-id pub-id-type="pmid">{}</article-id>\n'.format(pmid))
        if year is not None:
            fi.write('''<permissions>                
                <copyright-statement>Copyright &#169; {}, {} et al.  
                This is an Open Access article distributed under the terms of the Creative Commons Attribution 4.0 International License, allowing third parties to copy and redistribute the material in any medium or format and to remix, transform, and build upon the material for any purpose, even commercially, provided the original work is properly cited and states its license.
                </copyright-statement>
                </permissions>'''.format(year, author[0]))
        
        fi.write('<contrib-group>\n')
        
        ## SOL 2 for afiliations, not working with OJS
#         for i in range(len(author)):
#             if i == corres_id-1:
#                 fi.write('''<contrib contrib-type="author">
# <contrib-id contrib-id-type="orcid">{}</contrib-id>
# <name name-style="western">
# <surname>{}</surname>
# <given-names>{}</given-names>
# </name>
# <xref ref-type="aff" rid="{}"><sup>{}</sup></xref>
# <email>{}</email>
# </contrib>
# '''.format(orcid[i], surname[i], givenname[i], affil_id[i], affil_sup[i], corres.split(' ')[-1]))
#             else:
#                 fi.write('''<contrib contrib-type="author">
# <contrib-id contrib-id-type="orcid">{}</contrib-id>
# <name name-style="western">
# <surname>{}</surname>
# <given-names>{}</given-names>
# </name>
# <xref ref-type="aff" rid="{}"><sup>{}</sup></xref>
# </contrib>
# '''.format(orcid[i], surname[i], givenname[i], affil_id[i], affil_sup[i]))

#         for i in range(len(affil_address)):
#             fi.write('''<aff id="{}"><label>{}</label>{} </aff>
# '''.format(affil_address[i][0], affil_address[i][0], affil_address[i][1]))
        
        ## SOL 3 for affiliations, all parsed to ROLES, working OK with OJS
        for i in range(len(author)):
            if i == corres_id-1:
                fi.write('''<contrib contrib-type="author">
<contrib-id contrib-id-type="orcid">{}</contrib-id>
<name name-style="western">
<surname>{}</surname>
<given-names>{}</given-names>
</name>
<role> {}Correspondence to: <email>{}</email>
</role>
</contrib>
'''.format(orcid[i], surname[i], givenname[i], firstaffil[i]+', '+otheraffil[i], corres.split(' ')[-1]))
            else:
                fi.write('''<contrib contrib-type="author">
<contrib-id contrib-id-type="orcid">{}</contrib-id>
<name name-style="western">
<surname>{}</surname>
<given-names>{}</given-names>
</name>
<role> {}
</role>
</contrib>
'''.format(orcid[i], surname[i], givenname[i],firstaffil[i]+', '+otheraffil[i]))

        ## Editors        
        fi.write('''<contrib contrib-type="editor">
<name name-style="western">
<surname>{}</surname>
<given-names>{}</given-names>
</name>
<role>Handling Editor</role>
</contrib>
'''.format(hand_editor_surname,hand_editor_givenname))

        fi.write('''<contrib contrib-type="editor">
<name name-style="western">
<surname>{}</surname>
<given-names>{}</given-names>
</name>
<role>Production Editor</role>
</contrib>
'''.format(prod_editor_surname,prod_editor_givenname))
    
        fi.write('''<contrib contrib-type="editor">
<name name-style="western">
<surname>{}</surname>
<given-names>{}</given-names>
</name>
<role>Copy-Editing, Typesetting, Layout Editing</role>
</contrib>
'''.format(copyed_surname,copyed_givenname))
        
        if reviewer_givenname:
            for i in range(len(reviewer_givenname)):
                fi.write('''<contrib contrib-type="reviewer">
<name name-style="western">
<surname>{}</surname>
<given-names>{}</given-names>
</name>
<role>Reviewer</role>
</contrib>
'''.format(reviewer_surname[i],reviewer_givenname[i]))
                
        if translator_givenname:
            for i in range(len(translator_givenname)):
                fi.write('''<contrib contrib-type="translator">
<name name-style="western">
<surname>{}</surname>
<given-names>{}</given-names>
</name>
<role>Abstract translation</role>
</contrib>
'''.format(translator_surname[i],translator_givenname[i]))

    
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
    
    table_list = re.findall(r'(?s).begin{table\*?}(.*?)end{table\*?}', tex)
    pat = [r'\\label', r'\\caption']
    for i in range(len(table_list)):
        table = table_list[i]
        tab_meta=[]
        for stri in pat:
            pattern = re.compile(stri+r'{(.*?)}')
            match = re.findall(pattern, table)
            tab_meta.append(match)
        try:
            label = codepoints(tab_meta[0][0])
            caption = tab_meta[1][0]
        except:
            print('Table #{} does not have a label!'.format(i+1))
            print('label assigned: tab{}'.format(i+1))
            label = 'tab'+str(i+1)
            caption = ""
        # match main tex
        textab = re.findall(r'(?s).begin{(?:tabular|seistable)}(.*?)end{(?:tabular|seistable)}', table)
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
<!-- !!! without the potentials "table" tags (<table> and <\table>) -->
</tbody>
</table>
</table-wrap>
    '''.format(label, caption, 'tab'+str(i+1)+'.tex'))
    
        tabname = texname+'_tab'+str(i+1)+'.tex'
                # correct for textbf, not perfect....
        regex = r"\\textbf\{(([^{}]*(\{(([^{}]*(\{[^{}]*\}[^{}]*)?)*)\}[^{}]*)?)*)\}"
        subst = "\\1"
        result = re.sub(regex, subst, main, 0, re.MULTILINE)
        regex = r"[ ]{1,}|[\t]{1,}|[ \t]{1,}"
        subst = " "
        result = re.sub(regex, subst, result, 0, re.MULTILINE)
        with open(tabname, 'w') as fi:
            fi.write('{}'.format(result))

if __name__ == '__main__':
    
    tex2jats(sys.argv[1])
    

