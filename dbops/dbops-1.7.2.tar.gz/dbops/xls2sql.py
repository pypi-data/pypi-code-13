import xlrd


class Xls2Sql(object):
    """convert some common xls formats to sql patches."""

    def __init__(self, a="Id", b="SecId", c="Name",
                 table="dual", fin="patch.xls",
                 findopt={"Id": 1, "Name": 2}, lookup="", skiprows=1,
                 range2=[2, 3], t1="mysql.user", t2="mysql.user",
                 db="schemadb", t3="", d="", lookup2="", ina="", inb=""):
        """initalize the conversion."""
        self.xls = xlrd.open_workbook(fin).sheet_by_index(0)  # sheet
        # discard rows to skip in xls
        self.skiprows = skiprows
        self.range2 = range2
        self.table = table
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.findopt = findopt
        self.lookup = lookup
        self.lookup2 = lookup2
        self.db = db
        if not ina:
            self.ina = self.a
        else:
            self.ina = ina
        if not inb:
            self.inb = self.b
        else:
            self.inb = inb

    def query_gen_2(self):
        """Create a query for 2 cols (a relation between existing entities)."""
        query = "use " + self.db + "; \n"
        query = query + "insert ignore into " + self.table
        query = query + " (" + self.a + "," + self.b + ") values "
        for rownum in range(self.skiprows, self.xls.nrows):
            row = self.xls.row_values(rownum)
            alpha = "(select " + self.a + " from " + self.t1 + " where "
            for key, value in self.findopt.iteritems():
                alpha = alpha + "'" + key + "'" + " = "
                alpha = alpha + "'" + row[value].replace("'", r"\'")
                alpha = alpha + "'" + " and "
            alpha = alpha[:-4] + " limit 1)"  # remove last 'and'
            for cn in self.range2:
                try:
                    thecell = row[cn]
                except IndexError:
                    thecell = ''
                if not thecell == '':
                    if self.lookup:
                        beta = "(select " + self.lookup + " from "
                        beta = beta + self.t2 + " where " + self.c + " = '"
                        beta = beta + (thecell).replace("'", r"\'")
                        beta = beta + "' limit 1)"
                    else:
                        beta = "'" + (thecell).replace("'", r"\'") + "'"
                    query = query + " (" + alpha + "," + beta + "),"
        return query[:-1]  # remove last comma and return

    def query_gen_3(self):
        """Make relation between two tables using a third as lookup."""
        query = "use " + self.db + "; \n"
        prefix1 = "insert ignore into " + self.table
        prefix1 = prefix1 + " (" + self.ina + "," + self.inb + ") select "
        for rownum in range(self.skiprows, self.xls.nrows):
            query = query + prefix1
            row = self.xls.row_values(rownum)
            alpha = "(select " + self.a + " from " + self.t1 + " where "
            for key, value in self.findopt.iteritems():
                alpha = alpha + key + " = "
                alpha = alpha + "'" + row[value].replace("'", r"\'")
                alpha = alpha + "'" + " and "
            alpha = alpha[:-4] + " limit 1), "  # remove last 'and'
            alpha = alpha + " " + self.d + " from " + self.t3 + " where "
            for cn in self.range2:
                try:
                    thecell = row[cn]
                except IndexError:
                    thecell = ''
                if not thecell == '':
                    if self.lookup:
                        beta = self.lookup2 + " = "
                        beta = beta + "(select " + self.lookup + " from "
                        beta = beta + self.t2 + " where " + self.c + " = '"
                        beta = beta + (thecell).replace("'", r"\'")
                        beta = beta + "' limit 1) or"
                    else:
                        beta = "'" + (thecell).replace("'", r"\'") + "'"
                alpha = alpha + beta + " "
            query = query + alpha[:-4] + "; \n "
        return query + ";"  # remove last union and return

if __name__ == "__main__":
    import sys
    args = ['nothing', 'Id', 'SecId', 'Name', 'dual', 'patch.xls',
            {"Id": 1, "Name": 2}, "", 1, 2, 3, 'mysql.user', 'mysql.user',
            'schemadb']
    for x in range(1, len(sys.argv)):
        args[x] = sys.argv[x]
    searcher = Xls2Sql(args[1], args[2], args[3], args[4], args[5], args[6],
                       args[7], range(args[8], args[9]), args[10], args[11],
                       args[12], args[13])
    print(searcher.query_gen_2())
