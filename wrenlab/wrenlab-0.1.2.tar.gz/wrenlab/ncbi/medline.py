"""
Parser for MEDLINE XML files.

Example:

.. code-block:: python
   
    from wrenlab.ncbi.medline import parse

    path = "http://www.nlm.nih.gov/databases/dtd/medsamp2013.xml.gz"
    with parse(path) as h:
        for article in path:
            print(article)
"""

import sqlite3
import datetime
import locale
import re
import os
import multiprocessing as mp
import gzip
import pickle
import xml.etree.ElementTree as ET

from collections import namedtuple

import wrenlab.text.nlp
import wrenlab.util
from wrenlab.util import LOG

__all__ = ["parse", "Article", "Journal"]

Article = namedtuple("Article", 
                     "id title abstract publication_date journal citations")
Journal = namedtuple("Journal", "id issn title")

class MedlineXMLFile(object):
    # FIXME: Date parsing will probably only work if system
    #   locale is US English

    _months = dict((i, locale.nl_langinfo(getattr(locale, "ABMON_" + str(i))))
                        for i in range(1,13))
    _non_digit_regex = re.compile(r"[^\d]+")

    def __init__(self, path):
        self._is_open = True
        self._handle = gzip.open(path, "rb")
    
    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        if self._is_open:
            self._handle.close()
            self._is_open = False
    
    def _text(self, xpath):
        try:
            return self._current_element.findall(xpath)[0].text
        except IndexError:
            return None

    def _strip_non_digit(self, text):
        return self._non_digit_regex.sub('', text)

    def _parse_citation(self):
        # Parse Article information
        pmid = int(self._text(".//PMID"))
        title = self._text(".//Article/ArticleTitle")
        abstract = self._text(".//Article/Abstract/AbstractText")

        publication_date = None
        year = self._text(".//Article/Journal/JournalIssue/PubDate/Year")
        if year:
            month = self._text(".//Article/Journal/JournalIssue/PubDate/Month")
            month = self._months.get(month, "01")
            day = self._text(".//Article/Journal/JournalIssue/PubDate/Day") or "01"
            publication_date = datetime.date(int(year), int(month), int(day))

        # Parse Journal information
        journal_id = self._text(".//MedlineJournalInfo/NlmUniqueID")
        journal_id = int(self._strip_non_digit(journal_id))
        journal_issn = self._text(".//MedlineJournalInfo/ISSNLinking")
        journal_name = self._text(".//MedlineJournalInfo/MedlineTA")
        journal = Journal(journal_id, journal_issn, journal_name)

        # Parse Citation information
        citations = set()
        xp = ".//CommentsCorrectionsList/CommentsCorrections"
        for e in self._current_element.findall(xp):
            for c in e.findall("PMID"):
                citations.add(int(c.text))

        return Article(pmid, title, abstract, publication_date, journal, citations)

    def __iter__(self):
        for event, element in ET.iterparse(self._handle):
            if event == "end" and element.tag == "MedlineCitation":
                self._current_element = element
                yield self._parse_citation()

def parse(path_or_handle, lazy=False):
    o = MedlineXMLFile(path_or_handle)
    if lazy:
        return o
    else:
        return list(o)

def _parse_all(medline_dir):
    #pool = mp.Pool(mp.cpu_count() - 10)
    pool = mp.Pool(8)
    paths = [os.path.join(medline_dir, p) 
            for p in os.listdir(medline_dir) if p.endswith(".xml.gz")][:5]
    seen = set()
    for articles in pool.imap(parse, paths):
        for article in articles:
            if article.id in seen:
                continue
            seen.add(article.id)
            yield article

def parse_all(x):
    import itertools
    return itertools.islice(_parse_all(x), 10000)

##########
# Database
##########

class MEDLINE(object):
    def __init__(self, path="~/.cache/wrenlab/medline.db"):
        self._path = os.path.expanduser(path)
        create = not os.path.exists(self._path)
        self._cx = sqlite3.connect(self._path)

        if create:
            schema = wrenlab.util.sql_script("medline")
            c = self._cx.cursor()
            c.executescript(schema)
            self._cx.commit()

    def __del__(self):
        self._cx.close()

    def _is_initialized(self):
        c = self._cx.cursor()
        c.execute("SELECT COUNT(*) FROM journal;")
        n = next(c)[0]
        return n > 0

    def _initialize_import_data(self, path):
        # Stage 1: Import journal
        def journal():
            it = parse_all(path)
            seen = set()
            for article in it:
                if article.journal is None:
                    continue
                j = article.journal
                if not j.id in seen:
                    yield j.id, j.title, j.issn
                    seen.add(j.id)

        LOG.info("Populating journal table ...")
        c = self._cx.cursor()
        c.executemany("INSERT INTO journal VALUES (?,?,?);", journal())
        self._cx.commit()

        # Stage 2: Import abstracts
        def article():
            it = parse_all(path)
            for a in it:
                yield (a.id, a.publication_date, a.title, a.abstract, a.journal.id)
        
        LOG.info("Populating article table ...")
        c = self._cx.cursor()
        c.executemany("INSERT INTO document VALUES (?,?,?,?,?);", article())
        self._cx.commit()

        # Stage 3: Import citations
        def citation():
            it = parse_all(path)
            for a in it:
                for c in a.citations:
                    yield (a.id, c)

        LOG.info("Populating citation table ...")
        c = self._cx.cursor()
        c.executemany("INSERT INTO citation VALUES (?,?);", citation())
        self._cx.commit()

    def _section_map(self):
        c = self._cx.cursor()
        c.execute("SELECT COUNT(*) FROM section;")
        if next(c)[0] > 0:
            return
        else:
            c.executemany("INSERT INTO section VALUES (?,?);",
                    [(0,"title"), (1, "abstract")])
            self._cx.commit()
        c.execute("SELECT name,id FROM section;")
        return dict(c)

    def _initialize_populate_sentence(self):
        def sentence():
            section_map = self._section_map()

            fn = wrenlab.text.nlp.punkt_sentence_tokenizer()
            c = self._cx.cursor()
            c.execute("SELECT id, title, abstract FROM document;")
            for id, title, abstract in c:
                if title is not None:
                    for i,s in enumerate(fn(title)):
                        yield id, section_map["title"], i, s
                if abstract is not None:
                    for i,s in enumerate(fn(abstract)):
                        yield id, section_map["abstract"], i, s

        LOG.info("Populating sentence table ...")
        c = self._cx.cursor()
        c.executemany("INSERT INTO sentence VALUES (?,?,?,?);", sentence())
        self._cx.commit()

    def initialize(self, path):
        """
        Import MEDLINE XML data into the local SQLite database.

        Arguments
        ---------
        path : str
            Path to the directory containing MEDLINE XML files.
        """
        self._initialize_import_data(path)
        self._initialize_populate_sentence()

if __name__ == "__main__":
    db = MEDLINE()
    db.initialize("/data/ncbi/medline/current/")
    #db._initialize_populate_sentence()
