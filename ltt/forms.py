from flask_wtf import FlaskForm
from wtforms import StringField , IntegerField , SubmitField, FloatField, SelectField
from wtforms.validators import Length , DataRequired
from ltt.models import Item, Comment, User, Application, Message,PC,Purchase,Inquiry,InqMessages, Feedback

# Creates a form to add items to the store
# with options for name, price, image, type, and compatibility
class Additem(FlaskForm):
    id = IntegerField(label= 'id', validators=[DataRequired()])
    item_name = StringField(label='item_name',  validators=[DataRequired()])
    item_price = IntegerField(label='item_price',  validators=[DataRequired()])
    item_image = StringField(label='image_path',validators=[DataRequired()])
    item_type = StringField(label='type',  validators=[DataRequired()])
    item_c = IntegerField(label='c type',  validators=[DataRequired()])
    submit = SubmitField(label='add')

# Creates a form to add comments
# with a string for the comment and a submit button
class CommentForm(FlaskForm):
    content = StringField(label='content',  validators=[DataRequired()])
    submit = SubmitField(label='post')

# Creates a form to add an integer rating
# as well as a submit button to apply it
class RateForm(FlaskForm):
    rate = IntegerField(label='rate',  validators=[DataRequired()])
    submit = SubmitField(label='give')

# Creates a form to register the user
# with string fields for username and password
# a dropdown for the customer type, and a submit button
class RegisterUser(FlaskForm):
    username_ = StringField(label='username',  validators=[DataRequired()])
    password_ = StringField(label='password',  validators=[DataRequired()])
    userType_ = SelectField(u'UserType', choices=[('Customer', 'Customer'), ('Employee', 'Employee'), ('Admin', 'Admin')])
    submit = SubmitField(label='Submit')

# Creates a form to log users in
# with string fields for username and password
# and a submit button to sign in
class LoginForm(FlaskForm):
    username_ = StringField(label='username',  validators=[DataRequired()])
    password_ = StringField(label='password',  validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

# Creates a form to deposit money
# with a float field for a deposit of currency
# and a submit button to complete the  deposit
class DepositForm(FlaskForm):
    amount = FloatField(label='Amount',  validators=[DataRequired()])
    submit = SubmitField(label='Deposit')

# A button to purchase items
class PurchaseForm(FlaskForm):
    submit = SubmitField(label = 'Purchase')

# Creates a form to create a PC
# with a string field for the name
# integer fields to input the IDs of the pieces
# and a submit button to create the build
class PCForm(FlaskForm):
    PCname = StringField(label='item_name',  validators=[DataRequired()])
    CPU = IntegerField(label= 'id', validators=[DataRequired()])
    GPU = IntegerField(label= 'id', validators=[DataRequired()])
    MB = IntegerField(label= 'id', validators=[DataRequired()])
    RAM = IntegerField(label= 'id', validators=[DataRequired()])
    submit = SubmitField(label = 'Create')

# 
class InquiryForm(FlaskForm):
    purchase_ = SelectField(u'Choose Purchase', choices=[], coerce=int, validate_choice=True)
    submit = SubmitField(label = 'Open Inquiry')

# Has string for inquiry, and submit button to send
class AddInquiryMessageForm(FlaskForm):
    content = StringField(label='content',  validators=[DataRequired()])
    submit = SubmitField(label='Post Message')

# Button to close inquiry
class CloseInquiryForm(FlaskForm):
    submit__ = SubmitField(label='Close')

# Gives option to submit Compliment or Complaint
# along with a string field for a comment to expand on the choice
# and a submit button to send it
class FeedbackForm(FlaskForm):
    feedbackType_ = SelectField('Feedback', choices=[('Compliment', 'Compliment'), ('Complaint', 'Complaint')] )
    conten = StringField(label='comments')
    submit_ = SubmitField(label='Send Feedback')
