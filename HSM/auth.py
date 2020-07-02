
from datetime import datetime
import math, random,os
import pdfkit
from flask import Blueprint, render_template, redirect, url_for, request, flash,session,make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required
from HSM.models import userstore,PatientStatus, MedicineTable1,MedicineTable2,DiagnosticsTable1,DiagnosticsTable2
from HSM import db, create_app

auth = Blueprint('auth', __name__)



################################                LOGIN               ##########################################################
@auth.route("/")
@auth.route("/login")
def login():
    return render_template('login.html')


@auth.route('/')
@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = userstore.query.filter_by(username=username).first()
    if user==None:
        flash("Invalid user")
        return redirect(url_for('auth.login'))
    #print(user)
    if user and user.password!=password:
        flash("Please check your login details and try again.")
        return redirect(url_for('auth.login'))

    login_user(user)
    if user and user.password==password:
        session['user_id'] = user.username
        session['username'] = user.username
        flash("Logged in Successfully!!!")
        return redirect(url_for('auth.Home'))


####################################################     HOME        #############################################
@auth.route('/home')
@login_required
def Home():
    if session['username']=="REG1234567":
        a=userstore.query.filter_by(username=session['username']).first()
        a.timestamp=datetime.now()
        db.session.commit()

        return render_template('home.html')
    if session['username']=="PMC1234567":
        a=userstore.query.filter_by(username=session['username']).first()
        a.timestamp=datetime.now()
        db.session.commit()
        return render_template('home.html')
    if session['username']=="DIG1234567":
        a=userstore.query.filter_by(username=session['username']).first()
        a.timestamp=datetime.now()
        db.session.commit()
        return render_template('home.html')

####################################################     REGISTER PATIENT        #############################################
@auth.route('/register_patient')
@login_required
def register_patient():
    return render_template('register_patient.html')
@auth.route('/register_patient', methods=['POST'])
def register_patient_post():
    ssnid = request.form.get('SSNID')
    name = request.form.get('name')
    age = request.form.get('age')
    bed=request.form.get('type')
    Address=request.form.get('add')
    state=request.form.get('state')
    city=request.form.get('city')
    #digits = "123456789"
    p_id =""
    for i in range(9) : 
        p_id =random.randrange(100000000,999999999)
        int("1"+str(p_id))
    p_id=int(p_id)
    patient = PatientStatus.query.filter_by(SSN_ID=ssnid).first()
    date=str(request.form.get('date'))
    if patient:
        flash("Patient already exist")
        return redirect(url_for('auth.register_patient'))

    
    new_user = PatientStatus(SSN_ID=ssnid,PatientID=p_id, Name=name, Age=age,DOJ=date,BedType=bed, Address=Address, State=state,City=city,Status='Active')
    #new_user.save()
    db.session.add(new_user)
    db.session.commit()
    flash("Patient Registration initiated successfully")

    return render_template('register_patient.html', title='Patient Registration')



####################################################     UPDATE PATIENT         ##############################################
@auth.route("/updatepatient")
@login_required
def update_patient2():
    return render_template("update_patient.html")

@auth.route("/updatepatient", methods=['GET', 'POST'])
@login_required
def update_patient():
    p_id=request.form.get('SSNID')
    newpatientname = request.form.get('name')
    newage = request.form.get('age')
    newaddress = request.form.get('add')
    d=request.form.get('date')
    #print(s_id)
    if p_id:
        u=PatientStatus.query.filter_by(PatientID=p_id).first()
        if u:
            resp=make_response(render_template("update_patient.html",u=u))
            resp.set_cookie('obj3',p_id)
            return resp
        if u==None:
            flash("Patient Not found")
            return render_template('update_patient.html')
    if newpatientname or newage or newaddress or d:
        a=request.cookies.get('obj3')
        c=PatientStatus.query.filter_by(PatientID=a).first()
        
        if newpatientname:
            c.Name=newpatientname
            db.session.commit()
        if newage:
            c.Age=newage
            db.session.commit()
        if newaddress:
            c.Address=newaddress
            db.session.commit()
        if d:
            c.DOJ=d
            db.session.commit()
        flash("Update Successfully initiated")
        return render_template("update_patient.html")
    flash("Nothing entered to update")
    return render_template("update_patient.html")


####################################################    DELETE PATIENT             ###############################################
@auth.route("/deletepatient")
@login_required
def delete_patient2():
    return render_template("delete_patient.html")
@auth.route("/deletepatient", methods=['GET', 'POST'])
def delete_patient():
    p_id = request.form.get('SSNID')
    h_id=request.form.get('hid')
    if p_id:
        u=PatientStatus.query.filter_by(PatientID=p_id).first()
        if u:
            return render_template("delete_patient.html",u=u)
        if u==None:
            flash("Patient Not found")
            return render_template('delete_patient.html')
    if h_id:
        print(h_id)
        q=PatientStatus.query.filter_by(SSN_ID=h_id).delete()
        db.session.commit()
        
        print(q)
        if q:
            flash("Delete Successfully initiated")
            return render_template('delete_patient.html')
        if q==0:
            flash("Invalid Patient")
            return render_template('delete_patient.html')
    if h_id==None:
        flash("Invalid Patient")
        return render_template('delete_patient.html')


        
