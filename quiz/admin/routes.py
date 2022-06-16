import imp
from pickletools import read_uint1
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, session,g
from quiz.users.forms import RegistraionForm, LoginForm
from quiz.admin.forms import SubjectForm, QuestionForm
from quiz.models import * 
from quiz.hash import Hashing
from quiz.config import Config

admin = Blueprint('admin', __name__)

@admin.before_request
def before_request():
    'Before request of login page '
    g.user_name = None
    if 'user_name' in session:
        g.user_name = session['user_name']



@admin.route('/admin', methods = ['GET', 'POST'])
def sign_up():

    'admin Registration with token number '

    form = RegistraionForm()
    session.pop('user_name', None)
    g.user_name = None
    if request.method == 'POST':   
       if form.validate_on_submit():
            user = Users.query.filter_by(user_name=form.user_name.data).first()
            config_instance = Config
            admin_token_number = config_instance.ADMIN_TOKEN
           
            if admin_token_number == request.form['token_number']:
                if(user == None):
                    hash_pass = Hashing()
                    gen_hash_password = hash_pass.gen_hash(form.password.data)
                    user = Users(user_name=form.user_name.data, mobile_number=form.mobile_number.data, password=gen_hash_password, is_admin='True')
                    db.session.add(user)
                    db.session.commit()
                
                    flash('Your account successfully created')
                    return redirect(url_for('admin.log_in'))
                else:
                    flash('User Name is already exist')
            flash('Enter valid Token Number ')        

       form.user_name.data  = ''
       form.password.data = ''
       form.mobile_number.data = ''    
       form.submit.data = ''
    return render_template('admin_registration.html', form=form)



@admin.route('/log_in', methods=['GET', 'POST'])
def log_in():
    'User login '
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            session.pop('user_name', None)
            hash_pass = Hashing()
            user = Users.query.filter_by(user_name=form.user_name.data).first()
            if user: 
                check_hash_password = hash_pass.check_hash(user.password, form.password.data)
                if check_hash_password: 
                    session['user_name'] = form.user_name.data 
                    if user.is_admin == 'True':
                        return redirect(url_for('admin.admin_dashboard'))
                   
                else:
                    flash('Enter valid password  ') 
                    return redirect(url_for('admin.log_in'))                   
            flash('Enter valid username ')       

    return render_template('login.html', form=form, admin=True)                





@admin.route('/admin_dashboard')
def admin_dashboard():

    'Admin dashboard'

    if g.user_name:
        flash('Welcome to Admin panel')
        return render_template('admin_dashboard.html')
    return redirect(url_for('users.log_in'))    


@admin.route("/show_user_data")
def show_user_data(): 
    if g.user_name: 

        'Admin can show user detail'
    # user_data = Users.query.all()

        user_data = Users.query.filter_by(is_admin='False')
        if user_data:
             return render_template('show_user_data.html', user_data=user_data, user_available =True)
        return render_template('show_user_data.html', user_available=False)
    return redirect('users.log_in')    


@admin.route('/update_and_delete/<int:id>')
def update_and_delete(id):

    'Admin can update and delete user'

    return render_template('delete_and_update_user.html', id=id)



@admin.route('/subject_panel')
def subject_panel():
    
    'Subject panel'

    return render_template('subject_panel.html')    

@admin.route('/question_panel')
def question_panel():

    'Question panel'

    return render_template('question_panel.html')  


@admin.route('/add_subject', methods= ['GET', 'POST'])
def add_subject():

    'User can add subject.'

    subject_form = SubjectForm()
    if request.method == 'POST':
        if subject_form.validate_on_submit():
            subject_name = subject_form.subject_name.data
            is_subject_available = Subject.query.filter_by(subject_name=subject_name).first()
            if is_subject_available == None: 
                subject = Subject(subject_name=subject_name.upper())
                db.session.add(subject)
                db.session.commit()
                flash(f"{subject_name.upper()} subject has been added")
                return redirect(url_for('admin.add_subject'))
            else:
                flash('Subject is already available ')    

    return render_template('add_subject.html', subject_form=subject_form)    



@admin.route('/update_subject', methods= ['GET', 'POST'])
def update_subject():

    'Admin can update subject'

    subjects =  Subject.query.all()
    if len(subjects) != 0 : 
        if request.method == 'POST':
            select_subject_name = request.form.get('subject_name')
            update_subject_name = request.form.get('update_subject_name').upper()
            is_subject_available = Subject.query.filter_by(subject_name=update_subject_name).first()
            if is_subject_available == None: 
                subject_update =  Subject.query.filter_by(subject_name=select_subject_name).first()
                try:
                    subject_update.subject_name = update_subject_name
                    db.session.add(subject_update)
                    db.session.commit()
                    flash('Subject name has Updated')
                except:
                    flash('Subject name has not updated')
               
            else:
                flash('subject already available ')       
    else:
        flash('Subject is not available')
        return redirect(url_for('admin.admin_panel'))
                
    return render_template('update_subject.html', subjects=subjects)

            
@admin.route('/delete_subject', methods = ['POST', 'GET'])
def delete_subject():

    'admin can delete subject'

    if g.user_name: 
        subjects =  Subject.query.all()
        if len(subjects) != 0 : 

            if request.method == 'POST':
                select_subject_name = request.form.get('subject_name')
                subject_delete =  Subject.query.filter_by(subject_name=select_subject_name).first()
                try:
                    db.session.delete(subject_delete)
                    db.session.commit()

                    flash('Subject name has deleted')
                    return redirect(url_for('admin.delete_subject'))
                except:
                    flash("Subject name has not deleted ")
                    
                
        else:
            return redirect(url_for('admin.admin_panel'))
                    
        return render_template('delete_subject.html', subjects=subjects)
    return redirect(url_for('users.log_in'))     


@admin.route('/add_question', methods= ['GET', 'POST'])
def add_question():

    'Admin can add question'

    if g.user_name: 
        question_form = QuestionForm()
        subjects = Subject.query.all()
        if len(subjects) != 0 :
            question_form.select_subject.choices = []
            count = 0 
            for subject in subjects: 
                question_form.select_subject.choices.append(( str(count), subject.subject_name))
                count += 1 

            if request.method == 'POST':
                if question_form.validate_on_submit():
                    question = question_form.question.data.lower()
                    option1 = question_form.option1.data.lower()
                    option2 = question_form.option2.data.lower()
                    option3 = question_form.option3.data.lower()
                    option4 = question_form.option4.data.lower()
                    answer = question_form.answer.data.lower()
                    option_set = {option1, option2, option3, option4}
                    if len(option_set) == 4 and answer in option_set:
                        select_subject = question_form.select_subject.choices[question_form.select_subject.data][1]
                        question_level = question_form.select_question_level.choices[question_form.select_question_level.data][1]
                        subject_id = Subject.query.filter_by(subject_name=select_subject).first().id
                        question_table = Question(subject_id= subject_id, question_level=question_level , question=question, option1=option1, option2=option2, option3=option3, option4=option4, answer=answer)
                        db.session.add(question_table)
                        db.session.commit()
                        flash('Question is added successfully')
                        
                    
                    return redirect(url_for('admin.add_question'))    
        return render_template('add_question.html', question_form=question_form)  
    return redirect(url_for('users.log_in'))    


@admin.route('/log_out')
def log_out():
    'Log Out user '
    session["user_name"] = None 
    return redirect(url_for('users.log_in'))

