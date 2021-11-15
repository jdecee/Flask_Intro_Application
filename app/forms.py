from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileAllowed, FileField, FileRequired 


class UserInfoForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField()

class PhoneBookForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()

class AddProduct(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    colors = TextAreaField('Colors', validators=[DataRequired()])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg','png', 'gif', 'jpeg'])])
    submit = SubmitField()



