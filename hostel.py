# IMPORT
from flask import Flask, render_template , request , redirect, url_for, session, flash , g
from functools import wraps
from datetime import timedelta
import os
from flaskext.mysql import MySQL
#from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from models import LoginForm, student_main , selectstud
from wtforms.validators import InputRequired, Length


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
main_important= ['stud_id','fname','lname','father_name','mother_name','mobile_no','email','add1','add2','city','state','pincode','area_code','phone','par_mobile_no','bdate','pob','nationality','religion','gb','caste','sub_caste','aadhar','pan','gender',]
stud_father_fields = ['lname','father_name' ,'f_occupation','f_organization','f_qualification','f_office_addr','farea_code','father_phone','f_mobile_no','f_fax','f_email']
stud_mother_fields = ['lname','mother_name', 'm_occupation','m_organization','m_qualification','m_office_addr','marea_code','mother_phone','m_mobile_no','m_fax','m_email']
all_students_data = []
payment_form_fields = ['hostel_id','mess_id','hostel_type','mess_type','hostel_total_till_now','hostel_prev_date','mess_total_till_now','mess_prev_date']

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
    cur.execute(comd1, ( data['stud_id'],data['fname'],data['lname'],data['father_name'],data['mother_name'],data['mobile_no'],data['email'],data['add1'],data['add2'],data['city'],data['state'],int(data['pincode']),int(data['area_code']),data['phone'],data['par_mobile_no'],int(data['bdate'][5:7]),int(data['bdate'][8:]),int(data['bdate'][0:4]),data['pob'],data['nationality'],data['religion'],data['gb'],data['caste'],data['sub_caste'],data['aadhar'],data['pan'],data['gender']))
    conn.commit()
    cur.close()

    conn = mysql.connect()
    cur = conn.cursor()
    fdata['father_area_code'] = "022"
    print(fdata)
    comd2 = "INSERT INTO stud_father values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(comd2, (data['stud_id'],fdata['lname'],fdata['father_name'] ,fdata['f_occupation'],fdata['f_organization'],fdata['f_qualification'],fdata['f_office_addr'],fdata['farea_code'],fdata['father_phone'],fdata['f_mobile_no'],fdata['f_fax'],fdata['f_email']))
    conn.commit()
    cur.close()

    conn = mysql.connect()
    cur = conn.cursor()
    mdata['mother_area_code'] = "022"
    comd3 = "INSERT INTO stud_mother values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(comd3, (data['stud_id'],mdata['lname'],mdata['mother_name'] ,mdata['m_occupation'],mdata['m_organization'],mdata['m_qualification'],mdata['m_office_addr'],str(mdata['marea_code']),mdata['mother_phone'],mdata['m_mobile_no'],mdata['m_fax'],mdata['m_email']))
    conn.commit()
    cur.close()
    all_students_data.append(dict(student = data, father = fdata, mother = mdata))
    
def db_conn(data):
    conn = mysql.connect()
    cur = conn.cursor()
    fdata['father_area_code'] = "022"
    print(fdata)
    comd2 = "INSERT INTO stud_father values(%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(comd2, (data['hostel_id'],data['mess_id'],data['hostel_type'],data['mess_type'],data['hostel_total_till_now'],data['hostel_prev_date'],data['mess_total_till_now'],data['mess_prev_date']))
    conn.commit()
    cur.close()


