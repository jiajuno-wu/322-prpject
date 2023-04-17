from flask import Blueprint, render_template, redirect,url_for
from ltt.forms import Additem
from ltt import app
from ltt import db
from ltt.models import Item

view = Blueprint("view",__name__)

@view.route('/')
@view.route('/home')
def home():
    items = Item.query.all()
    return render_template("home.html", items = items)



@view.route('/additem',methods = ['GET','POST'])
def additem():
    form = Additem()
   
    if form.validate_on_submit():
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



@view.route('/displayItem')
def displayItem():
    items = Item.query.all()
    return render_template('displayItem.html', items = items)




@view.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Item.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('view.displayItem'))
    except:
        return 'There was an error deleting'


