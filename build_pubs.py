# -*- coding: utf-8 -*-
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

# the bib file is generated automatically by Zotero
with open('publications/publications.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

writer = BibTexWriter()
with open('ignore/publications.md', 'w') as md_file:

    md_file.write('### Publications\n\n') # Write title

    for bib_item in bib_database.entries:
        if not 'Schlechtweg' in bib_item['author']:
            continue

        # Replace special signs
        mapping = {'\\"{a}':'ä','\n':' '}
        for item in bib_item:
            for symbol in mapping:
                #print(bib_item[item])            
                bib_item[item] = bib_item[item].replace(symbol, mapping[symbol])
        
        if 'booktitle' in bib_item:
            venue = u', {}'.format(bib_item['booktitle']).replace('{','').replace('}','').strip(',')
        elif bib_item['journal']:
            venue = u', {}'.format(bib_item['journal']).strip(',')
        else:
            venue = u''

        # Modify pages    
        if 'pages' in bib_item:
            pages = u', {}'.format(bib_item['pages'])
        else:
            pages = u''
        pages = pages.replace('--','-') 

        if 'file' in bib_item:
            pdf_link = u' [[pdf]]({})'.format(bib_item['file'])
        else:
            pdf_link = u''

        # Modify author
        authors = bib_item['author'].split(' and ')
        authors_new = []
        print(authors)
        for author in authors:
            print(author)            
            names = author.split(', ')
            if len(names) == 1:
                if ' {' in names:
                    names = author.split(' {')
                else:
                    names = author.split(' ')
                first_names = names[0]
                last_name = names[1].strip('}')
            elif len(names) == 2:
                first_names = names[1].strip()
                last_name = names[0].strip()
            else:
                print('Check author field.')
            author_new = (first_names + ' ' + last_name.strip())    
            authors_new.append(author_new)
            print(author_new)
        bib_item['author'] = ', '.join(authors_new)
        print('----')

        # create bibtex file
        db = BibDatabase()
        db.entries = [bib_item]
        bib_file = 'publications/bib/{0}.bib'.format(bib_item['ID'])
        bib_link = u' [[bib]]({})'.format(bib_file)
        with open('{0}'.format(bib_file), 'w') as bib:
            bib.write(writer.write(db))

        md_file.write(u"- {0}. {2}. **{1}**.{3}{4}. {5} {6}\n".format(bib_item['author'].replace('{','').replace('}',''),
                                                                  bib_item['title'].replace('{','').replace('}',''),
                                                                  bib_item['year'],
                                                                  venue,
                                                                  pages,
                                                                  pdf_link,
                                                                  bib_link))
       
