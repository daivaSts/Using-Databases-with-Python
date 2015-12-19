# Coursera.org /Learn to Program and Analyze Data with Python Specialization
# Course 4 - Using Databases with Python
# Week 3
# Assignment: Multi-Table Database - Tracks. Create a python code to parse an XML list of albums,
# artists, and genres(provided) and produce a properly normalized database using a Python program.

import xml.etree.ElementTree as ET
import sqlite3

# Open a connection to the SQLite database file database called trackdb.sqlite:
conn = sqlite3.connect('trackdb.sqlite')
cursor = conn.cursor()

# Create 4 tables
cursor.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')


# Provide a new or use provided source xml file, sample of the file:

source_file = raw_input('Enter file name: ')
if ( len(source_file) < 1 ) :
    source_file = 'Library-short.xml'


'''
The lookup function returns the entry's string or integer tag content
if the key tag content matches to the provided string
Entry sample:
<key>Track ID</key><integer>369</integer>
<key>Name</key><string>Another One Bites The Dust</string>
<key>Artist</key><string>Queen</string>
'''
def lookup(d, key):
    ''' (element, string) --> string
    '''
    found = False
    for child in d:
        if found :
            return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

stuff = ET.parse(source_file)
all_list = stuff.findall('dict/dict/dict')
#print 'Dict count:', len(all_list)

'''
Iterates over the list created by parsing the source xml file and adds the extracted
data to the appropriate tables of the database.
'''
for entry in all_list:
    if ( lookup(entry, 'Track ID') is None ) : continue

    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')
    genre = lookup(entry, 'Genre')


    if name is None or artist is None or album is None or genre is None:
        continue

    cursor.execute('''INSERT OR IGNORE INTO Artist (name)  VALUES ( ? )''', ( artist,))
    cursor.execute('SELECT id FROM Artist WHERE name = ? ', (artist,))
    artist_id = cursor.fetchone()[0]

    cursor.execute('''INSERT OR IGNORE INTO Album (title, artist_id) VALUES ( ?, ? )''', (album, artist_id))
    cursor.execute('SELECT id FROM Album WHERE title = ? ', (album,))
    album_id = cursor.fetchone()[0]

    cursor.execute('''INSERT OR IGNORE INTO Genre (name) VALUES ( ? )''', ( genre,))
    cursor.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
    genre_id = cursor.fetchone()[0]

    cursor.execute('''INSERT OR REPLACE INTO Track (title, album_id, len, rating, count, genre_id)
        VALUES ( ?, ?, ?, ?, ?, ? )''', (name, album_id, length, rating, count, genre_id))

    conn.commit()
