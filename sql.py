# sql.py - Creates a SQLite3 table and populates it

import sqlite3

# Create the new database for our blog if it doesn't already exist

with sqlite3.connect("blog.db") as connection:

    #cursor
    c = connection.cursor()

    #create table
    c.execute("""CREATE TABLE posts
                (title TEXT, post TEXT)
                """)

    #insert some dummy date to work with
    c.execute('INSERT INTO posts VALUES("Good", "I\'m good.")')
    c.execute('INSERT INTO posts VALUES("Well", "I\'m well.")')
    c.execute('INSERT INTO posts VALUES("Excellent", "I\'m excellent.")')
    c.execute('INSERT INTO posts VALUES("Okay", "I\'m okay.")')