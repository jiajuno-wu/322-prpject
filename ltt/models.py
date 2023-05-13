from ltt import db,app,login_manager
  #from this package import the db object 
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(120))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    
    def __repr__(self):
        return f'<Comment"{self.content}">'


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
    
class Application(db.Model):
    _tablename_ = 'Application'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), default = None)
    password = db.Column(db.String(120), default = None)

class PC(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    PCname = db.Column(db.String(120))
    cpu = db.Column(db.Integer, db.ForeignKey('item.id'))
    gpu = db.Column(db.Integer, db.ForeignKey('item.id'))
    ram = db.Column(db.Integer, db.ForeignKey('item.id'))
    MB = db.Column(db.Integer, db.ForeignKey('item.id'))

class Message(db.Model):
    _tablename_ = 'Message'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), default = None)


with app.app_context():
    # db.drop_all()
    db.create_all()
