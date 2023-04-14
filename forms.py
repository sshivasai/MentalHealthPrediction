from wtforms import Form, StringField, DecimalField,SelectField, IntegerField, TextAreaField, PasswordField, validators

#form used on Register page
class RegisterForm(Form):
    name = StringField('Full Name', [validators.Length(min=1,max=50)])
    username = StringField('Username', [validators.Length(min=4,max=25)])
    age = IntegerField('Age')
    gender = SelectField('Gender', choices=[('Male','Male'),('Female','Female')])
    email = StringField('Email', [validators.Length(min=6,max=100)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')



class UpdateProfileForm(Form):
    age = IntegerField('Age',default=None)
    name = StringField('Full Name', [validators.Length(min=1,max=50)])
    email = StringField('Email', [validators.Length(min=6,max=50)],default=None)
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')],default=None)
    confirm = PasswordField('Confirm Password',default=None)
    family_history = StringField('Email', [validators.Length(min=6,max=50)],default=None)
    benefits = StringField('Email', [validators.Length(min=6,max=50)],default=None)
    care_options = StringField('Email', [validators.Length(min=6,max=50)],default=None)
    anonymity = StringField('Email', [validators.Length(min=6,max=50)],default=None)
    leave = StringField('Email', [validators.Length(min=6,max=50)],default=None)
    work_interfere = StringField('Email', [validators.Length(min=6,max=50)],default=None)

class PredictForm(Form):
    name = StringField('Full Name', [validators.Length(min=1,max=50)])
    age = IntegerField('Age',default=None)
    gender = SelectField('Gender', choices=[('Male','Male'),('Female','Female')])
    family_history = StringField('Email', [validators.Length(min=6,max=50)],default=None)
    benefits = StringField('Email', [validators.Length(min=6,max=50)],default=None)
    care_options = StringField('Email', [validators.Length(min=6,max=50)],default=None)
    anonymity = StringField('Email', [validators.Length(min=6,max=50)],default=None)
    leave = StringField('Email', [validators.Length(min=6,max=50)],default=None)
    work_interfere = StringField('Email', [validators.Length(min=6,max=50)],default=None)
