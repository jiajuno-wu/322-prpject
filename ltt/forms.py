from flask_wtf import FlaskForm
from wtforms import StringField , IntegerField , SubmitField
from wtforms.validators import Length , DataRequired

class Additem(FlaskForm):
    #id = IntegerField(label= 'id', validators=[DataRequired()])
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