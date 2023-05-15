from flask import Blueprint, render_template, redirect,url_for,flash
from ltt.forms import Additem , CommentForm, RateForm, RegisterUser,LoginForm,DepositForm,PurchaseForm,PCForm,InquiryForm,AddInquiryMessageForm,CloseInquiryForm,FeedbackForm
from ltt import app
from ltt import db
from ltt.models import Item, Comment, User, Application, Message,PC,Purchase,Inquiry,InqMessages, Feedback
from flask_login import login_user, current_user, logout_user

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
        item_to_add = Item(
                       id = form.id.data,
                       item_name = form.item_name.data,
                       item_price = form.item_price.data,
                       item_image = form.item_image.data,
                       item_type = form.item_type.data,
                       item_c = form.item_c.data,)
        db.session.add(item_to_add)
        db.session.commit()
        return redirect(url_for('view.additem'))
    return render_template('additems.html',form=form,current_user=current_user)



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
        return 'There was an error approving'



@view.route('/itempage/<int:items_id>', methods = ['GET','POST'])   #item page
def views(items_id):
    item_to_show = Item.query.get_or_404(items_id)
    c = Comment.query.filter_by(item_id = items_id)
    form = CommentForm()
    if form.validate_on_submit():
        # if form.content.data contain taboo then give  warning
        text = form.content.data
        text = text.split(' ')
        for t in TABOO:
            if t in text :
                if(current_user.is_active == False):
                    flash('Your comment contain taboo',category = 'danger')
                    return redirect(url_for('view.views', items_id = items_id)) 
                else:
                    current_user.warnings = current_user.warnings + 1
                    db.session.commit()
                    if current_user.warnings == 3:
                        current_user.status = "Invalid"
                        db.session.commit()
                
                    flash('Your comment contain taboo',category = 'danger')
                    return redirect(url_for('view.views', items_id = items_id)) 
        comment = Comment(content = form.content.data, item_id = items_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('view.views', items_id = items_id))

    rform = RateForm()
    if rform.validate_on_submit():
        item_to_show.rate_count = item_to_show.rate_count + 1
        item_to_show.rate_acc = item_to_show.rate_acc + rform.rate.data
        db.session.commit()
        return redirect(url_for('view.views', items_id = items_id))
    
    Pform = PurchaseForm()
    if Pform.validate_on_submit():
        if(current_user.balance >= item_to_show.item_price):
            flash('Succesfully Purchased')
            current_user.balance = current_user.balance - item_to_show.item_price
            purchase_to_add = Purchase(user_id = current_user.id,pc_id = item_to_show.id)
            db.session.add(purchase_to_add)
            db.session.commit()
            return redirect(url_for('view.views', items_id = items_id))
        else:
            flash('Insufficent Funds',category = 'danger')
            current_user.warnings = current_user.warnings + 1
            db.session.commit()
            return redirect(url_for('view.views', items_id = items_id))

    return render_template('item.html',item_to_show = item_to_show,c = c ,form = form, rform = rform,Pform = Pform,current_user=current_user)


@view.route('/register', methods = ['GET','POST']) #Register route for users
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        if form.userType_.data == "Customer":
            application_to_add = Application(username = form.username_.data,
                                             password = form.password_.data)
            db.session.add(application_to_add)
            db.session.commit()
            flash(f'Application submitted.', category='succes')
            return render_template('applicationSubmitted.html')
        else:
            user_to_add = User(username=form.username_.data, 
                            password=form.password_.data,
                            userType = form.userType_.data
                            )
            db.session.add(user_to_add)
            db.session.commit()
        return redirect(url_for('view.login'))
    return render_template('register.html', form = form)

@view.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username_.data).first()
        if attempted_user.status == "Invalid":
            flash("you are suspended")
            return render_template('login.html',form=form)
        if attempted_user and attempted_user.check_password_correction (attempted_password = form.password_.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as :{attempted_user.username}', category = 'success')
            return redirect(url_for("view.home"))
        else:
            flash('Username and password is incorrect! Please try again',category = 'danger')
            return render_template('failure.html')

    return render_template('login.html',form=form)

@view.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('view.home'))

@view.route('/deposit',methods= ['GET','POST'])
def deposit():
    form = DepositForm()
    if form.validate_on_submit():
        current_user.balance = current_user.balance + form.amount.data
        db.session.commit()
        return redirect(url_for('view.home'))
    return render_template('deposit.html', form = form)

