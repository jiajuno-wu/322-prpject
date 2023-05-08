from flask import Blueprint, render_template, redirect,url_for
from ltt.forms import Additem , CommentForm
from ltt import app
from ltt import db
from ltt.models import Item, Comment

import random

view = Blueprint("view",__name__)

TABOO = ["dead","death"]

@view.route('/')
@view.route('/home')   #home page to show all the item
def home():
    items = Item.query.all()
    return render_template("home.html", items = items)



@view.route('/additem',methods = ['GET','POST'])  #page for staff to add item
def additem():
    form = Additem()
   
    if form.validate_on_submit():  # function is called when press submit button
        item_to_add = Item(id = form.id.data,
                       item_name = form.item_name.data,
                       item_price = form.item_price.data,
                       item_image = form.item_image.data,
                       item_type = form.item_type.data,
                       item_c = form.item_c.data,)
        db.session.add(item_to_add)
        db.session.commit()
        return redirect(url_for('view.additem'))
    return render_template('additems.html',form=form)



@view.route('/displayItem')   #page for staff to view item
def displayItem():
    items = Item.query.all()
    return render_template('displayItem.html', items = items)




@view.route('/delete/<int:id>')  #a route bind to a delete button hit when the button is pressed
def delete(id):
    item_to_delete = Item.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('view.displayItem'))
    except:
        return 'There was an error deleting'




@view.route('/itempage/<int:items_id>', methods = ['GET','POST'])   #item page
def views(items_id):
    item_to_show = Item.query.get_or_404(items_id)
    c = Comment.query.filter_by(item_id = items_id)
    
    form = CommentForm()
    if form.validate_on_submit():
        # if form.content.data contain taboo then give  warning
        #text = form.content.data
        #text = text.split(' ')
        #for t in TABOO:
        #    if t in text : update the current user col "warning" by +1 in the USER table  
        #
        comment = Comment(content = form.content.data, item_id = items_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('view.views', items_id = items_id))

    return render_template('item.html',item_to_show = item_to_show,c = c ,form = form)