####################################################    VIEW PATIENT            ###############################################
@auth.route("/viewpatient")
@login_required
def view_patient():
    d=PatientStatus.query.order_by(PatientStatus.SSN_ID).all()
    return render_template("view_patient.html",d=d)





####################################################     SEARCH PATIENT          ##############################################
@auth.route("/patientsearch")
@login_required
def search_patient2():
    return render_template('patient_search.html')
@auth.route("/patientsearch", methods=['GET', 'POST'])
def search_patient():
    c=None
    ssn_id = request.form.get('SSNID')
    if ssn_id:
        c=PatientStatus.query.filter_by(PatientID=ssn_id).first()
        if c:
            flash("Patient Found")
            return render_template("patient_search.html",c=c)
        

    
    flash("Patient not found")
    return render_template('patient_search.html')



###################################################      ISSUE MEDICINE          #############################################
@auth.route("/getpatient")
@login_required
def issue_medicine():
    return render_template('get_patient.html')


@auth.route("/getpatient", methods=['GET', 'POST'])
def get_patient():
    c=None
    r=[]
    r2=[]
    r3=[]
    ssn_id = request.form.get('SSNID')
    if ssn_id:
        c=PatientStatus.query.filter_by(PatientID=ssn_id).first()
        
        if c:
            d=MedicineTable1.query.filter_by(PatientID=ssn_id).all()
            
            if d:
                #flash("Patient Found with medicine Information")
                for i in d:
                    r2.append(i.MedicineID)
                    r3.append(i.Quantity)
                r2=list(set(r2))
                l=len(r3)-1
                print(r2,r3)

                for i in r2:
                    mid=i
                    p=MedicineTable2.query.filter_by(MedicineID=mid).first()
                    if p:
                    #rate=float(p.Rate)
                        r.append(p)
                print(d,r,c)
                
                resp=make_response(render_template("get_patient.html",c=c,d=d,r=r,r3=r3,l=l))
                resp.set_cookie('obj5',ssn_id)
                return resp
                
            #flash("Patient Found with No Medicine information")
            resp=make_response(render_template("get_patient.html",c=c))
            resp.set_cookie('obj5',ssn_id)
            return resp


        
        flash("Patient not found")
        return render_template('get_patient.html')

@auth.route("/issuemedicine",methods=['GET','POST'])
@login_required
def issue_medicine3():
    name=request.form.get('name')
    qty=request.form.get('qty')
    hid=request.form.get('h1')
    if name:
        k=MedicineTable2.query.filter_by(MedName=name).first()
        if k:
            if k.AvlQty>0:
                flash("Medicine Available")
                return render_template("issue_medicine.html",k=k)
            else:
                flash("Medicine Not Available")
                return render_template("issue_medicine.html")
        if k==None:
            flash("Invalid Medicine Name")
            return render_template('issue_medicine.html')
    elif qty and hid:
        k2=MedicineTable2.query.filter_by(MedicineID=hid).first()
        print(k2)
        if k2:
            a=request.cookies.get('obj5')
            print(a)
            if k2.AvlQty<int(qty):
                flash("Medicine Out of stuck!!! Required medicine quantity is more than Available")
                return render_template('issue_medicine.html')
            k2.AvlQty=int(k2.AvlQty)-int(qty)
            db.session.commit()
            mid=k2.MedicineID
            new=MedicineTable1(MedicineID=mid,PatientID=a,Quantity=qty)
            db.session.add(new)
            db.session.commit()
            flash("Medicine Issued Successfully")
            return render_template('issue_medicine.html')


    return render_template('issue_medicine.html')


####################################################     ADD DIAGNOSTICS         ##############################################

@auth.route("/getpatient2")
@login_required
def add_diagnostics():
    return render_template('get_patient2.html')


@auth.route("/getpatient2", methods=['GET', 'POST'])
def get_patient2():
    c=None
    r=[]
    ssn_id = request.form.get('SSNID')
    if ssn_id:
        c=PatientStatus.query.filter_by(PatientID=ssn_id).first()
        
        if c:
            d=DiagnosticsTable1.query.filter_by(PatientID=ssn_id).all()
            
            if d:
                for i in d:
                    mid=i.TestID
                    p=DiagnosticsTable2.query.filter_by(TestID=mid).first()
                    if p:
                        r.append(p)
                print(d,r,c)
                resp=make_response(render_template("get_patient2.html",c=c,d=d,r=r))
                resp.set_cookie('obj6',ssn_id)
                return resp
                
            resp=make_response(render_template("get_patient2.html",c=c))
            resp.set_cookie('obj6',ssn_id)
            return resp


        
        flash("Patient not found")
        return render_template('get_patient2.html')

