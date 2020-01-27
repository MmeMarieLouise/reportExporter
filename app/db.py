from sqlalchemy import create_engine

# create engine object to connect to remote postgres server
engine = create_engine('postgresql+psycopg2://interview:uo4uu3AeF3@candidate.suade.org/suade')

# connect to remote server and returns a connect object, inside () can execute sql commands to query database, if it returns a proxy object - then use fetchall()
#  o = conn.execute('select * from reports')
#  o.fetchall()

conn = engine.connect()

all_tables = engine.table_names()

results = conn.execute('select * from reports')

for row in results:
    print(row)

conn.close()


