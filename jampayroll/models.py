from datetime import datetime
from jampayroll import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    employees = db.relationship('Employe3', backref='manager', lazy=True)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# ==================== JAMPAYROLL : employee BELOW ==================
class Employe3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(64))
    middleName = db.Column(db.String(64))
    lastName = db.Column(db.String(64))
    companyName = db.Column(db.String(64))
    allowance = db.Column(db.Integer)
    hourlyRate = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    concatenated_input = str(firstName.data + middleName.data + lastName.data)
    
    def __repr__(self):
        return '<Employee %r %r>' % (self.firstName, self.lastName) 

class Employee(db.Model):
    # __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(64))
    middleName = db.Column(db.String(64))
    lastName = db.Column(db.String(64))
    companyName = db.Column(db.String(64))
    allowance = db.Column(db.Integer)
    hourlyRate = db.Column(db.Float)
    hoursWorked = db.Column(db.Float)

    def __repr__(self):
        return '<Employee %r %r>' % (self.firstName, self.lastName) 
