import biblib.bib as bbl
import numpy as np
import sys

def sort_refs(bibfile,ofile):
    parser = bbl.Parser()
    parsed = parser.parse(open(bibfile,'r'))
    unsorted = parsed.get_entries()

    bibkeys = np.array([k for k in unsorted.keys()])
    surnames = []
    for key in bibkeys:
        entry = unsorted[key]
        firstauth = entry['author'].split('and')[0]
        if ',' in firstauth:
            surnames.append(firstauth.split(',')[0])
        elif firstauth.startswith('{') and firstauth.endswith('}'):
            toadd = firstauth.split(' ')[0].lstrip('{')
            if toadd.lower() == 'the':
                toadd = firstauth.split(' ')[1].rstrip('}')
            surnames.append(toadd)
        else:
            surnames.append(firstauth.split(' ')[-1])

    keyorder = bibkeys[np.argsort(surnames)]

    with open(ofile,'w') as f:
        for k in keyorder:
            f.write(unsorted[k].to_bib())
            f.write('\n')

if __name__ == '__main__':
    bibfile = sys.argv[1] + '.bib'
    ofile = sys.argv[1] + '_sort.bib'

    sort_refs(bibfile,ofile)
