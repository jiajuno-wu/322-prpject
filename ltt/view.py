from flask import Blueprint, render_template, redirect,url_for,flash, request
from ltt.forms import Additem , CommentForm, RateForm, RegisterUser,LoginForm,DepositForm,PurchaseForm,PCForm,InquiryForm,AddInquiryMessageForm,CloseInquiryForm,FeedbackForm
from ltt import app
from ltt import db
from ltt.models import Item, Comment, User, Application, Message,PC,Purchase,Inquiry,InqMessages, Feedback
from flask_login import login_user, current_user, logout_user

import random

view = Blueprint("view",__name__)

TABOO = ["dead","death"]

id_list = [0,0,0,0]


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
    comment_to_submit = ""
    form = CommentForm()
    if form.validate_on_submit():
        # if form.content.data contain taboo then give  warning
        text = form.content.data
        text = text.split(' ')
        iterator = 0
        taboo_count = 0
        for t in text:
            if t in TABOO :
                taboo_count = taboo_count+1
                comment_to_submit = comment_to_submit +" "+ ('*'*len(t))
            else:
                comment_to_submit = comment_to_submit + " " +  text[iterator]
            iterator = iterator + 1
            

        if(current_user.is_active == False and taboo_count != 0):
            flash('Your comment contain taboo',category = 'danger')
            return redirect(url_for('view.views', items_id = items_id)) 
        else:
            if taboo_count > 3:
                current_user.warnings = current_user.warnings + 2
                db.session.commit()
                flash('Your comment contain TOO many Taboos',category = 'danger') 
                if current_user.warnings >= 3:
                    current_user.status = "Invalid"
                    db.session.commit()
                return redirect(url_for('view.views', items_id = items_id))

            else:
                current_user.warnings = current_user.warnings + 1
                db.session.commit()

            if current_user.warnings == 3:
                current_user.status = "Invalid"
                db.session.commit()

        comment = Comment(content = comment_to_submit, item_id = items_id)
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
        if attempted_user.userType == "Employee":
            if attempted_user.compliments > 3:
                flash("you are promote")
                attempted_user.compliments = 0
                db.session.commit()
            if attempted_user.warnings > 6:
                flash("you are fired")
                attempted_user.status = "Invalid"
                db.session.commit()

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






#this is for the staff
@view.route('/setPC',methods = ['GET','POST'])
def setPC():
    form = PCForm()
    if form.validate_on_submit():
        cpu = Item.query.get_or_404(form.CPU.data)
        gpu = Item.query.get_or_404(form.GPU.data)
        ram = Item.query.get_or_404(form.RAM.data)
        mb = Item.query.get_or_404(form.MB.data)
        if (cpu.item_c == gpu.item_c == ram.item_c == mb.item_c):
            pc = PC(PCname = form.PCname.data,
                    cpu = cpu.id,
                    gpu = gpu.id,
                    ram = ram.id,
                    MB = mb.id,
                    creator_id = current_user.id )
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





#this is for the user
@view.route('/customize',methods = ['GET','POST'])
def customize():
    flag = 0 #if flag is 0 which mean it is no compatiable
    pform = PCForm()
    if pform.validate_on_submit():
        cpu = Item.query.get_or_404(pform.CPU.data)
        gpu = Item.query.get_or_404(pform.GPU.data)
        ram = Item.query.get_or_404(pform.RAM.data)
        mb = Item.query.get_or_404(pform.MB.data)
        id_list [0] = pform.CPU.data
        id_list [1] = pform.GPU.data
        id_list [2] = pform.RAM.data
        id_list [3] = pform.MB.data
        sum = cpu.item_price + gpu.item_price + ram.item_price + mb.item_price
        if cpu.item_c == gpu.item_c == ram.item_c == mb.item_c:
            flag = 1
            if current_user.balance < sum:
                flash("not enough balance") 
                current_user.warnings = current_user.warnings + 1
                db.session.commit()
                return redirect(url_for('view.deposit'))
            else:
                flash("purchased")
                current_user.balance = current_user.balance - sum
                purchase_to_add = Purchase(user_id = current_user.id)
                db.session.add(purchase_to_add)
                db.session.commit()
                return render_template("customize.html", pform = pform, flag = flag)
        else:
            flag = 0
            flash("NOT compatible")
            return redirect(url_for('view.customize'))
    return render_template("customize.html", pform = pform, flag = flag)





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





@view.route('/buy/<int:id>', methods = ['GET', 'POST'])
def buy(id):
    pc = PC.query.get_or_404(id)
    cpu = Item.query.get_or_404(pc.cpu)
    gpu = Item.query.get_or_404(pc.gpu)
    ram = Item.query.get_or_404(pc.ram)
    mb = Item.query.get_or_404(pc.MB)
    sum = cpu.item_price + gpu.item_price + ram.item_price + mb.item_price
    flag = 0 #if 0 mean customer have no 10% off
    if current_user.compliments >= 3:
        flag = 1
    if current_user.balance < sum :
        current_user.warnings = current_user.warnings + 1
        db.session.commit()
        return redirect(url_for('view.deposit'))
    else:
        if flag == 1:
            current_user.balance = current_user.balance - 0.9*sum
            purchase_to_add = Purchase(user_id = current_user.id,pc_id = pc.id)
            db.session.add(purchase_to_add)
            db.session.commit()
            return redirect(url_for('view.rate',id = id))
        else :
            current_user.balance = current_user.balance - sum
            purchase_to_add = Purchase(user_id = current_user.id,pc_id = pc.id)
            db.session.add(purchase_to_add)
            db.session.commit()
            return redirect(url_for('view.rate',id = id))




