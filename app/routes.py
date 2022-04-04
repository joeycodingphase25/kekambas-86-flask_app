
from app import app
from flask import redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, SignUpForm, ItemForm
from app.models import User, Item, Cart
from app.stored import about_data, store_data



@app.route('/')
def index():
    title = "Jojo's Flask Shop"
    return render_template('index.html', title=title)


@app.route('/about')
def about():
    title = "Things I learned"
    data = about_data
    return render_template('about.html', title=title, about_data=data)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    title = 'Sign Up To Make An Account'
    form = SignUpForm()
    # check if a post request and that the form is valid
    if form.validate_on_submit():
        # Get data from the validated form
        email = form.email.data
        username = form.username.data
        password = form.password.data
        # Check if there is a user with email or username
        users_with_that_info = User.query.filter((User.username==username)|(User.email==email)).all() 
        if users_with_that_info:
            flash(f"There is already a user with that username and/or email. Please try again", "danger")
            return render_template('signup.html', title=title, form=form)
        new_user = User(email=email, username=username, password=password)
        # flash message saying new user has been created
        flash(f"{new_user.username} has succesfully signed up.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html', title=title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Log In to Start Shopping'
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f'THANK YOU {user} AND HAPPY SHOPPING', 'success')
            return redirect(url_for('index')) #change to browse later
        else:
            flash('Username and/or password is wrong.', 'danger')
    return render_template('login.html', title=title, form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out, Thanks!', 'primary')
    return redirect(url_for('index'))

@app.route('/browse')
@login_required
def browse():
    title = 'Shopping Center'
    data = Item.query.all()
    price = round(sum([float(item.price) for item in Cart.query.all()]), 2)
    return render_template('browse.html', title=title, data=data, total=price)

@app.route('/browse/<item_id>')
@login_required # this grants current user acccess
def single_item(item_id):
    var = Item.query.get(item_id)
    cart = Cart(category = var.category, item = var.item, price = var.price, user_id = current_user.id)
    flash(f"{cart.item} has succesfully been added to your cart for ${cart.price}.", "success")
    return redirect(url_for('browse'))

@app.route('/item-detail/<item_id>')
def item_detail(item_id):
    item = Item.query.filter_by(id=item_id).first()
    return render_template('item_detail.html', item=item)



@app.route('/checkout')
@login_required
def checkout():
    title = 'Your Shopping Cart'
    cart = [x for x in Cart.query.all()]
    price = round(sum([float(item.price) for item in Cart.query.all()]), 2)
    return render_template('checkout.html', cart=cart, title=title, price=price)

@app.route('/checkout/remove/<item_id>')
@login_required # this grants current user acccess
def remove(item_id):
    var = Cart.query.filter_by(id=item_id).first()
    sample = var.item
    var.delete()
    flash(f"{sample} has succesfully been removed to your cart", "warning")
    return redirect(url_for('checkout'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    title = 'Welcome Admin, Please add to ItemForm'
    form = ItemForm()
    if form.validate_on_submit():
        category = form.category.data
        item = form.item.data
        price = form.price.data #f"${int(form.price.data)}"
        # build total item list
        shop = Item(category=category, item=item, price=price)
        flash(f"{shop.item} has succesfully been added to database for ${shop.price}.", "success")
        return redirect(url_for('browse'))
 
    return render_template('admin.html', title=title, form=form)

