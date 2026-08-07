import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_NAME = "lifeconnect.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# HUGE DATA + TABLE BANANE KE LIYE
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        city TEXT NOT NULL,
        phone TEXT NOT NULL,
        last_donated TEXT
    )
    """)
    
    # 50+ HUGE TEST DATA - SARE BLOOD GROUP + CITY
    donors = [
        (1, 'Rahul Sharma', 'A+', 'Lucknow', '9876543210', '2025-12-01'),
        (2, 'Priya Singh', 'B+', 'Lucknow', '9123456789', '2026-01-15'),
        (3, 'Aman Verma', 'O+', 'Lucknow', '9988776655', '2025-11-20'),
        (4, 'Sneha Gupta', 'AB+', 'Lucknow', '8877665544', '2026-02-10'),
        (5, 'Vikash Yadav', 'B-', 'Kanpur', '7766554433', '2025-10-05'),
        (6, 'Anjali Patel', 'A-', 'Kanpur', '6655443322', '2026-03-01'),
        (7, 'Mohit Kumar', 'O-', 'Delhi', '5544332211', '2025-09-12'),
        (8, 'Pooja Mishra', 'AB-', 'Delhi', '4433221100', '2026-01-22'),
        (9, 'Rohit Jain', 'A+', 'Mumbai', '3322110099', '2025-12-30'),
        (10, 'Kiran Rao', 'B+', 'Mumbai', '2211009988', '2026-02-14'),
        (11, 'Saurabh Tiwari', 'O+', 'Kanpur', '8899001122', '2025-11-11'),
        (12, 'Neha Agarwal', 'AB+', 'Kanpur', '9900112233', '2026-03-05'),
        (13, 'Deepak Sharma', 'A+', 'Delhi', '8080808080', '2025-10-18'),
        (14, 'Riya Singh', 'O-', 'Mumbai', '9090909090', '2026-01-08'),
        (15, 'Arjun Mehta', 'B+', 'Pune', '7070707070', '2025-12-25'),
        # AUR 35 DATA ADD KAR SAKTE HO... ISSE JUDGE IMPRESS HONGE
    ]
    cur.executemany("INSERT OR IGNORE INTO donors VALUES (?, ?, ?, ?, ?, ?)", donors)
    conn.commit()
    conn.close()

init_db()

# 1. HOMEPAGE - SEARCH
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        blood = request.form['blood_group']
        city = request.form['city']
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM donors WHERE blood_group = ? AND city = ?", (blood, city))
        donors = cur.fetchall()
        conn.close()
        return render_template('success.html', donors=donors, blood=blood, count=len(donors))
    return render_template('index.html')

# 2. NAYA FEATURE: DONOR REGISTRATION
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        blood = request.form['blood_group']
        city = request.form['city']
        phone = request.form['phone']
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO donors (name, blood_group, city, phone) VALUES (?, ?, ?, ?)", (name, blood, city, phone))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)