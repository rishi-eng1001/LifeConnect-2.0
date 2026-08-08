from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

class HospitalBlood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_name = db.Column(db.String(100), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    quantity_ml = db.Column(db.Integer, nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        d = Donor(name=request.form['name'], blood_group=request.form['blood_group'], city=request.form['city'], phone=request.form['phone'])
        db.session.add(d)
        db.session.commit()
        return "Donor Registered! <a href='/'>Home</a>"
    return render_template('register.html')

@app.route('/find', methods=['GET', 'POST'])
def find():
    donors = []
    msg = ""
    if request.method == 'POST':
        donors = Donor.query.filter_by(blood_group=request.form['blood_group'], city=request.form['city']).all()
        if len(donors) == 0:
            msg = "Doner not found"
    return render_template('donor_search.html', donors=donors, msg=msg)

@app.route('/addfake')
def addfake():
    names = ["Amit Kumar","Ravi Singh","Priya Sharma","Sonia Gupta","Anjali Verma","Pooja Yadav","Sanjay Patel","Kiran Mishra","Rohit Jaiswal","Neha Singh"]
    cities = ["Motipur","Lucknow","Delhi","Mumbai","Patna","Kanpur","Varanasi","Gaya","Muzaffarpur","Gorakhpur"]
    blood = ["A+","A-","B+","B-","O+","O-","AB+","AB-"]
    for i in range(500):
        d = Donor(name=random.choice(names)+" "+str(i+1), blood_group=random.choice(blood), city=random.choice(cities), phone="9"+str(random.randint(10000000,99999999)))
        db.session.add(d)
    db.session.commit()
    return "500 Fake Donors Added! <a href='/find'>Check Here</a>"

@app.route('/addhospitaldata')
def addhospitaldata():
    hospitals = ["AIIMS Delhi","SGPGI Lucknow","PMCH Patna","KGMU Lucknow","RML Hospital Delhi"]
    blood = ["A+","A-","B+","B-","O+","O-","AB+","AB-"]
    cities = ["Delhi","Lucknow","Patna","Motipur"]
    for h in hospitals:
        for b in blood:
            for c in cities:
                db.session.add(HospitalBlood(hospital_name=h, blood_group=b, city=c, quantity_ml=random.randint(500, 10000)))
    db.session.commit()
    return "Hospital Data Added! <a href='/hospital-stock'>Check Stock</a>"

@app.route('/hospital-stock', methods=['GET', 'POST'])
def hospital_stock():
    results = []
    if request.method == 'POST':
        results = HospitalBlood.query.filter_by(blood_group=request.form['blood'], city=request.form['city']).all()
    return render_template('hospital_stock.html', results=results)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)