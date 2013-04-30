from flask import Flask
from flask import request, render_template, redirect, flash, url_for, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/energy', methods=['POST'])
def energy():
	artist = request.form.get('artist').title()
	conn = sqlite3.connect('/home/shobit/development/big-data-project/subsets/databases/artist_energy.db')
	c = conn.execute("SELECT * FROM artistenergy WHERE artist_name = '" + artist + "'")
	l = c.fetchone()
	return jsonify(results = l)

@app.route('/similar', methods=['POST'])
def similar():
	artist = request.form.get('artist').lower()
	conn = sqlite3.connect('/home/shobit/development/big-data-project/subsets/databases/similar_artists.db')
	c = conn.execute("select * from similar where artist_name='" + artist + "' ORDER BY CAST(value as float) DESC")
	l = c.fetchall()
	return jsonify(similars = l)

@app.route('/listens', methods=['POST'])
def listens():
	artist = request.form.get('artist').lower()
	conn = sqlite3.connect('/home/shobit/development/big-data-project/subsets/databases/top_artists.db')
	c = conn.execute("SELECT * FROM charts WHERE artist_name = '" + artist + "'");
	listens = c.fetchone()
	return jsonify(listens = listens)

@app.route('/geo', methods=['POST'])
def geo():
	artist = request.form.get('artist').title()
	conn = sqlite3.connect('/home/shobit/development/big-data-project/subsets/databases/geo.db')
	c = conn.execute("SELECT country, value FROM geodist where artist_name = '" + artist + "' ORDER BY CAST(value AS INTEGER) DESC")
	l = c.fetchall()
	return jsonify(geodata = l)

@app.route('/demographics', methods=['POST'])
def demographics():
	artist = request.form.get('artist').title()
	conn = sqlite3.connect('/home/shobit/development/big-data-project/subsets/databases/demo.db')
	c = conn.execute("SELECT gender, value FROM demo WHERE artist_name='" + artist + "'")
	l = c.fetchall()
	return jsonify(d = l)
@app.route('/topartists', methods=['POST'])
def topartists():
	conn = sqlite3.connect('/home/shobit/development/big-data-project/subsets/databases/top_artists.db')
	c = conn.execute("SELECT artist_name, hits FROM charts ORDER BY CAST(hits as integer) DESC LIMIT 50");
	temp = c.fetchall()
	topsongs = []
	for t in temp:
		m = []
		m.append(t[0].title())
		m.append(t[1])
		topsongs.append(m)
	print topsongs
	conn2 = sqlite3.connect('/home/shobit/development/big-data-project/subsets/databases/song_frequency.db')
	c2 = conn2.execute("SELECT song_name, artist_name, frequency FROM song_frequency ORDER BY CAST(frequency as INTEGER) DESC LIMIT 50");
	topartists = c2.fetchall()
	return jsonify(top = topsongs, artists = topartists)

@app.route('/artisttopsongs', methods=['POST'])
def artisttopsongs():
	artist = request.form.get('artist').title()
	conn = sqlite3.connect('/home/shobit/development/big-data-project/subsets/databases/song_frequency.db')
	c = conn.execute("SELECT song_name FROM song_frequency WHERE artist_name='" + artist + "' ORDER BY CAST(frequency as INTEGER) DESC LIMIT 10")
	topsongs = c.fetchall();
	return jsonify(topsongs = topsongs)

if __name__ == "__main__":
	app.run(debug=True)
