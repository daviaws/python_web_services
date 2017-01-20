import sqlite3

conn = sqlite3.connect('app.db')

c = conn.cursor()

c.execute("""drop table if exists person""")

conn.commit()

person_table = """create table person (
    cpf         int     PRIMARY KEY NOT NULL,
    name			        text	NOT NULL,
    age                     int     NOT NULL,
    height		            real    NOT NULL)"""

#BEGIN CREATE TABLES
c.execute(person_table)
c.execute("""CREATE UNIQUE INDEX index_person_cpf ON person (cpf)""")

conn.commit()
#END CREATE TABLES

print('select person\n')
c.execute ("""select * from person""")
for row in c:
        print (row)
        print(row[1])
print('\n')

c.close()
