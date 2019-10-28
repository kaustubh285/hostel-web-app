from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , TextAreaField, IntegerField, SelectField , FloatField , FileField
from wtforms.validators import InputRequired, Length
from wtforms.fields.html5 import DateField 
from flask_wtf.file import FileField 

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('Please enter username'), Length(min = 4, max = 7, message="WTF bro!!")])
    password = PasswordField('password')


class student_main(FlaskForm):
    stud_id = StringField('stud_id', validators=[InputRequired()])
    fname = StringField('fname', validators=[InputRequired()])
    lname = StringField('lname', validators=[InputRequired()])
    father_name = StringField('father_name', validators=[InputRequired()])
    mother_name = StringField('mother_name', validators=[InputRequired()])
    mobile_no = StringField('mobile', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired()])
    add1 = TextAreaField('add1', validators=[InputRequired()])
    add2 = TextAreaField('add2', validators=[InputRequired()])
    city = StringField('city', validators=[InputRequired()])
    state = StringField('state', validators=[InputRequired()])
    pincode = IntegerField('pincode', validators=[InputRequired()])
    area_code = IntegerField('area', validators=[InputRequired()])
    phone = StringField('phone', validators=[InputRequired()])
    par_mobile_no = StringField('par_mobile_no', validators=[InputRequired()])
    bdate = DateField('bday', validators=[InputRequired()])
    pob = StringField('pob', validators=[InputRequired()])
    nationality = StringField('nationality', validators=[InputRequired()])
    religion = StringField('religion', validators=[InputRequired()])
    gb = StringField('gb', validators=[InputRequired()])
    caste = StringField('caste', validators=[InputRequired()])
    sub_caste = StringField('sub_caste', validators=[InputRequired()])
    aadhar = StringField('aadhar', validators=[InputRequired()])
    pan = StringField('pan', validators=[InputRequired()])
    gender = StringField('gender')

    m_occupation = StringField('mobile', validators=[InputRequired()])
    m_organization = StringField('email', validators=[InputRequired()])
    m_qualification = StringField('city', validators=[InputRequired()])
    m_office_addr = StringField('state', validators=[InputRequired()])
    marea_code = IntegerField('pincode', validators=[InputRequired()])
    mother_phone = IntegerField('area', validators=[InputRequired()])
    m_fax = StringField('phone', validators=[InputRequired()])
    m_mobile_no = StringField('par_mobile_no', validators=[InputRequired()])
    m_email = StringField('par_mobile_no', validators=[InputRequired()])
    
    f_occupation = StringField('mobile', validators=[InputRequired()])
    f_organization = StringField('email', validators=[InputRequired()])
    f_qualification = StringField('city', validators=[InputRequired()])
    f_office_addr = StringField('state', validators=[InputRequired()])
    farea_code = IntegerField('pincode', validators=[InputRequired()])
    father_phone = IntegerField('area', validators=[InputRequired()])
    f_fax = StringField('phone', validators=[InputRequired()])
    f_mobile_no = StringField('par_mobile_no', validators=[InputRequired()])
    f_email = StringField('par_mobile_no', validators=[InputRequired()])

    college_addr = TextAreaField('add1', validators=[InputRequired()])
    xiiloc = StringField('xiiloc')
    f_dom_maha = StringField('f_dom_maha')
    current_year = IntegerField('current_year')
    percent_in_prev = FloatField('percent_in_prev')
    annual_income = FloatField('annual_income')
    admission_through = StringField('ad_through')
    #file_upload = FileField('file_upload', FileNotFoundError('dont know!!!'))

class selectstud(FlaskForm):
    stud_id = SelectField('Programming Language')