@view.route('/applications', methods = ['GET', 'POST'])
def verifyApplications():
    applicants = Application.query.all()
    return render_template('applicationList.html', applicants = applicants)

@view.route('/setPC',methods = ['GET','POST'])
def setPC():
    form = PCForm()
    if form.validate_on_submit():
        cpu = Item.query.get_or_404(form.CPU.data)
        gpu = Item.query.get_or_404(form.GPU.data)
        ram = Item.query.get_or_404(form.RAM.data)
        mb = Item.query.get_or_404(form.MB.data)
        if cpu.item_c == gpu.item_c == ram.item_c == mb.item_c:
            pc = PC(PCname = form.PCname.data,
                    cpu = cpu.id,
                    gpu = gpu.id,
                    ram = ram.id,
                    MB = mb.id)
            db.session.add(pc)
            db.session.commit()
            return redirect(url_for('view.setPC'))
        else:
            return redirect(url_for('view.setPC'))
    return render_template('setPC.html', form = form)

@view.route('/prebulid')
def prebulid():
    pc = PC.query.all()
    return render_template("prebulid.html", pc = pc)


        
@view.route('/approval/<int:id>')
def approval(id):
    application_to_approve = Application.query.get_or_404(id)
    try:
        user_to_add = User(username = application_to_approve.username,
                           password = application_to_approve.password,
                           userType = "Customer")
        db.session.add(user_to_add)
        db.session.delete(application_to_approve)
        db.session.commit()
        return redirect(url_for('view.verifyApplications'))
    except:
        return 'There was an error approving'

@view.route('/rejection/<int:id>')
def rejection(id):
    application_to_reject = Application.query.get_or_404(id)
    message_to_send = Message(username = application_to_reject.username)
    try:
        db.session.add(message_to_send)
        db.session.delete(application_to_reject)
        db.session.commit()
        return redirect(url_for('view.verifyApplications'))
    except:
        return 'There was an error rejecting'
    
@view.route('/messages', methods = ['GET', 'POST'])
def messages():
    messages = Message.query.all()
    return render_template('applicationsRejected.html', messages = messages)

@view.route('/inquiry',methods = ['GET','POST'])
def viewInquiry():
    inquiry_to_show = Inquiry.query.filter_by(user_id = current_user.id)
    purchase = Purchase.query.filter_by(user_id=current_user.id)
    form = InquiryForm()
    if form.validate_on_submit():
        rand = random.randrange(0, User.query.filter_by(userType = "Employee").count())
        inquiry_to_add = Inquiry(user_id = current_user.id,purchase_id = purchase.first().id,employee_id= User.query.filter_by(userType = "Employee").first().id )
        db.session.add(inquiry_to_add)
        db.session.commit()
        flash('Succesfully made inquiry')
        return redirect(url_for('view.currentInquiry',inquirys_id = inquiry_to_add.id))
    return render_template('inquiry.html',form=form,inquiry_to_show = inquiry_to_show)

@view.route('/inquirypage/<int:inquirys_id>',methods = ['GET','POST'])
def currentInquiry(inquirys_id):
    inquiry_to_show = Inquiry.query.get_or_404(inquirys_id)
    form = AddInquiryMessageForm()
    comments = InqMessages.query.filter_by(inquiry_id = inquirys_id)
    if form.validate_on_submit():
        comment_to_add = InqMessages(content = form.content.data , inquiry_id = inquirys_id , user_id = current_user.id)
        db.session.add(comment_to_add)
        db.session.commit()
        return redirect(url_for('view.currentInquiry',inquirys_id = inquirys_id ))
    
    cform = CloseInquiryForm()
    if cform.validate_on_submit():
        inquiry_to_show.status = "closed"
        db.session.commit()
        return redirect(url_for('view.currentInquiry',inquirys_id = inquirys_id ))

    fform = FeedbackForm()
    if fform.validate_on_submit():
        feedback_to_add = Feedback(feedbackType = fform.feedbackType_.data ,comment = fform.content_.data,employee_id = inquiry_to_show.employee_id, customer_id = inquiry_to_show.user_id, inquiry_id = inquiry_to_show.id )
        db.session.add(feedback_to_add)
        db.session.commit()
        return redirect(url_for('view.currentInquiry', inquirys_id = inquirys_id ))

    return render_template('displayInquiry.html',form=form,comments=comments,inquiry_to_show = inquiry_to_show,current_user=current_user,User=User,Inquiry = Inquiry,cform=cform,fform = fform,Feedback = Feedback )