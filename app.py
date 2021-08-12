from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import test
import math as m
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///file.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Detections(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    glucose = db.Column(db.Integer,nullable=False)
    bp = db.Column(db.Integer,nullable=False)
    insulin = db.Column(db.Integer,nullable=False)
    bmi = db.Column(db.Float,nullable=False)
    age = db.Column(db.Integer,nullable=False)
    prob = db.Column(db.Integer,nullable=False)
    

    def __repr__(self) -> str:
        return f"{self.sno} - {self.age}"

@app.route("/",methods=['GET','POST'])
def detect():
    if request.method == "POST":
        glucose = int(request.form['glucose'])
        bp = int(request.form['bp'])
        insulin = int(request.form['insulin'])
        bmi = float(request.form['bmi'])
        age = int(request.form['age'])
        print(glucose,bp,insulin,bmi,age)
        prob = int(m.ceil((test.predict([[glucose,bp,insulin,bmi,age]])*100)))
        result = Detections(glucose=glucose,bp=bp,insulin=insulin,bmi=bmi,age=age,prob=prob)
        db.session.add(result)
        db.session.commit()
        return render_template('results.html',prob=prob)
    return render_template('detect.html')

@app.route("/detections")
def detections():
    p = Detections.query.all()
    return render_template('detections.html',p=p)

'''@app.route("/results")
def results():
    p = Detections.query.all()
    return render_template('detections.html',p=p)'''

if __name__ == "__main__":
    app.run(debug=True)