from app import app, db
from flask import render_template, redirect, url_for, flash
from flask_login import login_user
from app.forms import LoginForm, PhoneBookForm, UserInfoForm, PostForm
from app.models import Contact, User, Post


@app.route('/')
def index():
    name = 'Jon'
    title = 'Coding Temple Class'
    return render_template('index.html', name_of_user=name, title=title)

@app.route('/products')
def products():
    title = 'Coding Temple Products'
    products = ['apple', 'orange', 'banana', 'peach']
    return render_template('products.html', title=title, products=products)

@app.route('/heroes')
def heroes():
    heroes = ['Mom', 'Dad', 'Elon Musk', 'Craig Ferguson', 'Dane Cook' ]
    return render_template('heroes.html', heroes=heroes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = UserInfoForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data

        existing_user = User.query.filter_by(username=username).all()
        if existing_user:
            flash(f'{username} is already in use. Please register with a new username', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(username, email, password)
        
        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you {username}, you have successfully registered!', 'success')

        return redirect(url_for('index'))

    return render_template('register.html', form=register_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash(f'Your username or password is incorrect', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        flash(f'You have successfully logged in!', 'success')
        return redirect(url_for('index'))    

    return render_template('login.html', form=form)    

@app.route('/createpost', methods=['GET', 'POST'])
def createpost():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_post = Post(title, content, user_id=1)
        db.session.add(new_post)
        db.session.commit()
    return render_template('createpost.html', form=form)

@app.route('/phonebook', methods=['GET', 'POST'])
def add_contact():
    form = PhoneBookForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        address = form.address.data
        phone_number = form.phone_number.data
        new_contact = Contact(first_name, last_name, address, phone_number)
        db.session.add(new_contact)
        db.session.commit()
    return render_template('phonebook.html', form=form)