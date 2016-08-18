import MySQLdb as mdb
import unicodedata
import lmdb

class DbManager():

    def remove_accents(self, input_str):
        nkfd_form = unicodedata.normalize('NFKD', unicode(input_str.decode('utf-8')))
        return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

    def parse_tag(self, f, tags):

        new_tags = []
        for tag in tags:
            new_tags.append(self.remove_accents(f(tag)))

        return new_tags

    def get_all_rushs_tags(self):

        con = mdb.connect('localhost', 'root', 'castor69', 'webcastor', charset='utf8', use_unicode=True)
        cur = con.cursor()
        cur.execute('SELECT tags, media_ref FROM jos_inwicast_medias')

        str_tags = cur.fetchall()
        tags = []
        for str_tag in str_tags:
            tags = tags + [(self.parse_tag(lambda x: x.strip().lower().encode('utf-8'), str_tag[0].split(',')), str_tag[1])]

        return tags