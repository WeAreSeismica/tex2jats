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
from bs4 import BeautifulSoup, CData, NavigableString
from pathlib import Path


def sepbib(texname):
    xmlname = texname
    

    outname = 'bib.xml'
    with open(outname, "w", encoding='utf-8') as fout:
        fout.write('<back>\n')
        with open(xmlname+'.xml') as fi:
            for line in iter(fi.readline, '<back>\n'):
                pass
            for line in iter(fi.readline, '</back>\n'):
                fout.write(str(line))
        fout.write('</back>\n')
        
    return
        
        
def metatex2jats(texname):
    
    with open(texname+'.tex') as fi:
        tex = fi.read()
        
    strings = ["title",           
               "publisheddate",
               r"author\[ *([\d]{1,2})((?: *, *[\d]{1,2})*) *\]{ *(.*?) *(\n)",
               "orcid",
               "thanks",
               r"affil\[([\d]{1,2})\]",
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
            pattern = re.compile(r'(.*?)'+stri+r'{(.*?)}')
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
    
    try:
        if '%' not in meta[11][0][0]:
            revs = re.split(r'\\|and|,', meta[11][0][1])
            reviewers = [x for x in revs if x]
            reviewer_givenname = []
            reviewer_surname = []
            for rev in reviewers:
                nospace = [ x for x in rev.split(' ') if x]
                reviewer_givenname.append(nospace[0])
                reviewer_surname.append(nospace[1])
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
    
    surname = []
    givenname = []
    for auth in author:
        names = re.split(r' |~|}', auth)
        names = [x for x in names if x]
        surname.append(names[-1])
        givenname.append( ' '.join(names[0:-1]) )
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
    try:
        corres = meta[4][0][1]
        corres_id = len(re.findall('author', meta[4][0][0]))
    except:
        print('\nNo corresponding author found!')
        corres_id = 0
    
    outname = texname+'_metadata.xml'
    with open(outname, "w", encoding='utf-8') as fi:
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
        if len(orcid) == len(surname):
            for i in range(len(author)):
                if i == corres_id-1:
                    fi.write('''<contrib contrib-type="author">
    <contrib-id contrib-id-type="orcid">{}</contrib-id>
    <name name-style="western">
    <surname>{}</surname>
    <given-names>{}</given-names>
    </name>
    <role> {}. Correspondence to: <email>{}</email>
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
        else:
            print('\nOrcid macro for all authors not provided -> empty ORCIDs.')
            for i in range(len(author)):
                if i == corres_id-1:
                    fi.write('''<contrib contrib-type="author">
    <contrib-id contrib-id-type="orcid">{}</contrib-id>
    <name name-style="western">
    <surname>{}</surname>
    <given-names>{}</given-names>
    </name>
    <role> {}. Correspondence to: <email>{}</email>
    </role>
    </contrib>
    '''.format('', surname[i], givenname[i], firstaffil[i]+', '+otheraffil[i], corres.split(' ')[-1]))
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
    '''.format('', surname[i], givenname[i],firstaffil[i]+', '+otheraffil[i]))
                    
                    
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
        
    credname = texname+'_credits.xml'
    with open(credname, "w", encoding='utf-8') as fi:
        fi.write('''<sec id="author-contributions">
<title>Author contributions</title>
<p>{}</p>
</sec>
'''.format(credit))
    
    return outname, credname

def cleanid(xmlname):
        
    special_characs = "\"#$%&*+/;<=>?@[\]^`{|}~"
    special_characs2 = ["<",">","&"]
    xml_code2=['&#60;','&#62;','&#38;']
    
    def codepoints(stri):
        out = ''
        for c in stri: 
            if c in special_characs:
                out = out+'{:04X}'.format( ord(c) )
            elif c ==':':
                out = out+'U003A'
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
        
    with open(xmlname+'.xml', "w", encoding='utf-8') as fi:
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
        
    with open(xmlname+'.xml', "w", encoding='utf-8') as fi:
        xml = fi.write(xml_new)
        
    return

def cleanxrefjats(xmlname):
        
    with open(xmlname+'.xml') as fi:
        xml = fi.read()
      
    soup = BeautifulSoup(xml, 'html.parser')
    
    # get figures labels (id)
    labels = []
    for index, p in enumerate(soup.find_all('fig')):
       labels.append( p['id'] )
    
    # correct xrefs for figures labels (id)
    ## Check for xref ids for xref whose ref-type is correct
    for p in soup.find_all("xref", attrs={"ref-type": "fig"}):
        alt = labels.index(p['rid']) +1
        p['alt'] = str(alt)
        p.string.replace_with(str(alt))
        
    ## Check for xref ids for xref whose ref-type is incorrect
    for rid in labels:
        for p in soup.find_all("xref", attrs={"rid": rid}):
            alt = labels.index(p['rid']) +1
            p['alt'] = str(alt)
            p["ref-type"]= "fig"
            p.string.replace_with(str(alt))        
                
    # correct graphic for png extension
    for p in soup.find_all('graphic'):
        p["mime-subtype"] = "png"
        p["mimetype"]="image"
        href = p["xlink:href"]
        uphref = href.rsplit( ".", 1 )[0]+'.png'
        p["xlink:href"] = uphref
        
    ## output to XML file
    with open(xmlname+'.xml', "w", encoding='utf-8') as fi:
        fi.write(str(soup))
    
    return

def table2jats(texname):
    xmlname = texname
    
    with open(texname+'.tex') as fi:
        tex = fi.read()
        
    with open(xmlname+'.xml') as fi:
        xml = fi.read()
      
    ### in TeX file
    ## extract table 
    special_characs = "\"#$%&*+/;<=>?@[\]^`{|}~"
    def codepoints(stri):
        out = ''
        for c in stri: 
            if c in special_characs:
                out = out+'{:04X}'.format( ord(c) )
            elif c ==':':
                out = out+'U003A'
            else:
                out = out+c
        return out
    
    table_list = re.findall(r'(?s).begin{table\*?}(.*?)end{table\*?}', tex)

    pat = [r'\\label{(.*?)}', r'(?s)\\caption\{(.*?)\\label', r'((?<=caption\{).*$)']
    labels = []
    captions = []
    for i in range(len(table_list)):
        table = table_list[i]
        
        # label
        pattern = re.compile(pat[0])
        match = re.findall(pattern, table)
        if len(match) > 0:
            label = codepoints(match[0])
        else:
            print('Table #{} does not have a label!'.format(i+1))
            print('label assigned: tab{}'.format(i+1))
            label = 'tab'+str(i+1)   
        labels.append(label)
        
        # caption
        pattern = re.compile(pat[1])
        match = re.findall(pattern, table)
        if len(match) > 0:
            caption = match[0].rsplit('}',1)[0].replace('\n','')
        else:
            pattern = re.compile(pat[2])
            match = re.findall(pattern, table)
            if len(match) > 0:
                caption = match[0].rsplit('}',1)[0].replace('\n','')
            else:
                print('Table #{} does not have a caption!'.format(i+1))
                caption = ''
        captions.append(caption)
            
        # match main tex
        textab = re.findall(r'(?s).begin{(?:tabular|seistable)}(.*?)end{(?:tabular|seistable)}', table)
        main = textab[0]
        
    ### correct references in caption
    #for cap in captions:
        #cap = re.sub(r' \{} '.format(c), ' {} '.format(xml_code2[i]), xml_new, flags = re.M)
    
    
    ## in XML file
    table_list_xml = re.findall(r'(<table-wrap>)', xml)
        
    # check same length as TeX table list
    if len(table_list_xml) != len(table_list):
        table_list_xml = re.findall(r'(<table-wrap id=)', xml)
        
        if len(table_list_xml) != len(table_list):
           print('Error: the number of tables in the TeX and XML files is different')

    # replace metadata in XML file
    soup = BeautifulSoup(xml, 'html.parser')
    
    boxed_txt = [x for x in soup.find_all("boxed-text") if x.find('table-wrap')]
    for p in boxed_txt:
        p.replaceWithChildren()
        
    for index, p in enumerate(soup.find_all('table-wrap')):
        p['id'] = labels[index]
        
        captagg = p.find('caption')
        if not captagg:
            captag = soup.new_tag("caption")
            pp = soup.new_tag("p")
            captag.append(pp)
            p.append(captag)
            pp.string = captions[index]
        
    for index, p in enumerate(soup.find_all('table'), start=1):
        p['frame'] = "box"
        p['rules'] = "all"
        p['cellpadding'] = "5"
    
    ## Check for xref ids for xref whose ref-type is correct
    for p in soup.find_all("xref", attrs={"ref-type": "table"}):
        alt = labels.index(p['rid']) +1
        p['alt'] = str(alt)
        p.string.replace_with(str(alt))
        
    ## Check for xref ids for xref whose ref-type is incorrect
    for rid in labels:
        for p in soup.find_all("xref", attrs={"rid": rid}):
            alt = labels.index(p['rid']) +1
            p['alt'] = str(alt)
            p["ref-type"]= "table"
            p.string.replace_with(str(alt))        
                
    ## output to XML file
    with open(xmlname+'.xml', "w", encoding='utf-8') as fi:
        fi.write(str(soup))

    ## Output to separate files for use when table is too complex
    Path("tables").mkdir(parents=True, exist_ok=True)

    for i in range(len(table_list)):
        # write to file
        tabname = 'tables/' + texname+'_tab'+str(i+1)+'.xml'
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
    '''.format(labels[i], captions[i], 'tab'+str(i+1)+'.tex'))
    
        tabname = 'tables/'+texname+'_tab'+str(i+1)+'.tex'
        # correct for textbf, not perfect....
        regex = r"\\textbf\{(([^{}]*(\{(([^{}]*(\{[^{}]*\}[^{}]*)?)*)\}[^{}]*)?)*)\}"
        subst = "\\1"
        result = re.sub(regex, subst, main, 0, re.MULTILINE)
        regex = r"[ ]{1,}|[\t]{1,}|[ \t]{1,}"
        subst = " "
        result = re.sub(regex, subst, result, 0, re.MULTILINE)
        with open(tabname, 'w') as fi:
            fi.write('{}'.format(result))
            
    return
    
def cleanmathjats(xmlname):
        
    with open(xmlname+'.xml') as fi:
        xml = fi.read()
      
    soup = BeautifulSoup(xml, 'html.parser')
    
    # correct for inline formulas
    for p in soup.find_all("inline-formula"):
        newtag = p.find('alternatives').find('tex-math')
        p.append( newtag )
        p.alternatives.decompose()
        
    # correct for formulas
    label_number = 1
    ids = []
    for p in soup.find_all("disp-formula"):
        newtag = p.find('alternatives').find('tex-math')
        
        if 'label' in str(newtag):
            regex = r"(\\label\{(\S*?)\})"
            label = re.findall(regex, str(newtag) )[0][1]
            p["id"] = label
            ids.append(label)
            
            labeltag = soup.new_tag("label")
            p.append(labeltag)
            sc = soup.new_tag("sub")
            labeltag.append(sc)
            sc.string = "Equation ("+str(label_number)+")"
            label_number += 1
            
            p.append( newtag )        
            p.alternatives.decompose()
        else:
            p.append( newtag )
            p.alternatives.decompose()
    
    # correct Xrefs
    for rid in ids:
        for p in soup.find_all("xref", attrs={"rid": rid}):
            alt = ids.index(p['rid']) +1
            p['alt'] = str(alt)
            p["ref-type"]= "disp-formula"
            p.string.replace_with(str(alt))   
    
    ## output to XML file
    with open(xmlname+'.xml', "w", encoding='utf-8') as fi:
        fi.write(str(soup))
        
    # remove label from CDATA
    with open(xmlname+'.xml', 'r') as fi:
        xml = fi.read()
        
    regex = r"\<tex-math>[\S\n\t\v ]{,20}\<!\[CDATA\[([\S\n\t\v ]{,200})\\label\{([\S]*?)\}[\S\n\t\v ]{,20}\]\]\>[\S\n\t\v ]{,20}\<\/tex-math>"
    xml_new = re.sub(regex, r"<tex-math><![CDATA[\1]]></tex-math>", xml)
    
    with open(xmlname+'.xml', "w", encoding='utf-8') as fi:
        xml = fi.write(xml_new)
    
    return


def cleanbibentries(bibname, xmlname):
        
    with open(bibname+'.xml') as fi:
        xml = fi.read()
      
    soup = BeautifulSoup(xml, 'xml')
    
    for p in soup.find_all('ref'):
        src = p.find('source')
    
    for p in soup.find_all('element-citation', attrs={'publication-type':"article-journal"}):
        if p.find("pub-id") is None:
            uri = p.find('uri')
            source = p.find('source')
            if uri is not None and source is not None:
                source.insert(1, NavigableString(". Available from: "+uri.text+" Year") )
            elif uri is not None and source is None:
                newtag = soup.new_tag("source")
                #newtag.append(uri)
                p.append(newtag)
                newtag.insert(1, NavigableString("Available from: "+uri.text+" Year") )
            elif uri is None and source is not None:
                pass
            else:
                print('\n There might be information missing for this bibliography entry:')
                print(p)
        
    for p in soup.find_all('element-citation', attrs={'publication-type':None}):
        p['publication-type'] = "article-journal"
        #p['publication-format'] = "web"
        
        uri = p.find('uri')
        doi = p.find('pub-id')
        source = p.find('source')
        
        if source is None:
            if uri is not None and doi is None:  
                newtag = soup.new_tag("source")
                #newtag.append(uri)
                p.append(newtag)
                newtag.insert(0, NavigableString("Available from: "+uri.text+" Year"))   
                
                #newtag = soup.new_tag("pub-id")
                #newtag["pub-id-type"]="url"
                #p.append(newtag)
                #newtag.insert(0, NavigableString(uri.text) )  
                
            elif uri is None and doi is None:
                print('There might be information missing for this bibliography entry:')
                print(p)
        else:
            if uri is not None:
                source.insert(1, NavigableString(". Available from: "+uri.text+" Year") )
    
    ## output to XML file
    with open(bibname+'.xml', "w", encoding='utf-8') as fi:
        fi.write(str(soup))
        
    return

if __name__ == '__main__':
    
    texname = sys.argv[1]
    
    # extract references for separate cleaning (requires different XML parser)
    #sed -n '/\<back\>/,/\<\/back\>/p' $1.xml > bib.xml
    sepbib(texname)
    
    # extract tex metadata to jats metadata
    # output texname_metadata.jats
    # extract list of references because BeautifulSoup messes up with it
    metatex2jats(texname)
    
    # clean ids from characters that do not print correctly
    cleanid(texname)
    
    # cleans xrefs and figures extension
    cleanxrefjats(texname)

    # include tables in XML file, clean xrefs
    table2jats(texname)
    
    # clean formulas
    cleanmathjats(texname)
    
    # clean misc bib entries + include list of refs
    cleanbibentries('bib', texname)
    
