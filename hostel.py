# IMPORT
from flask import Flask, render_template , request , redirect, url_for, session, flash , g
from functools import wraps
from datetime import timedelta
import os
from flaskext.mysql import MySQL
#from flask_mysqldb import MySQL




#Application config
app=Flask(__name__)
app.secret_key = "BATMAN"
app.permanent_session_lifetime = timedelta(minutes=180)
app.config['uploaded_files'] = "C:\\Users\\kaustubh\\Documents\\Dr.Who\\AdminLTE-2.4.18 (2)\\uploaded"
app.config['allowed_ext'] = "PDF"

app.config['MYSQL_DATABASE_USER']='kaustubh'
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_PASSWORD']='12345'  
app.config['MYSQL_DATABASE_DB']='hostel'

mysql = MySQL()
mysql.init_app(app)
data=[]
main_important= ['stud_id','fname','lname','father_name','mother_name','mobile_no','email','add1','add2','city','state','pincode','area_code','phone','par_mobile_no','date','POB','nationality','religion','gb','caste','sub_caste','aadhar','pan','gender',]
stud_father_fields = ['lname','father_name' ,'father_present_designation','father_organization','father_qualification','father_office_address','father_area_code','father_phone','father_mobile_no','father_fax','father_email']
stud_mother_fields = ['lname','mother_name', 'mother_present_designation','mother_organization','mother_qualification','mother_office_address','mother_area_code','mother_phone','mother_mobile_no','mother_fax','mother_email']
all_students_data = []


#Other Functions
def checkext(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".",1)[1]
    print(ext)
    if ext.upper() == app.config['allowed_ext']:
        return True
    else:
        return False

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You have to log in first! ")
            return redirect(url_for('login'))
    return wrap


def db_connector(data,fdata,mdata):
    print("")
    conn = mysql.connect()
    cur = conn.cursor()
    comd1 = "INSERT INTO student_main values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(comd1, ( data['stud_id'],data['fname'],data['lname'],data['father_name'],data['mother_name'],data['mobile_no'],data['email'],data['add1'],data['add2'],data['city'],data['state'],int(data['pincode']),int(data['area_code']),data['phone'],data['par_mobile_no'],int(data['date'][5:7]),int(data['date'][8:]),int(data['date'][0:4]),data['POB'],data['nationality'],data['religion'],data['gb'],data['caste'],data['sub_caste'],data['aadhar'],data['pan'],data['gender']))
    conn.commit()
    cur.close()

    conn = mysql.connect()
    cur = conn.cursor()
    fdata['father_area_code'] = "022"
    print(fdata)
    comd2 = "INSERT INTO stud_father values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(comd2, (data['stud_id'],fdata['lname'],fdata['father_name'] ,fdata['father_present_designation'],fdata['father_organization'],fdata['father_qualification'],fdata['father_office_address'],fdata['father_area_code'],fdata['father_phone'],fdata['father_mobile_no'],fdata['father_fax'],fdata['father_email']))
    conn.commit()
    cur.close()

    conn = mysql.connect()
    cur = conn.cursor()
    mdata['mother_area_code'] = "022"
    comd3 = "INSERT INTO stud_mother values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(comd3, (data['stud_id'],mdata['lname'],mdata['mother_name'] ,mdata['mother_present_designation'],mdata['mother_organization'],mdata['mother_qualification'],mdata['mother_office_address'],str(mdata['mother_area_code']),mdata['mother_phone'],mdata['mother_mobile_no'],mdata['mother_fax'],mdata['mother_email']))
    conn.commit()
    cur.close()
    

    all_students_data.append(dict(student = data, father = fdata, mother = mdata))
    '''
    username = data[0]
    password = data[1]
    print(username)
    print(password)
    a=3
    comd = 'INSERT INTO trial(id,user,password) values(%s,%s,%s)'
    cur.execute(comd , (str(a) ,str(username), str(password)))
    conn.commit()
    #mysql.connection.commit()
    cur.close()
    '''

    #for x in range(len(main_important)
    #stud_data[main_important[x]] = form[x]
    #print(stud_data)

#Main Pages Of Website
@app.route('/', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = " Invalid Credentials! Please Try again"
        else:
            session['logged_in']=True
            flash("Session Expired!!")
            return redirect(url_for('home'))
    return render_template('login.html', error=error)



@app.route('/registration', methods=['GET','POST'])
@login_required
def registration():
    error=""
    if request.method=="POST":
        form  = request.form
        stud_data={}
        for valuesa in main_important:
            if form.get(valuesa) =="":
                flash("Please Enter all details")
                #return redirect(url_for('registration'))
            else:
                stud_data[valuesa] = form.get(valuesa)
        father_data={}        
        for valuesa in stud_father_fields:
            father_data[valuesa] = form.get(valuesa)
            if form.get(valuesa) =="":
                flash("Please Enter all details")
                #return redirect(url_for('registration'))
            else:
                flash("nothing wrong")
                #father_data[valuesa] = form.get(valuesa)
        
        print(father_data)
        mother_data = {}
        for valuesa in stud_mother_fields:
            mother_data[valuesa] = form.get(valuesa)
            if form.get(valuesa) =="":
                flash("Please Enter all details")
                #return redirect(url_for('registration'))
            else:
                flash("Nothing wrong")
        uploaded_file =  request.files["fileupload"]
        if not uploaded_file.filename== "":
            print(uploaded_file.filename)
            if not checkext(uploaded_file.filename):
                flash("Please upload only PDF file")
                return redirect(url_for('#'))
            else:
                myname = ((stud_data['fname'])+"_"+(stud_data['stud_id'])+".pdf")
                uploaded_file.save(os.path.join(app.config['uploaded_files'], myname))
                db_connector(stud_data, father_data, mother_data)
                return render_template('view_hostel.html', data = stud_data)
        elif uploaded_file.filename== "":
            flash("Please upload PDF file")
            return redirect(url_for('registration'))
    return render_template('registration.html')



@app.route('/logout')
@login_required
def logout():
    flash("You have been logged out")
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/view-hostel')
@login_required
def view_hostel():
    conn = mysql.connect()
    cur = conn.cursor()
    stu = int('043')
    comd = 'select h.stud_id, h.name, h.surname, h.college_name, s.mobile_no, p.stud_mess_id, p.payment_monthly, p.payment_till_now, p.last_payment_amt, p.last_payment_date from host_stud as h , stud_pers as s, paid as p where h.stud_id =043;'
    cur.execute(comd)# , int(stu))
    values = cur.fetchall()
    data=[]
    for row in values:
        data.append(dict(stud_id = row[0], name = row[1], surname= row[2], college_name = row[3], mobile_number = row[4], stud_mess_id = row[5], Monthly = ("yes" if row[6] else "no"), paid_till_now = row[7], last_payment_amt = row[8], last_payment_date = row[9] , next_payment_date = ""))
    conn.close()
    return render_template('view_hostel.html',data = data)

@app.route('/view-mess')
@login_required
def view_mess():
    return render_template('view_mess.html')


if __name__=="__main__":
    app.run(debug=True)
