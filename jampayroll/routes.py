from flask import (
    render_template, url_for, flash, redirect, request, jsonify
    )
from jampayroll import (
    app, db, bcrypt
    )
from jampayroll.forms import (
    RegistrationForm, 
    LoginForm, 
    WeeklyHours, 
    DailyHours, 
    EmployeeForm, 
    CompanyForm, 
    PostForm, 
    Form2SQL
    )
from jampayroll.models import (
    User, 
    Post, 
    Employee, 
    Unique,
    Company,
    Category,
    )
from jampayroll.Pay_stub import (
    Pay_stub, Employee_form_data, ModGeneratedPayStubFrom
    )
from flask_login import (
    login_user, current_user, logout_user, login_required
    )
# =========================================
posts = [
    {
        'author': 'S Attila Turkoz', 'title': 'Add Intro Home', 'content': 'content', 'date_posted': 'Nov, 18 2019' },
    {
        'author': 'S Attila Turkoz', 'title': 'Add Nav Bar Icons', 'content': 'content', 'date_posted': 'Nov, 18 2019' },
    {
        'author': 'S Attila Turkoz', 'title': 'Move Tasks SideBar', 'content': 'content', 'date_posted': 'Nov, 18 2019' },        
    ]
# =========================================

@app.before_first_request
def setup():
    pass
    # Drops all data, dont forget to register again if testing user-only features
    # db.drop_all()
    # Creates all tables, required if a new db-model to be tested
    # db.create_all()

@app.route('/', methods = ['POST', 'GET'])
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


@app.route("/wall", methods = ["GET", "POST"]) 
# @login_required
def wall():
    pass
    if current_user.is_authenticated:
        UserAllEmployees = Employee.query.filter_by(user_id=current_user.id)
        UserAllCompanies = Company.query.filter_by(user_id=current_user.id)
        EmployeeF0rm = EmployeeForm()
        CompanyF0rm = CompanyForm()
        return render_template(
            "wall.html",
            EmployeeForm = EmployeeF0rm, 
            CompanyForm = CompanyF0rm, 
            title = 'wall', 
            AllEmployees = UserAllEmployees, 
            AllCompanies = UserAllCompanies, 
            WallPosts = posts
            )
    else:
        flash('Please login to enjoy all Wall features!')
        return redirect('login')

@app.route('/addcompany', methods = ["GET","POST"])
def addcompany():
    pass
    FormsFilled = CompanyForm(obj = request.form)
    duplicate = Company.query.filter_by(companyName = str(FormsFilled.companyName.data)).first()
    if duplicate == None:
        pass
        company_to_database = Company(
            companyName = FormsFilled.companyName.data, 
            man4ger = current_user
            )
        db.session.add(company_to_database)
        db.session.commit()
        flash('Company added to database', 'secondary')
        return render_template(
            'addcompany_data.html', 
            CompanyFormData = FormsFilled,
            )
    else:
        pass
        flash('Duplicate record, please review info and try again')
        redirect(url_for('wall'))

@app.route("/addemployee", methods=["GET","POST"]) 
def addemployee():
    pass
    # Forms2fill.validate_uniq3()
    FormsFilled = EmployeeForm(obj=request.form)
    FormsFilled.generate_tag()
    generated_tag = str(FormsFilled.tag)
    duplicate = Unique.query.filter_by(tag=generated_tag).first()
    print(duplicate)
    if  duplicate == None:
        pass
        print('routes if equals none')
        tag_to_database = Unique(tag = generated_tag, manag3r = current_user)
        db.session.add(tag_to_database)
        employee_to_database = Employee(firstName = request.form["firstName"],middleName = request.form["middleName"], lastName = request.form["lastName"], companyName = request.form["companyName"],
        allowance = request.form["allowance"], hourlyRate=request.form["hourlyRate"], manager = current_user,)
        # database create entry
        db.session.add(employee_to_database)
        db.session.commit()
        flash('Employee added to database', 'secondary')
        return render_template(
            "addemployee_data.html",
            EmployeeFormData = FormsFilled,
            title='add employee',
            )
    else:
        print('route > else')
        # raise ValidationError('Duplicate record')
        flash('Duplicate record, please review info', 'danger')
        return redirect(
            url_for('wall')
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
        pass
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

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

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

