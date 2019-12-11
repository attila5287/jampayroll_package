from datetime import datetime
from jampayroll import db, login_manager
from flask_login import UserMixin

# ===================================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    is_urgent = db.Column(db.Text, default='n')
    is_important = db.Column(db.Text, default='n')
    matrix_zone = db.Column(db.Text, default='00')
    border_style = db.Column(db.Text, default='info')
    urg_points= db.Column(db.Integer, default=int(36)) 
    imp_points = db.Column(db.Integer, default=int(36))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
 
    def add_matrix_zone(self):
        pass
        self.matrix_zone = str(self.is_urgent) + str(self.is_important)
    
    def add_task_border(self):
        pass
        style_dict = {'11' : 'danger', '10' : 'warning', '01' : 'primary', '00' : 'info'}
        self.border_style = style_dict[self.matrix_zone]
    
    def add_urgency_points(self):
        pass
        urgency_point_dict = {
            '11' : '96',
            '10' : '72',
            '01' : '48',
            '00' : '36',
        }
        self.urg_points = int(urgency_point_dict[self.matrix_zone])

    def add_importance_points(self):
        pass
        importance_point_dict = {
            '11' : '96',
            '10' : '48',
            '01' : '72',
            '00' : '36',
        }
        self.imp_points = int(importance_point_dict[self.matrix_zone])        

    def __repr__(self):
        return '<Task %s>' % self.title
# ===================================
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    employees = db.relationship('Employee', backref='manager', lazy=True)
    tags = db.relationship('Unique', backref='manag3r', lazy=True)
    companies = db.relationship('Company', backref='man4ger', lazy=True)
    tasks = db.relationship('Task', backref='manag5r', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
# ===================================
class Post(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    # category = db.relationship('Category', backref=db.backref('posts', lazy=True))
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
# ===================================
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name
# ===================================
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(64))
    middleName = db.Column(db.String(64))
    lastName = db.Column(db.String(64))
    companyName = db.Column(db.String(64))
    allowance = db.Column(db.Integer)
    hourlyRate = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Employee %r %r>' % (self.firstName, self.lastName) 
# ====================
class Unique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tag = db.Column(db.String(64))
# ====================
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Employee %r %r>' % (self.firstName, self.lastName) 