@auth.route("/adddiagnostics",methods=['GET','POST'])
@login_required
def add_diagnostics3():
    name=request.form.get('name')
    #qty=request.form.get('qty')
    hid=request.form.get('h1')
    if name:
        k=DiagnosticsTable2.query.filter_by(TestName=name).first()
        if k:
            if k.TestCharge:
                flash("Test Available")
                return render_template("add_diagnostics.html",k=k)
            else:
                flash("Diagnostics Not Available")
                return render_template("add_diagnostics.html",k=k)
        if k==None:
            flash("Invalid Diagnostics Name")
            return render_template('add_diagnostics.html')
    elif hid:
        k2=DiagnosticsTable2.query.filter_by(TestID=hid).first()
        if k2:
            a=request.cookies.get('obj6')
            mid=k2.TestID
            new=DiagnosticsTable1(TestID=mid,PatientID=a)
            db.session.add(new)
            db.session.commit()
            flash("Diagnostics added Successfully")
            return render_template('add_diagnostics.html')
    return render_template('add_diagnostics.html')

###################################################     PATIENT BILLING         ##############################################
@auth.route("/getpatient3")
@login_required
def billing_patient2():
    return render_template('get_patient3.html')


@auth.route("/getpatient3", methods=['GET', 'POST'])
def get_patient3():
    c=None
    r=[]
    r2=[]
    ssn_id = request.form.get('SSNID')
    hid=request.form.get('h5')
    if ssn_id:
        c=PatientStatus.query.filter_by(PatientID=ssn_id).first()
        
        if c:
            dcharge=0
            mcharge=0
            d=DiagnosticsTable1.query.filter_by(PatientID=ssn_id).all()
            k=MedicineTable1.query.filter_by(PatientID=ssn_id).all()
            gt=0
            
            if d or k:
                if d:

                    
                    for i in d:
                    
                        mid=i.TestID
                        p=DiagnosticsTable2.query.filter_by(TestID=mid).first()
                        if p:
                            dcharge=dcharge+p.TestCharge
                            r.append(p)
                if k:
                   
                    for j in k:
                        mid2=j.MedicineID
                        p2=MedicineTable2.query.filter_by(MedicineID=mid2).first()
                        if p2:
                            mcharge=mcharge+(p2.Rate*j.Quantity)
                            r2.append(p2)
                r2=list(set(r2))
                print(d,r,c)
                from datetime import date
                date2=str(datetime.today().strftime('%Y-%m-%d'))
                DOJ=c.DOJ.split('-')
                print(DOJ)
                d5=DOJ[2]
                y1=DOJ[0]
                m1=DOJ[1]
                d0=date(int(y1),int(m1),int(d5))
                d6=date2.split('-')
                d7=d6[2]
                y2=d6[0]
                m2=d6[1]
                d10=date(int(y2),int(m2),int(d7))
                print(d6)
                Nday=d10-d0
                print(Nday)
                if c.BedType=="General Ward":
                    rbill=2000 * Nday
                elif c.BedType=="Semi sharing":
                    rbill=4000 * Nday
                elif c.BedType=="Single room":
                    rbill=8000* Nday
            
                print(str(rbill))

                rbill=str(rbill)
                rbill=rbill.split()
                gt=int(rbill[0])+dcharge+mcharge
                resp=make_response(render_template("get_patient3.html",c=c,d=d,r=r,k=k,r2=r2,date2=date2,Nday=Nday,rbill=rbill[0],dcharge=dcharge,mcharge=mcharge,gt=gt))
                response.set_cookie('obj7',ssn_id)
                return response
            
            from datetime import date
            date2=str(datetime.today().strftime('%Y-%m-%d'))
            DOJ=c.DOJ.split('-')
            print(DOJ)
            d5=DOJ[2]
            y1=DOJ[0]
            m1=DOJ[1]
            d0=date(int(y1),int(m1),int(d5))
            d6=date2.split('-')
            d7=d6[2]
            y2=d6[0]
            m2=d6[1]
            d10=date(int(y2),int(m2),int(d7))
            print(d6)
            Nday=d10-d0
            print(Nday)
            if c.BedType=="General Ward":
                rbill=2000 * Nday
            elif c.BedType=="Semi sharing":
                rbill=4000 * Nday
            elif c.BedType=="Single room":
                rbill=8000* Nday
            
            print(str(rbill))

            rbill=str(rbill)
            rbill=rbill.split()
            gt=int(rbill[0])+dcharge+mcharge

            resp=make_response(render_template("get_patient3.html",c=c,date2=date2,Nday=Nday,rbill=rbill[0]))
            
            resp.set_cookie('obj7',ssn_id)
            return resp


        
        flash("Patient not found")
        return render_template('get_patient3.html')
    if hid:
        k2=PatientStatus.query.filter_by(PatientID=hid).first()
        if k2.Status=="Discharged":
            flash("Patient Already Discharged")
            return render_template('home.html')
        k2.Status="Discharged"
        db.session.commit()
        flash("Patient Discharged Successfully")
        return render_template('home.html')






    
####################################################              LOG OUT                 ##############################################

@auth.route("/logout")
def logout():
    flash("Logged out Successfully!!!")
    return redirect(url_for('auth.login'))
