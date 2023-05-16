from flask_wtf import FlaskForm
from wtforms import StringField , IntegerField , SubmitField, FloatField, SelectField
from wtforms.validators import Length , DataRequired
from ltt.models import Item, Comment, User, Application, Message,PC,Purchase,Inquiry,InqMessages, Feedback

class Additem(FlaskForm):
    id = IntegerField(label= 'id', validators=[DataRequired()])
    item_name = StringField(label='item_name',  validators=[DataRequired()])
    item_price = IntegerField(label='item_price',  validators=[DataRequired()])
    item_image = StringField(label='image_path',validators=[DataRequired()])
    item_type = StringField(label='type',  validators=[DataRequired()])
    item_c = IntegerField(label='c type',  validators=[DataRequired()])
    submit = SubmitField(label='add')

class CommentForm(FlaskForm):
    content = StringField(label='content',  validators=[DataRequired()])
    submit = SubmitField(label='post')

class RateForm(FlaskForm):
    rate = IntegerField(label='rate',  validators=[DataRequired()])
    submit = SubmitField(label='give')

class RegisterUser(FlaskForm):
    username_ = StringField(label='username',  validators=[DataRequired()])
    password_ = StringField(label='password',  validators=[DataRequired()])
    userType_ = SelectField(u'UserType', choices=[('Customer', 'Customer'), ('Employee', 'Employee'), ('Admin', 'Admin')])
    submit = SubmitField(label='Submit')

class LoginForm(FlaskForm):
    username_ = StringField(label='username',  validators=[DataRequired()])
    password_ = StringField(label='password',  validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class ApplicationForm(FlaskForm):
    username_  = StringField(label='username',  validators=[DataRequired()])
    submit = SubmitField(label='Application')

class DepositForm(FlaskForm):
    amount = FloatField(label='Amount',  validators=[DataRequired()])
    submit = SubmitField(label='Deposit')

class PurchaseForm(FlaskForm):
    submit = SubmitField(label = 'Purchase')

class PCForm(FlaskForm):
    PCname = StringField(label='item_name',  validators=[DataRequired()])
    CPU = IntegerField(label= 'id', validators=[DataRequired()])
    GPU = IntegerField(label= 'id', validators=[DataRequired()])
    MB = IntegerField(label= 'id', validators=[DataRequired()])
    RAM = IntegerField(label= 'id', validators=[DataRequired()])
    submit = SubmitField(label = 'Create')

class InquiryForm(FlaskForm):
    purchase_ = SelectField(u'Choose Purchase', choices=[], coerce=int, validate_choice=True)
    submit = SubmitField(label = 'Open Inquiry')

class AddInquiryMessageForm(FlaskForm):
    content = StringField(label='content',  validators=[DataRequired()])
    submit = SubmitField(label='Post Message')

class CloseInquiryForm(FlaskForm):
    submit__ = SubmitField(label='Close')

class FeedbackForm(FlaskForm):
    feedbackType_ = SelectField('Feedback', choices=[('Compliment', 'Compliment'), ('Complaint', 'Complaint')] )
    conten = StringField(label='comments')
    submit_ = SubmitField(label='Send Feedback')
