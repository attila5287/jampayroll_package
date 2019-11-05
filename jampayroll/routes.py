from flask import render_template, url_for, flash, redirect, request, jsonify
from jampayroll import app, db, bcrypt
from jampayroll.forms import RegistrationForm, LoginForm, WeeklyHours, DailyHours, EmployeeForm, PostForm, Form2SQL
from jampayroll.models import User, Post, Employee, Employe3, Unique
from jampayroll.Pay_stub import Pay_stub, Employee_form_data, ModGeneratedPayStubFrom
from flask_login import login_user, current_user, logout_user, login_required
# =========================================
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.before_first_request
def setup():
    pass
    # Recreate database each time for testing new models only
    # db.drop_all()

    # only to initiate local db not req'd for actual app on heroku
    # db.create_all()

@app.route("/")
@app.route("/addemployee", methods=["GET", "POST"]) 
def addemployee():
    user_input_first = EmployeeForm()
    if request.method == "POST":
        unique_check = Form2SQL(
            firstName = request.form["firstName"],
            middleName = request.form["middleName"],
            lastName=request.form["lastName"],
            companyName=request.form["companyName"],
            manag3r = current_user, 
            )
        
        concat_input = unique_check.concat_input_as_tag()
        _duplicate_ = Unique.query.filter_by(tag= concat_input).first()
        if _duplicate_:
            pass
            employee_to_database = Employe3(
            firstName = request.form["firstName"],
            middleName = request.form["middleName"],
            lastName=request.form["lastName"],
            companyName = request.form["companyName"],
            allowance = request.form["allowance"],
            hourlyRate=request.form["hourlyRate"],
            manager = current_user, 
            )
            # database create entry
            db.session.add(employee_to_database)
            db.session.commit()
            flash('Employee added to database', 'success')
        else:
            # raise ValidationError('Duplicate employee info, please review forms')
            flash('Duplicate employee info, please review forms', 'danger')
        AllEmployees = Employe3.query.filter_by(user_id=current_user.id)
        user_input_received = EmployeeForm(obj=request.form)
        return render_template(
            "addemployee_data.html",
            EmployeeFormData = user_input_received,
            title='employee added',
            AllEmployees = AllEmployees,
        )

    return render_template(
        "addemployee.html",
        EmployeeForm=user_input_first,
        title = 'add employee'
    )

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template(
        'create_post.html',
        title='New Post', 
        form=form, legend='New Post',
    )

@app.route('/timesheet', methods = ['POST', 'GET'])
def timesheet():
    pass
    We3klyTimesheet = WeeklyHours()
    D4ys = ['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun']
    if request.method == 'POST':
        pass
        # still need request.form for iteration through form data
        result = request.form
        We3klyTimesheetRes = WeeklyHours(obj=request.form)
        return render_template(
            "f0rm_data.html",
            Days=D4ys,
            WeeklyResult=result,
            WeeklyTimesheetRes = We3klyTimesheetRes
        )
    return render_template(
        'f0rm.html',
        Days = D4ys, 
        WeeklyTimesheetForm=We3klyTimesheet
        )

@app.route('/intro', methods = ['POST', 'GET'])
def intro():
    return render_template('h0me.html')

# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"]) 
def send():
    if request.method == "POST":
        employee = Employee(
            firstName = request.form["firstName"],
            middleName = request.form["middleName"],
            lastName=request.form["lastName"],
            companyName = request.form["companyName"],
            allowance = request.form["allowance"],
            hourlyRate = request.form["hourlyRate"],
            hoursWorked=request.form["hoursWorked"]
            )
        #  database create entry
        db.session.add(employee)
        db.session.commit()

        user_input = Employee_form_data(
            firstName = request.form["firstName"],
            middleName = request.form["middleName"],
            lastName=request.form["lastName"],
            companyName = request.form["companyName"],
            allowance = request.form["allowance"],
            hourlyRate = request.form["hourlyRate"],
            hoursWorked=request.form["hoursWorked"]
        )

        generated_paystub = ModGeneratedPayStubFrom(
            firstName = request.form["firstName"],
            middleName = request.form["middleName"],
            lastName=request.form["lastName"],
            companyName = request.form["companyName"],
            allowance = int(request.form["allowance"]),
            hourlyRate = float(request.form["hourlyRate"]),
            hoursWorked= float(request.form["hoursWorked"]),
            payCntYr2Dt= int(request.form["payCntYr2Dt"]),
            dateStart=request.form["dateStart"],
            dateEnd=request.form["dateEnd"]
        )
        dict = {
            'Social Security': float(generated_paystub.social_security_perc),
            'Medicare': float(generated_paystub.medicare_perc),
            'Total Taxes Withheld From Employee': float(generated_paystub.taxes_perc),
            'Net Pay': float(generated_paystub.net_pay_perc)
            # 'FUTA' : float(generated_paystub.futa_perc), 
            # 'State Unemployment Tax' : float(generated_paystub.co_unemp_perc) 
            }
    
        return render_template("pay_stub_generat0r.html", Pay_stub=generated_paystub, dict = dict)
        
    return render_template("form.html")
# ================IMPLEMENT JAMPAYROLL ABOVE================

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')



@app.route("/api/pals")
def pals():
   results = db.session.query(Employee.lastName, Employee.firstName, Employee.middleName, Employee.allowance, Employee.hourlyRate, Employee.hoursWorked).all()

   firstName = [result[0] for result in results]
   middleName = [result[1] for result in results]
   lastName = [result[2] for result in results]
   allowance = [result[3] for result in results]
   hourlyRate = [result[4] for result in results]
   hoursWorked = [result[5] for result in results]
   ee_data = [{
         'firstName' : firstName,
         'middleName' : middleName,
         'lastName' : lastName,
         'allowance' : allowance,
         'hourlyRate' : hourlyRate,
         'hoursWorked' : hoursWorked
   }]
   return jsonify(ee_data)

