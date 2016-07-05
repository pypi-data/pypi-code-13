import sqlite3, unittest
from .helpers import get_sql_results_factory, dict_factory
from . import db_path
from pypershelf import base_model_factory
from pypershelf.play import f

def setup_module(module):
    global conn
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    setup_artist_class(module)
    setup_album_class(module)

def setup_artist_class(module):
    global Artist
    BaseModel = base_model_factory(get_sql_results_factory(conn))
    class Dummy(BaseModel):
        table_name = "Artist"
        pk = "ArtistId"

        @property
        def albums(self):
            return self.inboundHasMany(Album, 'ArtistId', 'ArtistId')
    Artist = Dummy

def setup_album_class(module):
    global Album
    BaseModel = base_model_factory(get_sql_results_factory(conn))
    class Dummy(BaseModel):
        table_name = "Album"
        pk = "AlbumId"

        @property
        def artist(self):
            return self.outboundHasOne(Artist, 'ArtistId', 'ArtistId')
    Album = Dummy

def teardown_module(module):
    conn.close()

def test_db_setup():
    cur = conn.cursor()
    cur.execute("select * from Artist")
    results = cur.fetchall()
    cur.close()
    assert(len(results)==275)

class TestSelectAll(unittest.TestCase):
    def test_artists(self):
        self.assertEqual(len(Artist.all()), 275)

    def test_albums(self):
        self.assertEqual(len(Album.all()), 347)

    def test_play(self):
        self.assertIn('water', f())

class TestRelationships(unittest.TestCase):
    def test_outbound_has_one(self):
        album = Album.all()[0]
        self.assertEqual(album.artist.Name, 'AC/DC')

    def test_inbound_has_many(self):
        artist = Artist.all()[0]
        self.assertEqual(artist.albums[0].Title, 'For Those About To Rock We Salute You')
