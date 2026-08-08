from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS donors
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  blood_group TEXT NOT NULL,
                  city TEXT NOT NULL,
                  phone TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        blood_group = request.form['blood_group']
        city = request.form['city']
        phone = request.form['phone']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO donors (name, blood_group, city, phone) VALUES (?, ?, ?, ?)",
                  (name, blood_group, city, phone))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/donor_search')
def donor_search():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM donors")
    donors = c.fetchall()
    conn.close()
    return render_template('donor_search.html', donors=donors)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)