#Main Pages Of Website
@app.route('/', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST':
        error = form.errors
        print('uname is {}, password is {}'.format(form.username.data, form.password.data))
        if form.username.data != 'admin' or form.password.data != 'admin':
            error = " Invalid Credentials! Please Try again"
        else:
            session['logged_in']=True
            conn = mysql.connect()
            cur = conn.cursor()
            comd1 = "INSERT INTO logintest values(%s,%s)"
            cur.execute(comd1,(form.username.data, form.password.data))
            conn.commit()
            cur.close()
            print('uname is {}, password is {}'.format(form.username.data, form.password.data))
            return redirect(url_for('home'))
    return render_template('login.html',form = form, error=error)



@app.route('/registration', methods=['GET','POST'])
@login_required
def registration():
    form = student_main(request.form)
    print(request.form.values)
    #uploaded_file =  request.files["fileupload"]
    #print(uploaded_file.filename)
    error=""
    if request.method=="POST":
        form  = request.form
        stud_data={}
        for valuesa in main_important:
            stud_data[valuesa] = form.get(valuesa)
        print(stud_data)
        father_data={}        
        for valuesa in stud_father_fields:
            father_data[valuesa] = form.get(valuesa)
        print(father_data)
        mother_data = {}
        for valuesa in stud_mother_fields:
            mother_data[valuesa] = form.get(valuesa)
        print(mother_data)
        db_connector(stud_data, father_data, mother_data)
        return redirect(url_for('view_hostel'))  
        '''uploaded_file =  request.files["fileupload"]
        if not uploaded_file.filename== "":
            print(uploaded_file.filename)
            if not checkext(uploaded_file.filename):
                flash("Please upload only PDF file")
                return redirect(url_for('#'))
            else:
                myname = ((stud_data['fname'])+"_"+(stud_data['stud_id'])+".pdf")
                uploaded_file.save(os.path.join(app.config['uploaded_files'], myname))
                #db_connector(stud_data, father_data, mother_data)
                return render_template('view_hostel.html', data = stud_data)
        elif uploaded_file.filename== "":
            flash("Please upload PDF file")
            return redirect(url_for('registration'))'''
    return render_template('registration-copy.html', form = form)



@app.route('/student-payment', methods=['GET','POST'])
@login_required
def student_payment():
    error=""
    payment_data={}
    if request.method=="POST":
        form  = request.form
        for valuas in payment_form_fields:
            if form.get(valuas) =="":
                return redirect(url_for(student_payment))
            else:
                payment_data[valuas] = form.get(valuas)
        #db_conn(payment_data)
    return render_template('student_payment.html')




@app.route('/logout')
@login_required
def logout():
    flash("You have been logged out")
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/home', methods=['GET','POST'])
@login_required
def home():
    select_stud = selectstud(request.form)
    
    select_stud.stud_id.choices = [('vu4f1516043','vu4f1516043' ),('vu4f1516007','vu4f1516007')]
    if request.method == 'POST':
        id_selected = select_stud.stud_id.data
        print(id_selected) 
    #tes = "kaustubh"
    #if tes == 'kaustubh':
        return redirect(url_for('change_personal', id_selected = id_selected))
    return render_template('home.html', selectstud = select_stud)

@app.route('/view-hostel')
@login_required
def view_hostel():
    conn = mysql.connect()
    cur = conn.cursor()
    stu = int('043')
    comd = "select sm.fname, sm.lname ,pt.* , ch.mess_monthly, ch.hostel_yearly from charges as ch, pay_table as pt, student_main as sm where pt.stud_id= 'vu4f1516043'  and  sm.stud_id= 'vu4f1516043';"
    cur.execute(comd)# , int(stu))
    values = cur.fetchall()
    data={}
    for rows in values:
        data = dict(stud_id = rows[2], fname = rows[0], lname = rows[1], stud_mess_id= rows[3], payment_method_monthly= rows[4] , payment_till_now= rows[5] , prev_payment_amt = rows[6], prev_amt_date = rows[7], payment_start_date = rows[8], mess_monthly = rows[9], hostel_yearly = rows[10])
    conn.close()
    return render_template('view_hostel.html',data = data)


@app.route('/view-all')
@login_required
def view_all():
    data=[]
    conn = mysql.connect()
    cur = conn.cursor()
    comd = ' select stud_id from student_main'
    cur.execute(comd)
    all_ids = cur.fetchall()
    conn.close()
    for ids in all_ids:
        conn = mysql.connect()
        cur = conn.cursor()
        comd = "select sm.fname, sm.lname ,pt.* , ch.mess_monthly, ch.hostel_yearly from charges as ch, pay_table as pt, student_main as sm where pt.stud_id= 'vu4f1516043'  and  sm.stud_id=%s;"
        cur.execute(comd,ids)# , int(stu))
        values = cur.fetchall()
        print(values)
        for rows in values:
            data.append(dict(stud_id = rows[2], fname = rows[0], lname = rows[1], stud_mess_id= rows[3], payment_method_monthly= rows[4] , payment_till_now= rows[5] , prev_payment_amt = rows[6], prev_amt_date = rows[7], payment_start_date = rows[8], mess_monthly = rows[9], hostel_yearly = rows[10]))
        conn.close()
    return render_template('view_hostel.html', datas = data)


@app.route('/change-personal/<id_selected>')
@login_required
def change_personal(id_selected):
    conn = mysql.connect()
    cur = conn.cursor()
    comd = "select * from student_main left join stud_father on student_main.stud_id  = stud_father.stud_id left join stud_mother on student_main.stud_id = stud_mother.stud_id where student_main.stud_id = %s;"
    cur.execute(comd,id_selected)# , int(stu))
    values = cur.fetchall()
    print(values)
    stud_id = 
    fname = 
    lname = 
    father_name = 
    mother_name = 
    mobile_no = 
    email = 
    add1 = 
    add2 = 
    city = 
    state = 
    pincode = 
    area_code = 
    phone = 
    par_mobile_no = 
    bdate = 
    pob = 
    nationality = 
    religion = 
    gb = 
    caste = 
    sub_caste = 
    aadhar = 
    pan = 
    gender = 

    m_occupation = 
    m_organization = 
    m_qualification = 
    m_office_addr = 
    marea_code = 
    mother_phone = 
    m_fax = 
    m_mobile_no = 
    m_email = 
    
    f_occupation = 
    f_organization = 
    f_qualification = 
    f_office_addr = 
    farea_code = 
    father_phone = 
    f_fax = 
    f_mobile_no = 
    f_email = 

    college_addr = 
    xiiloc = 
    f_dom_maha = 
    current_year =
    percent_in_prev =
    annual_income = 
    admission_through = 
    return ("Cool!{}".format(id_selected))


@app.route('/view-mess')
@login_required
def view_mess():
    return render_template('view_mess.html')


if __name__=="__main__":
    app.run(debug=True)
