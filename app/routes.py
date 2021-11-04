from app import app
from flask import render_template
from app.forms import UserInfoForm

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

@app.route('/register')
def register():
    register_form = UserInfoForm()
    return render_template('register.html', form=register_form)