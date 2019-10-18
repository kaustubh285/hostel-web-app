from flask import Flask, render_template , request , redirect, url_for, session, flash
from functools import wraps

app=Flask(__name__)

app.secret_key = "BATMAN"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You have to log in first! ")
            return redirect(url_for('login'))
    return wrap



@app.route('/', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = " Invalid Credentials! Please Try again"
        else:
            session['logged_in']=True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


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

@app.route('/registration')
@login_required
def registration():
    return render_template('registration.html')

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
