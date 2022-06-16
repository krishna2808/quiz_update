from contextlib import redirect_stderr
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, session,g
from quiz.users.forms import RegistraionForm, LoginForm
from quiz.models import * 
from quiz.config import Config
from quiz.hash import Hashing
from datetime import datetime
# import datetime

users = Blueprint('users', __name__)

@users.before_request
def before_request():
    g.user_name = None
    if 'user_name' in session:
        g.user_name = session['user_name']
         
@users.route('/user_dashboard')
def user_dashboard():
    'User Dashboard'
    if g.user_name: 
        return render_template('user_dashboard.html')
    return redirect('log_in')    


@users.route('/', methods = ['GET', 'POST'])
@users.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    'User Registration '
    form = RegistraionForm()
    session.pop('user_name', None)
    g.user_name = None
    if request.method == 'POST':   
       if form.validate_on_submit():
            user = Users.query.filter_by(user_name=form.user_name.data).first()
            if(user == None):
                hash_pass = Hashing()
                gen_hash_password = hash_pass.gen_hash(form.password.data)
                user = Users(user_name=form.user_name.data, mobile_number=form.mobile_number.data, password=gen_hash_password)
                db.session.add(user)
                db.session.commit()
               
                flash('Your account successfully created')
                return redirect(url_for('users.log_in'))
            else:
                flash('User Name is already exist')

       form.user_name.data  = ''
       form.password.data = ''
       form.mobile_number.data = ''    
       form.submit.data = ''
    return render_template('registration.html', form=form)



@users.route('/log_in', methods=['GET', 'POST'])
def log_in():
    'User login '
    form = LoginForm()
    session.pop('user_name', None)
    if request.method == 'POST':
        if form.validate_on_submit():
            # session.pop('user_name', None)
            hash_pass = Hashing()
            user = Users.query.filter_by(user_name=form.user_name.data).first()
            if user: 
                check_hash_password = hash_pass.check_hash(user.password, form.password.data)
                if check_hash_password: 
                    session['user_name'] = form.user_name.data 
                    if user.is_admin == 'True':
                        return redirect(url_for('admin.admin_dashboard'))
                    elif user.is_admin == 'False':
                        return redirect(url_for('users.user_dashboard'))  
                else:
                    flash('Enter valid password  ') 
                    return redirect(url_for('users.log_in'))                   
            flash('Enter valid username ')       

    return render_template('login.html', form=form)                

@users.route('/log_out')
def log_out():

    'User log Out '

    session["user_name"] = None 
    return redirect(url_for('users.log_in'))


@users.route('/choice_subject_and_question_level', methods = ['POST', 'GET'])
def choice_subject_and_question_level():

    'User can choice question level as well as subject.'

    if g.user_name: 
        subjects = Subject.query.all()
        question = Question.query.all()
        if(len(subjects) !=0 and len(question) !=0 ):
            if request.method == 'POST':
                select_subject_name = request.form.get('subject_name')
                question_level = request.form.get('question_level')
                subject_name  = Subject.query.filter_by(subject_name=select_subject_name).first()
                subject_id = subject_name.id
                return redirect(url_for('users.quiz_start', question_level=question_level, subject_name=select_subject_name))
        else:
            return redirect(url_for('users.user_dashboard'))
        return render_template('question_level_and_subject.html', subjects=subjects) 
    return redirect(url_for('users.log_in'))              



# @app.route('/quiz_start', methods= ['GET', 'POST'])
@users.route('/quiz_start/<question_level>/<subject_name>', methods = ['POST', 'GET'])
def quiz_start(question_level, subject_name):

    'Quiz start and user can give question of answer'
    
    if g.user_name: 

        start_test_time = datetime.now()

        subject_name_filter  = Subject.query.filter_by(subject_name=subject_name).first()
        subject_id = subject_name_filter.id
        questions = Question.query.filter_by(subject_id=subject_id, question_level=question_level)

        if request.method == 'POST':
            end_test_time =  datetime.now()

            lst, score  = [], 0 
            for question in questions:
                choice_option = request.form[str(question.id)]
                if choice_option == question.answer and question_level == 'Easy':
                    score += 1  
                elif choice_option == question.answer and question_level == 'Medium':
                    score += 2
                elif choice_option == question.answer and question_level == 'Medium':
                    score += 3   
                lst.append(choice_option)
            user_id = Users.query.filter_by(user_name=g.user_name).first().id
            user_history = User_history(user_id=user_id, subject_id=subject_id, score=score, quiz_started_date = start_test_time, quiz_ended_date = end_test_time,  question_level=question_level ) 
            db.session.add(user_history)
            db.session.commit()
               
            return f'lst ***  {lst} score {score}'    


        return render_template('quiz_start.html', questions=questions, question_level=question_level, subject_name=subject_name)  
    return redirect(url_for('users.log_in'))    


@users.route('/history')
def history():
    # if g.user_name:
        user_id = Users.query.filter_by(user_name=g.user_name).first().id 
        history = User_history.query.filter_by(user_id=user_id).all()
        for i in history:
            print(i.user_id, i.subject_id, )
        print('user_id and user_history *********** ', history, user_id )
        subject_obj = Subject()
        return render_template('history.html', history=history, subject_obj=subject_obj)
        return 'page '

        

    # return redirect(url_for('log_in'))    