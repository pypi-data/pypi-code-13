"""
LordKey

It solves the problem of determining the combination in a sequence based on
the some alphabet with a given length, and use combination to determine the
iteration index.


The problem.

There are several elements to iterate - a, b and c. How many possible
combinations for unique enumeration if key size is 3? Or which combination is
at the tenth iteration? Or which iteration corresponds the `acc` combination?

For `abc` alphabet and 3 key size can be created the next iterations::

     0. aaa      1. aab      2. aac      3. aba      4. abb      5. abc
     6. aca      7. acb      8. acc      9. baa     10. bab     11. bac
    12. bba     13. bbb     14. bbc     15. bca     16. bcb     17. bcc
    18. caa     19. cab     20. cac     21. cba     22. cbb     23. cbc
    24. cca     25. ccb     26. ccc

So, the maximum number of iterations - 27, for 10 iteration corresponds to
`baa` combination and the `acc` combination - it is 7 iteration.


The theory.

Use the arbitrary alphabet (set of available characters to create a key) and
size of key can be created a sequence of unique combinations, where each new
combination has its unique numeric index (from 0 to N - where the N is maximum
number of possible combinations or infinity).

If specify the index (for example an ID in the table of database) - will be
returned the combination (key) for this index, and if specify combination -
will be returned it index.

P.s. The sequence is not created - just calculate the data of a specified
element. This algorithm allows you to quickly get the result.

Example::

    # INITIAL DATA
    # =================
    # Alphabet | abcde
    # ---------+-------
    # Key size | 3
    #
    # SEQUENCE
    # ==============================================
    # ID  |  0  |  1  |  2  | ... | 122 | 123 | 124
    # ----+-----+-----+-----+-----+-----+-----+-----
    # Key | aaa | aab | aac | ... | eec | eed | eee

    lk = LordKey(alphabet='abcde', size=3)
    lk.get_key_by_id(122) # eec
    lk.get_id_by_key('ecc') # 122

The alphabet may be omitted then will be used value by default. If not set the
size value - key size can be from one char to infinity.

Example::

    # Size not specified.
    lk = LordKey(alphabet='abc')
    lk.get_key_by_id(1) # b
    lk.get_key_by_id(10) # bab
    lk.get_key_by_id(100) # bacab
    lk.get_key_by_id(1000) # bbabaab
    lk.get_key_by_id(10000) # bbbcabbab
    lk.get_key_by_id(100000) # bcaacabbcab
    lk.get_key_by_id(1000000) # bcbccbacacaab
    lk.get_key_by_id(10000000) # caacbbaabbacbab

"""

__copyright__ = 'Copyright 2016, LordKey. All rights reserved.'
__license__ = 'MIT'
__version__ = '0.0.2'
__status__ = 'Production'
__author__ = 'Dvydenko Myroslav <valsorym>'
__email__ = 'i@valsorym.com'


