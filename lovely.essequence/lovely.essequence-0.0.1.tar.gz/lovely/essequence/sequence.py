import threading


# The storage for the data of the sequences
SEQUENCES = {}

GLOBAL_SEQUENCE_LOCK = threading.Lock()


class Sequence(object):
    """A sequence number generator

    This generator can generate integer sequences which are unique and
    guaranteed to be in ascending order over multiple processes.

    It uses the elasticsearch _update feature to increment an iid counter.

    Sequences are thread save.
    """

    ES = None
    _exists = False

    def __init__(self, name, bulk_size=10, transform=None, es=None):
        self.name = name
        if es:
            self.ES = es
        self.bulk_size = bulk_size
        if transform is None:
            self.transform = lambda n: n
        else:
            self.transform = transform

    def next(self):
        """Provide and consume the next id
        """
        with self._get_lock():
            return self.transform(self._get_bulk().pop())

    def _get_sequence_data(self):
        """Thread safe access to a named lock object"""
        global GLOBAL_SEQUENCE_LOCK, SEQUENCES
        with GLOBAL_SEQUENCE_LOCK:
            if self.name not in SEQUENCES:
                SEQUENCES[self.name] = {
                    'lock': threading.Lock(),
                    'bulk': [],
                    'exists': False,
                }
            return SEQUENCES[self.name]

    def _get_lock(self):
        return self._get_sequence_data()['lock']

    def _get_bulk(self):
        """Get the current bulk.

        Must be executed inside a local lock.
        data = self._get_sequence_data()
        """
        data = self._get_sequence_data()
        if not data['bulk']:
            self._ensure_exists()
            result = self.ES.update(
                index=INDEX_NAME,
                doc_type=INDEX_TYPE,
                id=self.name,
                body={
                    "script": "ctx._source['iid'] += bulk_size",
                    "lang": "groovy",
                    "params": {
                        "bulk_size": self.bulk_size
                    },
                    "upsert": {
                        'iid': self.bulk_size
                    },
                },
                refresh=True,
                retry_on_conflict=10,
                fields='iid',
            )
            iid = result['get']['fields']['iid'][0]
            data['bulk'] = range(iid, iid - self.bulk_size, -1)
        return data['bulk']

    def _ensure_exists(self):
        """Make sure the index and sequence exists

        Is only called the first time a sequence is used inside of a process.

        Must be executed inside a local lock.
        """
        data = self._get_sequence_data()
        if data['exists']:
            return
        es = self.ES
        if es is None:
            return
        es.indices.create(
            INDEX_NAME,
            INDEX_SETTINGS,
            ignore=400  # ignore index already exists
        )
        es.cluster.health(wait_for_status='yellow', timeout='10s')
        data['exists'] = True


INDEX_NAME = 'lc_iidsequences'
INDEX_TYPE = 'iid'
INDEX_SETTINGS = """
{
    "settings": {
        "number_of_shards": 1,
        "auto_expand_replicas": "0-all"
    },
    "mappings": {
        "iid": {
            "_all": {"enabled": 0},
            "_type": {"index": "no"},
            "dynamic": "strict",
            "properties": {
                "iid": {
                    "type": "long",
                    "index": "no"
                }
            }
        }
    }
}
"""


def testing_reset_sequences():
    """Reset all sequences for testing

    Note:
        This method is not thread save and must not be used if multiple
        processes use the sequence.
    """
    global SEQUENCES
    for name, data in SEQUENCES.iteritems():
        data = SEQUENCES[name]
        data['bulk'] = None
        data['exists'] = False
    es = Sequence.ES
    es.indices.delete(index=INDEX_NAME, ignore=404)
