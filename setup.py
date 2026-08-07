import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS hospitals''')
c.execute('''CREATE TABLE hospitals (id TEXT, name TEXT, city TEXT, contact TEXT, blood_data TEXT)''')
c.execute("INSERT INTO hospitals VALUES ('H9', 'District Hospital Lakhimpur', 'Lakhimpur', '05231-234567', 'A+:5, B+:8, O+:10, O-:2')")
c.execute("INSERT INTO hospitals VALUES ('H10', 'Ambalika Hospital Lakhimpur', 'Lakhimpur', '05231-987654', 'A+:12, B+:2, O+:15, O-:1')")

c.execute('''DROP TABLE IF EXISTS donors''')
c.execute('''CREATE TABLE donors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, mobile TEXT, blood_group TEXT, city TEXT)''')

c.execute('''DROP TABLE IF EXISTS requests''')
c.execute('''CREATE TABLE requests (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_name TEXT, blood_group TEXT, hospital TEXT, city TEXT, status TEXT)''')

conn.commit()
conn.close()
print("Database Ready with 3 Tables!")