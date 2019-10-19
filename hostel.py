# IMPORT
from flask import Flask, render_template , request , redirect, url_for, session, flash
from functools import wraps
from datetime import timedelta
import os
from flask.ext.sqlalchemy import SQLAlchemy


#Application config
app=Flask(__name__)
app.secret_key = "BATMAN"
app.permanent_session_lifetime = timedelta(minutes=20)
app.config['uploaded_files'] = "C:\\Users\\kaustubh\\Documents\\Dr.Who\\AdminLTE-2.4.18 (2)\\uploaded"
app.config['allowed_ext'] = "PDF"
app.config['SQLALCHEMY_DATABASE_URL']


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
        uploaded_file =  request.files["fileupload"]
        if uploaded_file.filename== "":
            flash("Please select a file")
        else:
            print(uploaded_file.filename)
            if not checkext(uploaded_file.filename):
                flash("Please upload only PDF file")
                #return render_template('registration.html', error= error)
            else:
                uploaded_file.save(os.path.join(app.config['uploaded_files'], "myname"))
                return redirect(url_for('home'))
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
    return render_template('view_hostel.html')

@app.route('/view-mess')
@login_required
def view_mess():
    return render_template('view_mess.html')


if __name__=="__main__":
    app.run(debug=True)
