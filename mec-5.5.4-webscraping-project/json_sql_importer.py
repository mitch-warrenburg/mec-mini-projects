import json
import sqlite3


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY ASC, 
                quote TEXT, 
                author TEXT)
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                tag TEXT, 
                quote_id INTEGER, 
                FOREIGN KEY(quote_id) REFERENCES quotes(id))
        ''')

    connection.commit()


def import_quotes(connection):
    cursor = connection.cursor()

    with open('scrapy_mini_project/css-scraper-results.json') as jsonFile:
        quotes = json.load(jsonFile)

        for quote in quotes:
            quote_values = (quote['text'], quote['author'])
            cursor.execute('INSERT INTO quotes (quote, author) VALUES (?, ?)', quote_values)

            quote_id = cursor.lastrowid

            for tag in quote['tags']:
                tag_values = (tag, quote_id)
                cursor.execute('INSERT INTO tags (tag, quote_id) VALUES (?, ?)', tag_values)

    connection.commit()


quotes_connection = sqlite3.connect('scrapy_quotes.db')

create_tables(quotes_connection)
import_quotes(quotes_connection)

quotes_connection.close()
