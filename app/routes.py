from app import app
from flask import render_template

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