class LordKey(object):
    """Determination of the key by the ID or the ID by the key.

    It is possible to expand the ability of the base class by adding caching
    system. For this is enough override the caching's methods: ``_cache_init``,
    ``_cache_write``, ``_cache_read``, ``_cache_is_active``.


    """
    ALPHABET = 'vWyuag74bU6ctXm1Fxe2iMrfLGdIwV3NZsoEjRJPphYDQ59HCzqOABl8kKST0n'

    def __init__(self, alphabet=None, size=None):
        """Create the basic parameters for generating of the sequence."""
        if alphabet is not None and not isinstance(alphabet, str):
            # The alphabet can be only string (str type) or None type.
            # If alphabet not set (has None value) - use default alphabet.
            errmsg = (
                "The 'alphabet' must be 'str' or None type. "
                "The '{}' object is not 'str' type."
            ).format(type(alphabet))
            raise TypeError(errmsg)
        elif isinstance(alphabet, str) and len(alphabet) != len(set(alphabet)):
            # The alphabet should not have symbols duplicates.
            errmsg = 'The alphabet should not have symbols duplicates.'
            raise ValueError(errmsg)

        # Size can be an integer greater than zero or None type.
        if not isinstance(size, (int, type(None), )):
            errmsg = (
                "The size must be 'int' or 'None' type. "
                "The size can't be of the '{}' type."
            ).format(type(size))
            raise TypeError(errmsg)
        elif isinstance(size, int) and size < 1:
            errmsg = 'The size can be None or an integer greater than zero.'
            raise ValueError(errmsg)

        # Alphabet and size are specified correctly.
        self._alphabet = alphabet or self.ALPHABET
        self._size = size

        # Determine the length of the alphabet and to determine the maximum
        # size of the sequence - there are no restrictions (None) if the size
        # is not specified.
        self._alphabet_len = len(self._alphabet)
        self._last_id = len(self._alphabet) ** size if size else None

    def _cache_init(self, *args, **kwargs):
        """The method can be overridden in descendants to initialize the cache
        settings.

        """
        pass

    def _cache_write(self, *, id, key):
        """The method can be overridden in descendants to write the id and the
        corresponding sequence into cache.

        """
        pass

    def _cache_read(self, *, id=None, key=None):
        """The method can be overridden in descendants to read data from the
        cache. Can specified only id or just key at an one moment of the time.

        Return None if the element is not found in the cache.

        """
        return None

    def _cache_is_active(self):
        """The method can be overridden in descendants - returns True if the
        cache is enabled.

        """
        return False

    @property
    def last_id(self):
        """Return the last available ID in the sequence or None - if the
        sequence is infinite.

        """
        return self._last_id

    @property
    def alphabet(self):
        """Return the currently used alphabet."""
        return self._alphabet

    @property
    def size(self):
        """Return the currently size of key or None if key is not have size."""
        return self._size

    def get_key_by_id(self, id):
        """Get the sequence element (key) by ID."""
        if self.last_id and id >= self.last_id:
            # If there is a restriction on the size of the key.
            errmsg = (
                'Too high a ID value. '
                'The max value of {}.'
            ).format(self.last_id)
            raise ValueError(errmsg)
        elif id < 0:
            # Unable to determine the key for the negative ID.
            raise ValueError('Too small a ID value.')

        # Find in the cache.
        # Cache: Accessing to the cache can be implemented in descendants.
        if self._cache_is_active():
            key = self._cache_read(id=id)
            if key:
                # Limit the size of the key (if necessary).
                return key[-1 * self._size:] if self._size else key

        # Create a hash based on the ID.
        # Note: Do not use ``divmode here`` - it works more slowly!
        l, r = id // self._alphabet_len, id % self._alphabet_len
        result = [self.alphabet[r], ]
        while l >= self._alphabet_len:
            l, r = l // self._alphabet_len, l % self._alphabet_len
            result.insert(0, self.alphabet[r])

        # Only if there is a balance.
        if l:
            result.insert(0, self.alphabet[l])

        # Create the right size wrench.
        if self.size:
            lack = range(self._size - len(result))
            result = [self._alphabet[0] for i in lack] + result

        # Result as a string.
        key = ''.join(result)

        # Save to the cache.
        # Cache: Accessing to the cache can be implemented in descendants.
        if self._cache_is_active():
            self._cache_write(id=id, key=key)

        return key

    def get_id_by_key(self, key):
        """Get the ID by sequence element (key)."""
        def get_clean_key(key):
            """Remove the leading characters and reverse the key.

            If alphabet == 'abc ... ... ... ', i.e. first char is 'a', and
            the key is 'aaacab', so need create 'acab' - remove the first
            duplicates.

            """
            key_len = len(key)
            if key_len < 2:
              return key

            seek, zerro_char = 0, self._alphabet[0]
            while seek < key_len and zerro_char == key[seek]:
                seek += 1

            # Remove the leading chars and reverse key.
            return key[:seek - key_len - 2:-1]


        if not key or not isinstance(key, (str, )):
            # The key should be not an empty string.
            raise ValueError('The key should be not an empty string.')
        elif self._size and len(key) != self._size:
            # Size not equal the required size.
            errmsg = (
                "Size not equal the required size: "
                "'{}' {} != {}."
            ).format(key, len(key), self._size)
            raise ValueError(errmsg)

        # Find in the cache.
        # Cache: Accessing to the cache can be implemented in descendants.
        if self._cache_is_active():
            id = self._cache_read(key=key)
            if id is not None:
                return id

        # Decompile.
        id, clean_key = 0, get_clean_key(key)
        for i, char in enumerate(clean_key):
            try:
                index = self._alphabet.index(char)
                iter = self._alphabet_len ** i
                id +=  iter * index if i > 0 else index
            except ValueError:
                errmsg = (
                    "The '{}' key has the '{}' char that are not included "
                    "in the '{}' alphabet."
                ).format(key, char, self._alphabet)
                raise ValueError(errmsg)

        # Save to the cache.
        # Cache: Accessing to the cache can be implemented in descendants.
        if self._cache_is_active():
            self._cache_write(id=id, key=key)

        return id