@view.route('/rate/<int:id>',methods = ['GET', 'POST'])
def rate(id):
    pc = PC.query.get_or_404(id)
    rform = RateForm()
    if rform.validate_on_submit():
        pc.rate_count = pc.rate_count + 1
        pc.rate_acc = pc.rate_acc + rform.rate.data
        if (rform.rate.data <= 1):
            creator = User.query.get_or_404(pc.creator_id)
            creator.warnings = creator.warnings + 1
            db.session.delete(pc)
            db.session.commit()
        elif(rform.rate.data >= 5):
            creator = User.query.get_or_404(pc.creator_id)
            creator.compliment = creator.compliment + 1
            db.session.commit()
        db.session.commit()
        return redirect(url_for('view.prebulid'))
    return render_template('rating.html', rform = rform)




@view.route('/promote')
def promote():
    pc = PC(PCname = current_user.id, cpu = id_list [0], gpu = id_list [1], ram = id_list [2], MB = id_list [3])
    db.session.add(pc)
    db.session.commit()
    return redirect(url_for('view.prebulid'))




@view.route('/inquiry',methods = ['GET','POST'])
def viewInquiry():
    inquiries_to_show_customer = Inquiry.query.filter_by(user_id = current_user.id)
    inquiries_to_show_employee = Inquiry.query.filter_by(employee_id = current_user.id)
    purchase = Purchase.query.filter_by(user_id=current_user.id)
    form = InquiryForm()
    form.purchase_.choices = [(purchases.id, PC.query.get_or_404(purchases.pc_id)) for purchases in Purchase.query.filter_by(user_id = current_user.id)]
    if form.validate_on_submit():
        rand = random.randrange(0, User.query.filter_by(userType = "Employee").count())
        inquiry_to_add = Inquiry(user_id = current_user.id,purchase_id = purchase.first().id,employee_id= User.query.filter_by(userType = "Employee").first().id )
        db.session.add(inquiry_to_add)
        db.session.commit()
        flash('Succesfully made inquiry')
        return redirect(url_for('view.currentInquiry',inquirys_id = inquiry_to_add.id))
    return render_template('inquiry.html',form=form,inquiries_to_show_customer = inquiries_to_show_customer,inquiries_to_show_employee=inquiries_to_show_employee)




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
    fform = FeedbackForm()
    if cform.validate_on_submit():
        inquiry_to_show.status = "closed"
        db.session.commit()
        feedback_to_add = Feedback(inquiry_id = inquirys_id,feedbackType = fform.feedbackType_.data ,comment_ = fform.conten.data)
        db.session.add(feedback_to_add)
        db.session.commit()
        return redirect(url_for('view.currentInquiry',inquirys_id = inquirys_id ))

    fform = FeedbackForm()
    if fform.validate_on_submit():
        feedback_to_add = Feedback(inquiry_id = inquirys_id,feedbackType = fform.feedbackType_.data ,comment_ = fform.conten.data)
        db.session.add(feedback_to_add)
        db.session.commit()
        return redirect(url_for('view.currentInquiry', inquirys_id = inquirys_id ))

    return render_template('displayInquiry.html',form=form,comments=comments,inquiry_to_show = inquiry_to_show,current_user=current_user,User=User,Inquiry = Inquiry,cform=cform,fform = fform,Feedback = Feedback )




@view.route('/processFeedback',methods=['GET','POST'])
def processFeedback():
    feedback_to_show_complaint = Feedback.query.filter_by(feedbackType = "Complaint")
    feedback_to_show_compliment = Feedback.query.filter_by(feedbackType = "Compliment")
    return render_template('processFeedback.html',feedback_to_show_complaint=feedback_to_show_complaint, feedback_to_show_compliment=feedback_to_show_compliment,Inquiry=Inquiry)




@view.route('/giveWarning/<int:user_id>/<int:feedback_id>',methods = ['GET','POST'])
def giveWarning(user_id,feedback_id):
    user_to_warn = User.query.get_or_404(user_id)
    try:
        user_to_warn.warnings = user_to_warn.warnings + 1
        db.session.delete(Feedback.query.get_or_404(feedback_id))
        db.session.commit()
        return redirect(url_for('view.processFeedback'))
    except:
        return 'There was an error in giving warning'
    


@view.route('/giveCompliment/<int:user_id>/<int:feedback_id>',methods = ['GET','POST'])
def giveCompliment(user_id,feedback_id):
    user_to_compliment = User.query.get_or_404(user_id)
    try:
        user_to_compliment.compliments = user_to_compliment.compliments + 1
        db.session.delete(Feedback.query.get_or_404(feedback_id))
        db.session.commit()
        return redirect(url_for('view.processFeedback'))
    except:
        return 'There was an error in giving compliment'
    


@view.route('/deletepc/<int:id>')  #a route bind to a delete button hit when the button is pressed
def deletepc(id):
    pc_to_delete = PC.query.get_or_404(id)
    try:
        user = User.query.get_or_404(pc_to_delete.creator_id)
        user.warnings = user.warnings + 1
        db.session.commit()
        db.session.delete(pc_to_delete)
        db.session.commit()
        return redirect(url_for('view.prebulid'))
    except:
        return 'There was an error approving'