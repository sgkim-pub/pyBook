import sqlite3

conn = sqlite3.connect('pyBook.db')
cursor = conn.cursor()

# SQL = 'DROP TABLE articles'
#
# cursor.execute(SQL)

SQL = 'CREATE TABLE IF NOT EXISTS articles (articleNo INTEGER PRIMARY KEY AUTOINCREMENT, ' \
      'author TEXT NOT NULL, title TEXT NOT NULL, category INTEGER, description TEXT, price INTEGER, picture TEXT)'

cursor.execute(SQL)

cursor.close()
conn.close()
