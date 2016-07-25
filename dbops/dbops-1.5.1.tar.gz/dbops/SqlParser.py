import re


class SqlParser(object):
    state = "start"  # what we are at
    routine = "start"  # what we are looking through
    next_state = "verb"  # what state do we want to go to
    previous= "no"
    position = 0
    errors = []
    query = []
    verbs = ["insert", "update", "create", "delete", "use", "index"]
    delimeter = ";"

    def __init__(self, query):
        """Take a query in and make a parser object."""
        raise FutureWarning("SqlParser under construction.")
        self.raw_query = query
        self.query = query.split(" ")

    def is_valid_col(self, this_in):
        """Return true if matches col regex."""
        cre = re.compile("^[a-zA-Z_][a-zA-Z0-9_]*$")
        re.search(cre, this_in)
        return False

    def is_valid_expr(self, this_in):
        """Return true if matches expr regex."""
        # TODO make this match expr rules
        cre = re.compile("^[a-zA-Z_][a-zA-Z0-9_]*$")
        re.search(cre, this_in)
        return False

    def add_error(self, type, message):
        """Add an error to the error list, return False if fatal."""
        self.errors.append(type.upper() + ": Word " +
                           str(self.position+1) + ": " + message)
        if (type.upper() == "FATAL"):
            self.finish()
            return False

    def next_word(self):
        """get the next word in the query."""
        if self.position >= len(self.query):
            return False
        wordin = self.query[self.position].lower()
        # does it have a delimiter or comma?
        word = re.split(re.escape(self.delimiter)+"|,", wordin)[0]
        # split out that word, add rest back in too
        wordout = wordin[(len(word)+1):]
        self.query.insert(self.position, word)
        self.query.insert(self.position+1, wordout)
        self.position = self.position + 1
        return word

    def finish(self):
        """Print errors and stop parsing."""
        print self.errors()

    def parse(self):
        """Generic parsing engine."""
        self.routine = self.next_word()
        if self.routine in self.verbs:
            self.state = self.routine
            self.parse_verb()
        else:
            if not self.add_error("FATAL", "Did not recognize word " +
                                  self.routine):
                return False

    def parse_verb(self):
        """Parsing engine for verbs."""
        if hasattr(self, "parse_" + self.routine):
            fun = getattr(self, "parse_" + self.routine)
            fun()
        else:
            if not self.add_error("FATAL", "Did not recognize verb " +
                                  self.routine):
                return False

    def parse_select(self):
        """Parser for select statements, pushdown automaton."""
        subqueries = ["select", "join"]
        set_previous = ["from", "where", "group", "having", "order"]
        need_previous = ["expr", "column", "num"]
        # use 2 maps to simply check validity
        valid_map = {"select": ["distinct", "all", "column"],
                     "distinct": ["column"],
                     "all": ["column"],
                     "column": ["column",
                                "from", "where", "group", "order", "limit"],
                     "from": ["column", "subquery"],
                     "where": ["expr"],
                     "group": ["by"],
                     "by": ["expr"],
                     "expr": ["expr", "group", "having", "offset"],
                     "having": ["expr"],
                     "order": ["by"],
                     "limit": ["expr"],
                     "offset": ["expr"]}
        # format; prev:[nexts]
        prev_map = {"no": [],
                    "from": ["column"],
                    "where": ["group", "order", "limit"],
                    "group": ["having", "order", "limit"],
                    "having": ["order", "limit"],
                    "order": ["expr", "limit"]}
        word = self.next_word()
        if not word:
            return True
        # figure out what we're looking at now
        if word in set_previous:
            self.previous = word
        if word in need_previous:
            # check if next word works with previous
            next_word = self.query[self.position+1]
            if next_word not in prev_map[self.previous]:
                if(("expr" in prev_map[self.previous]) or
                   ("column" in prev_map[self.previous])):
                    if not ((self.is_valid_col(next_word) and "column" in
                            prev_map[self.previous])or
                            (self.is_valid_expr(next_word) and
                            "expr" in prev_map[self.previous])):
                        if not self.add_error("FATAL", "error in" +
                                              self.previous + "statement"):
                            return False
        if word in subqueries:
            self.next_state = "subquery"
        elif (self.is_valid_col(word)):
            self.next_state = "column"
        elif (self.is_valid_expr(word)):
            self.next_state = "expr"
        else:
            self.next_state = word
        if self.next_state not in valid_map[self.state]:
            if not self.add_error("FATAL", "error in" + self.routine +
                                  "statement"):
                return False
        else:
            if word == "subquery":
                self.parse()
            self.parse_select()
