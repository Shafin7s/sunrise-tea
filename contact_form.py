from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import EmailField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, URL, Regexp, Length
from flask_ckeditor import CKEditorField

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^\d{10}$', message="Enter a valid 10-digit phone number"),
        Length(min=10, max=10)
    ])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')


class LoginForm(FlaskForm):

    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')



class ProductForm(FlaskForm):
    product_heading = StringField('Product Title',validators=[DataRequired()])

    product_subheading = StringField('Product Subheading',validators=[DataRequired()])

    product_description = StringField("Product Description")

    product_img_url = StringField('Product Image',validators=[DataRequired()])

    product_actual_price =StringField('Product Actual Price',validators=[DataRequired()])

    product_discounted_price= StringField('Product Discounted Price',validators=[DataRequired()])

    product_rating= StringField('Product Rating',validators=[DataRequired()])

    submit = SubmitField('Add')


class CreateBlog(FlaskForm):

    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")