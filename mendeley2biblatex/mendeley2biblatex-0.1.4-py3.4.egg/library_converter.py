import sqlite3
import sys

from .bib_entry import BibEntry


def dict_factory(cursor, row):
    """A function to use the SQLite row as dict for string formatting"""
    d = {}
    for idx, col in enumerate(cursor.description):
        if row[idx]:
            d[col[0]] = row[idx]
        else:
            d[col[0]] = ''
    return d


class LibraryConverter:
    @staticmethod
    def convert_library(db_name, bibtex_file=sys.stdout, quiet=False, folder=None):
        """Converts Mendely SQlite database to BibTeX file
        @param db_name The Mendeley SQlite file
        @param bibtex_file The BibLaTeX file to output the bibliography, if not
    supplied the output is written to the system standard stdout.
        @param quiet If true do not show warnings and errors
        @param folder If provided the Rult gets filtered by folder name
        """

        db = sqlite3.connect(db_name)
        c = db.cursor()
        # c.row_factory = sqlite3.Row # CANNOT be used with unicode string formatting
        # since it expect str indexes, and we are using
        # unicode string... grrr... ascii is not dead
        c.row_factory = dict_factory  # allows to use row (entry) as a dict with
        # unicode keys.

        if sys.stdout != bibtex_file:
            f = open(bibtex_file, 'w')
            f.write("""This file was generated automatically by Mendeley To
    BibLaTeX python script.\n\n""")
        else:
            f = bibtex_file

        query = '''
            SELECT
            D.id,
            D.citationKey,
            D.title,
            D.type,
            D.doi,
            D.publisher,
            D.publication,
            D.volume,
            D.issue,
            D.institution,
            D.month,
            D.year,
            D.pages,
            D.revisionNumber AS number,
            D.sourceType,
            DU.url,
            D.dateAccessed AS urldate
        FROM Documents D
        LEFT JOIN DocumentCanonicalIds DCI
            ON D.id = DCI.documentId
        LEFT JOIN DocumentFiles DF
            ON D.id = DF.documentId
        LEFT JOIN DocumentUrls DU
            ON DU.documentId = D.id
        LEFT JOIN DocumentFolders DFO
            ON D.id = DFO.documentId
        LEFT JOIN Folders FO
            ON DFO.folderId = FO.id
        WHERE D.confirmed = "true"
        AND D.deletionPending= "false"
        '''

        if folder is not None:
            query += 'AND FO.name="' + folder + '"'

        query += '''
        GROUP BY D.citationKey
        ORDER BY D.citationKey
        ;'''

        for entry in c.execute(query):
            c2 = db.cursor()
            c2.execute('''
        SELECT lastName, firstNames
        FROM DocumentContributors
        WHERE documentId = ?
        ORDER BY id''', (entry['id'],))
            authors_list = c2.fetchall()
            authors = []
            for author in authors_list:
                authors.append(', '.join(author))
            entry['authors'] = ' and '.join(authors)

            if isinstance(entry['url'],bytes):
                entry['url'] = entry['url'].decode('UTF-8')

            BibEntry.clean_characters(entry)
            # If you need to add more templates:
            #    all types of templates are available at
            #    http://www.cs.vassar.edu/people/priestdo/tips/bibtex
            #    all avaliable types are described in biblatex documentation
            #    ftp://ftp.mpi-sb.mpg.de/pub/tex/mirror/ftp.dante.de/pub/tex/macros/latex/contrib/biblatex/doc/biblatex.pdf
            try:
                formatted_entry = BibEntry.TEMPLATES.get(entry['type']).format(
                    entry=entry)

            except AttributeError:
                if not quiet:
                    print('''Unhandled entry type {0}, please add your own template.'''.format(
                        entry['type']))
                continue
            f.write(formatted_entry)

        if sys.stdout != bibtex_file:
            f.close()
