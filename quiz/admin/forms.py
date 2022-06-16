from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, validators, PasswordField,SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed




class SubjectForm(FlaskForm):
    subject_name = StringField('Subject Name ', validators=[DataRequired(),  Length(min=6, max=25)])
    submit  = SubmitField('Submit',  validators=[DataRequired()])


class QuestionForm(FlaskForm):
    question = StringField('Question ', validators=[DataRequired()])
    select_question_level = SelectField('Question Level ', coerce=int, choices=[('0', 'Easy'), ('1', 'Medium'), ('2', 'Hard')])
    select_subject = SelectField('Select Subject ', coerce=int, choices=[('1', 'No Subject ')])

    option1 = StringField('Option 1  ', validators=[DataRequired()])
    option2 = StringField('Option 2  ', validators=[DataRequired()])
    option3 = StringField('Option 3  ', validators=[DataRequired()])
    option4 = StringField('Option 4  ', validators=[DataRequired()])
    answer = StringField('Answer ', validators=[DataRequired()])

    submit  = SubmitField('Submit',  validators=[DataRequired()])

