import sqlite3
import random
import time


conn = sqlite3.connect('example.db')
c = conn.cursor()


def rnd():
    return random.random()

def rnds():
     return str(random.random())

start = time.time()

# Create table
c.execute('''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)''')

for row in c.execute('SELECT COUNT(*) FROM stocks'):
    print(row)
        
# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
# Larger example that inserts many records at a time
purchases = []
for i in range(1000*1000):
    p = (rnds(), rnds(), rnds(), rnd(), rnd())
    purchases.append(p)
    c.execute('INSERT INTO stocks VALUES (?,?,?,?,?)', p)

# c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
# Save (commit) the changes
conn.commit()

for row in c.execute('SELECT COUNT(*) FROM stocks'):
    print(row)
    
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

end = time.time()
print(str(end-start))
