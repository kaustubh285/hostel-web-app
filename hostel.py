from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/view-hostel')
def view_hostel():
    return render_template('view_hostel.html')

@app.route('/view-mess')
def view_mess():
    return render_template('view_mess.html')


if __name__=="__main__":
    app.run(debug=True)
