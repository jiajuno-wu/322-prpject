from ltt import db,app,login_manager
  #from this package import the db object 
from flask_login import UserMixin

# Pulls the user ID to have the user logged in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Item section has columns for name, price, image,
# type, compatibility, comments from users, the number
# of ratings, and the accumulated rating
class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer,primary_key = True)
    item_name = db.Column(db.String(20))
    item_price = db.Column(db.Integer)
    item_image = db.Column(db.String(20), default = "default.jpg")
    item_type = db.Column(db.String(20))
    item_c = db.Column(db.Integer)
    comments = db.relationship("Comment",backref ="item")
    rate_count = db.Column(db.Integer, default = 0)
    rate_acc = db.Column(db.Integer,default = 0)
    def __repr__(self):
        return f'<Item"{self.item_name}">'

# Comment section has column for the text of the comment
# and a foreign key for the item that it is commenting on
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(120))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    
    def __repr__(self):
        return f'<Comment"{self.content}">'

# User section has username, password, user balance,
# what type of user they are (defaulted to Visitor), 
# if they have been banned (defaulted to not), as well
# as the number of compliments and warnings
class User(db.Model,UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120),default = None )
    password = db.Column(db.String(120),default = None)
    balance = db.Column(db.Integer(),default=0)
    userType = db.Column(db.String(120),default = "Visitor")
    status = db.Column(db.String(120),default = "Valid")
    compliments = db.Column(db.Integer,default = 0)
    warnings = db.Column(db.Integer,default=0)

    def __repr__(self):
        return f'<User"{self.username}">'
    def check_password_correction(self,attempted_password):
        return self.password == attempted_password 
    
# Holds the username and password of a visitor applying
# to be a customer
class Application(db.Model):
    _tablename_ = 'Application'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), default = None)
    password = db.Column(db.String(120), default = None)

# Records the custom PC models, with information for
# name, the number of ratings, and total rating,
# as well as foreign keys for CPU, GPU, RAM, MB, and the creator
class PC(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    PCname = db.Column(db.String(120))
    cpu = db.Column(db.Integer, db.ForeignKey('item.id'))
    gpu = db.Column(db.Integer, db.ForeignKey('item.id'))
    ram = db.Column(db.Integer, db.ForeignKey('item.id'))
    MB = db.Column(db.Integer, db.ForeignKey('item.id'))
    creator_id = db.Column(db.Integer,db.ForeignKey('User.id'))
    rate_count = db.Column(db.Integer, default = 0)
    rate_acc = db.Column(db.Integer,default = 0)

# Carries the username of the rejected visitor
# when information is sent to the admin
class Message(db.Model):
    _tablename_ = 'Message'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), default = None)

# Records which users purchased which PCs
class Purchase(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    user_id = db.Column(db.Integer,db.ForeignKey('User.id'))
    pc_id = db.Column(db.Integer,db.ForeignKey('pc.id'))

# Keeps information on inquiries, including who sent it,
# about what item, to which employee, whether it has been addressed,
# and connects to the InqMessages model to hold the accompanying messge
class Inquiry(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('User.id')) 
    purchase_id = db.Column(db.Integer,db.ForeignKey('purchase.id'))
    messages = db.relationship("InqMessages",backref="inquiry")
    status = db.Column(db.String(120), default = "open")
    employee_id = db.Column(db.Integer,db.ForeignKey('User.id')) 

# Carries the content of the message, along with foreign keys
# for who sent it, and which inquiry it is attached to
class InqMessages(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(120))
    inquiry_id = db.Column(db.Integer, db.ForeignKey('inquiry.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('User.id')) 
    
    def __repr__(self):
        return f'<Message"{self.content}">'

# Responses to inquiries, with the feedbackType field
# used for Compliments or Complaints, and a string field for comments
class Feedback(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    inquiry_id = db.Column(db.Integer, db.ForeignKey('inquiry.id'))
    feedbackType = db.Column(db.String(120))
    # employee_id = db.Column(db.Integer,db.ForeignKey('User.id'))     
    # customer_id = db.Column(db.Integer,db.ForeignKey('User.id'))
    # status = db.Column(db.String(120), default = "open")
    comment_ = db.Column(db.String(120))

with app.app_context():
    # db.drop_all()
    db.create_all()
