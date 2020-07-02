from datetime import datetime
from flask_login import UserMixin
from HSM import db


class PatientStatus(db.Model):
    __tablename__='PatientStatus'
    SSN_ID= db.Column(db.Integer, primary_key=True)
    PatientID= db.Column(db.Integer,unique=True)
    Name= db.Column(db.String(20),nullable=False)
    Age= db.Column(db.Integer)
    DOJ= db.Column(db.String(20))
    BedType=db.Column(db.String(20))
    Address=db.Column(db.String(30))
    State=db.Column(db.String(20))
    City=db.Column(db.String(20))
    Status=db.Column(db.String(20))
    def __repr__(self):
        return f"PatientStatus('{self.SSN_ID}','{self.PatientID}','{self.Name}','{self.Age}','{self.DOJ}','{self.BedType}','{self.Address}','{self.State}','{self.City}','{self.Status}')"

class MedicineTable1(db.Model):
    __tablename__='MedicineTable1'
    ID=db.Column(db.Integer,primary_key=True,autoincrement=True)
    PatientID = db.Column(db.Integer)
    MedicineID = db.Column(db.Integer)
    Quantity = db.Column(db.Integer)
    

    def __repr__(self):
        return f"MachineTable1('{self.PatientID}', '{self.MedicineID}', '{self.Quantity}')"

class MedicineTable2(db.Model):
    __tablename__='MedicineTable2'
    MedicineID=db.Column(db.Integer,primary_key=True)
    MedName=db.Column(db.String(50),nullable=False)
    AvlQty=db.Column(db.Integer)
    Rate=db.Column(db.Float)
    def __repr__(self):
        return f"MachineTable2('{self.MedicineID}', '{self.MedName}', '{self.AvlQty}','{self.Rate}')"

class DiagnosticsTable1(db.Model):
    __tablename__='DiagnosticsTable1'
    ID=db.Column(db.Integer,primary_key=True,autoincrement=True)
    PatientID = db.Column(db.Integer,nullable=False)
    TestID=db.Column(db.Integer)
    def __repr__(self):
        return f"DiagnosticsTable1('{self.PatientID}', '{self.TestID}')"


class DiagnosticsTable2(db.Model):
    __tablename__='DiagnosticsTable2'
    TestID=db.Column(db.Integer,primary_key=True)
    TestName=db.Column(db.String(50),nullable=False)
    TestCharge=db.Column(db.Float)
    def __repr__(self):
        return f"DiagnosticsTable2('{self.TestID}', '{self.TestName}','{self.TestCharge}')"
class userstore(UserMixin, db.Model):
    __tablename__='userstore'
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"userstore('{self.username}', '{self.password}', '{self.timestamp}')"
    def is_authenticated(self):
        return True

    def is_active(self):
        return True
    def get_id(self):
        return str(self.username)
