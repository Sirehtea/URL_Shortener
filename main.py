from flask import Flask, render_template, request, redirect
import sqlite3
import logging
from collections import OrderedDict

app = Flask(__name__)

logging.basicConfig(filename='url_shortener.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def create_connection():
    return sqlite3.connect("url_shortener.db")

def create_database():
    con = create_connection()
    cursor = con.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            hash_value INTEGER PRIMARY KEY,
            original_url TEXT
        )
    ''')
    con.commit()
    con.close()

url_cache = OrderedDict()

def remember(func):
    def wrapper(url):
        if url not in url_cache:
            url_cache[url] = func(url)
            if len(url_cache) > 500:
                url_cache.popitem(last=False)  # Verwijdert het OUDSTE item
        return url_cache[url]
    return wrapper

@remember
def shorten_url(url):
    hash_value = hash(url)

    con = create_connection()

    if con:
        try:
            cursor = con.cursor()
            cursor.execute('SELECT original_url FROM urls WHERE hash_value = ?', (hash_value,))
            existing_url = cursor.fetchone()

            if existing_url:
                con.close()
                return existing_url[0]
            else:
                cursor.execute('INSERT INTO urls (hash_value, original_url) VALUES (?, ?)', (hash_value, url))
                con.commit()
                con.close()
                return f'/r/{hash_value}'
        except sqlite3.Error as e:
            logging.error(f'Error bij het verwerken van de URL: {e}')
            con.close()

    return "Fout bij het verwerken van de URL"


@app.route('/')
def show_form():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form.get('original_url')

    if original_url:
        logging.info(f'Ingevoerde URL: {original_url}')

        short_url = shorten_url(original_url)

        return render_template('shorten.html', original_url=original_url, short_url=short_url)

    return redirect('/')

@app.route('/r/<short_url>')
def redirect_to_original(short_url):
    logging.info(f'Opgevraagde verkorte URL: {short_url}')

    con = create_connection()

    if con:
        try:
            cursor = con.cursor()
            cursor.execute('SELECT original_url FROM urls WHERE hash_value = ?', (short_url,))
            result = cursor.fetchone()

            if result:
                con.close()
                return redirect(result[0])
        except sqlite3.Error as e:
            logging.error(f'Error bij het opzoeken van de oorspronkelijke URL: {e}')
            con.close()

    return render_template('not_found.html')

if __name__ == '__main__':
    create_database()
    print("* http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
