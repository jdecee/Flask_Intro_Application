from app import app
from flask import render_template
from app.forms import PhoneBookForm, UserInfoForm, PostForm
from app.models import Contact, User, Post
from app import db

@app.route('/')
def index():
    name = 'Jon'
    title = 'Coding Temple Class'
    return render_template('index.html', name_of_user=name, title=title)


@app.route('/products')
def test():
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
        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()
    return render_template('register.html', form=register_form)

@app.route('/createpost', methods=['GET', 'POST'])
def createpost():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_post = Post(title, content, user_id)
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