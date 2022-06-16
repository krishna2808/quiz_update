from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegistraionForm(FlaskForm):

    user_name = StringField('Username', validators=[DataRequired() , Length(min=2, max=20)])
    mobile_number = StringField('Mobile Number',  validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password', validators=[DataRequired(),  Length(min=5, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired() , EqualTo('password', message='Passwords must match'),  Length(min=5, max=10)])
    
    submit  = SubmitField('Submit')

    
    def __repr__(self):
        return '<Username %r>' % self.user_name


class LoginForm(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired() , Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(),  Length(min=5, max=10)])
    submit  = SubmitField('Submit')



