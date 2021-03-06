from app import app, db, mail, photos
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from app.forms import LoginForm, PhoneBookForm, UserInfoForm, PostForm, AddProduct
from app.models import Contact, User, Post, Product
import secrets

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET','POST'])
@login_required
def admin():
    form = AddProduct()
    products = Product.query.all()
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        stock = form.stock.data
        colors = form.colors.data
        description = form.description.data
        image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
        new_product = Product(name, price, stock, colors, description, image)

        db.session.add(new_product)
        db.session.commit()

        flash(f'{name} has been added', 'success')
        return redirect(url_for('admin'))
    return render_template('admin.html', form=form, products=products, title='admin')

@app.route('/updateproduct/<int:product_id>', methods=['GET', 'POST'])
def updateproduct(product_id):
    product = Product.query.get_or_404(product_id)
    form = AddProduct()

    if form.validate_on_submit():
        new_name = form.name.data
        new_price = form.price.data
        new_stock = form.stock.data
        new_colors = form.colors.data
        new_description = form.description.data
        new_image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")

        product.name = new_name
        product.price = new_price
        product.stock = new_stock
        product.colors = new_colors
        product.description = new_description
        product.image = new_image

        db.session.commit() 
        flash(f'Product has been updated')
        return redirect(url_for('admin', product_id=product.id))
    return render_template('updateproduct.html', product=product, form=form)

@app.route('/deleteproduct/<int:product_id>/', methods=['GET', 'POST'])
def deleteproduct(product_id):
    product = Product.query.get_or_404(product_id)
    
    db.session.delete(product)
    db.session.commit()

    flash('Product has been deleted', 'success')
    return redirect(url_for('admin'))

@app.route('/merch')
def merch():
    products = Product.query.filter(Product.stock > 0)
    return render_template('merch.html', title='merch', products=products)

def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2,dict):
        return dict(list(dict1.items()) + list(dict2.items()) )    
    return False

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and colors and request.method == "POST":
            DictItems = {product_id: {'name':product.name, 'price':product.price, 'color': colors, "quantity": quantity, 'image':product.image, 'colors':product.colors}}
            
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    flash("This product is in your cart already :)", 'info')
                else:
                    session['Shoppingcart'] = MergeDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)    
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)    

@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        subtotal += float(product['price']) * int(product['quantity'])
        grandtotal = subtotal
    return render_template('carts.html', grandtotal=grandtotal)

# app.route('/updatecart/<int:code>', methods=['POST'])
# def updatecart(code):
#     if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
#         return redirect(url_for('home'))
#     if request.method =="POST":
#         quantity = request.form.get('quantity')
#         color = request.form.get('color')
#         try:
#             session.modified = True
#             for key , item in session['Shoppingcart'].items():
#                 if int(key) == code:
#                     item['quantity'] = quantity
#                     item['color'] = color
#                     flash('Item is updated!')
#                     return redirect(url_for('getCart'))
#         except Exception as e:
#             print(e)
#             return redirect(url_for('getCart'))

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
     if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
         return redirect(url_for('merch'))
     else:
         session.modified = True
         for key, item in session['Shoppingcart'].items():
                 if int(key) == id:
                     session['Shoppingcart'].pop(key, None)
                     return redirect(url_for('getCart'))


@app.route('/clearcart')
def clearcart():
        session.pop('Shoppingcart', None)
        return redirect(url_for('merch'))

# @app.route('/empty')
# def empty_cart():
#     try:
#         session.clear()
#         return redirect(url_for('merch'))
#     except Exception as e:
#         print(e)

@app.route('/videos')
def videos():
    posts = Post.query.all()
    return render_template('videos.html', posts=posts)


#Classwork    


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

        existing_user = User.query.filter((User.username==username)|(User.email==email)).all()
        if existing_user:
            flash(f'{username} or {email} is already in use. Please register with a new username or email', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(username, email, password)
        
        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you {username}, you have successfully registered!', 'success')

        welcome_msg = Message('Welcome to the Kekambas Blog', [email])
        welcome_msg.body = f'Thank you for signing up {username}'
        mail.send(welcome_msg)

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

@app.route('/logout')
def logout():
    logout_user()
    flash(f'You have successfully logged out!', 'success')
    return redirect(url_for('index'))        

@app.route('/createpost', methods=['GET', 'POST'])
@login_required
def createpost():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_post = Post(title, content, current_user.id)
        db.session.add(new_post)
        db.session.commit()

        flash(f'The post {title} has been created.', 'success')
        return redirect(url_for('videos'))
    return render_template('createpost.html', form=form)

@app.route('/phonebook', methods=['GET', 'POST'])
@login_required
def add_contact():
    form = PhoneBookForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        full_name = first_name + " " + last_name
        address = form.address.data
        phone_number = form.phone_number.data
        

        new_contact = Contact(first_name, last_name, address, phone_number, current_user.id)
        db.session.add(new_contact)
        db.session.commit()
        flash(f'{full_name} has been added to the book.', 'success')
        return redirect(url_for('viewphonebook'))
    return render_template('phonebook.html', form=form)

@app.route('/viewphonebook')
@login_required
def viewphonebook():
    contacts = Contact.query.all()
    return render_template('viewphonebook.html', contacts=contacts)

@app.route('/my-account')
@login_required
def my_account():
    return render_template('my_account.html')

@app.route('/my-posts')
@login_required
def my_posts():
    posts = current_user.posts
    return render_template('my_posts.html', posts=posts)

@app.route('/my-contacts')
@login_required
def my_contacts():
    contacts = current_user.contacts
    return render_template('my_contacts.html', contacts=contacts)


@app.route('/contacts/<int:contact_id>')
def contact_detail(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return render_template('contact_detail.html', contact=contact)

@app.route('/contacts/<int:contact_id>/edit', methods=['GET', 'POST'])    
@login_required
def contact_edit(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if contact.creator.id != current_user.id:
        return redirect(url_for('my_contacts'))

    form = PhoneBookForm()
    if form.validate_on_submit():
        new_first_name = form.first_name.data
        new_last_name = form.last_name.data
        new_address = form.address.data
        new_phone_number = form.phone_number.data
        contact.first_name = new_first_name
        contact.last_name = new_last_name
        contact.address = new_address
        contact.phone_number = new_phone_number

        db.session.commit() 

        flash(f'Contact has been updated')
        return redirect(url_for('contact_detail', contact_id=contact.id))

    return render_template('contact_edit.html', contact=contact, form=form)

@app.route('/contacts/<int:contact_id>/delete', methods=['GET','POST'])
@login_required
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if contact.creator != current_user:
        flash('You can only delete your own posts', 'danger')
        return redirect(url_for('my_contacts'))
    
    db.session.delete(contact)
    db.session.commit()

    flash('Contact removed from phonebook', 'success')
    return redirect(url_for('my_contacts'))

@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != current_user.id:
        return redirect(url_for('my_posts'))
    
    form = PostForm()
    if form.validate_on_submit():
        new_title = form.title.data
        new_content = form.content.data
        post.title = new_title
        post.content = new_content
        db.session.commit()

        flash(f'Post has been updated')
        return redirect(url_for('post_detail', post_id=post.id))

    return render_template('post_edit.html', post=post, form=form)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You can only delete your own posts', 'danger')
        return redirect(url_for('my_posts'))
    
    db.session.delete(post)
    db.session.commit()

    flash('Post has been deleted', 'success')
    return redirect(url_for('my_posts'))

