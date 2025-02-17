import smtplib
from datetime import date

from flask import Flask, render_template, flash, url_for, redirect, session, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from contact_form import ContactForm, LoginForm, ProductForm, CreateBlog

MY_EMAIL = "khanshafin25@gmail.com"
MY_PASSWORD = "wrozcupzppupqdvj"
app = Flask(__name__)
ckeditor = CKEditor(app)
Bootstrap5(app)


# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# SQLAlchemy Setup
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = "SECRET_KEY"
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'  # Store session in a temporary file

db.init_app(app)

# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

# User Model


class Product(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    product_title: Mapped[str] = mapped_column(String(100),nullable=False)
    product_img : Mapped[str] = mapped_column(nullable=False)
    product_subtitle :Mapped[str] = mapped_column(String(250), nullable=False)
    product_description: Mapped[str] = mapped_column(db.Text,nullable=True)
    actual_price: Mapped[str] = mapped_column(String(20),nullable=True)
    discounted_price: Mapped[str] = mapped_column(String(20),nullable=True)
    product_rating: Mapped[str] = mapped_column(nullable=True)




# User Model
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)  # Admin field


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(db.Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)



# Create database tables
with app.app_context():
    db.create_all()

# Sample Testimonials
testimonials = [
    {"name": "Amit Sharma", "feedback": "Best tea I’ve ever had! The aroma is amazing.", "rating": "⭐⭐⭐⭐⭐"},
    {"name": "Priya Desai", "feedback": "Great taste and fast delivery. Will order again!", "rating": "⭐⭐⭐⭐"},
    {"name": "Rahul Verma", "feedback": "Really loved the packaging and quality of the tea!", "rating": "⭐⭐⭐⭐⭐"},
]

# Home Route
@app.route('/')
def home():
    result = db.session.execute(db.select(Product))
    products = result.scalars().all()

    blogs_results = db.session.execute(db.select(BlogPost))
    blogs = blogs_results.scalars().all()


    return render_template('index.html', testimonials=testimonials,products=products,blogs=blogs)




# User Login/Registration Route
@app.route("/secret-login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if this is the first user
        first_user = User.query.first()
        is_admin = first_user is None  # First user is admin

        new_user = User(
            email=form.email.data,
            password=form.password.data,
            is_admin=True
        )
        if new_user.email == form.email.data and new_user.password ==form.password.data:
            login_user(new_user)
            session.permanent = False  # Auto logout when browser closes
            flash('You have logged in successfully', 'success')
            return redirect(url_for('add_product'))

    return render_template("login.html", form=form)

# Logout Route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()  # Clear session on logout
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

# About Us Route
@app.route("/about-us")
def about_us():
    return render_template('about.html')


# Contact Us Page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        user_name = form.name.data
        user_email = form.email.data
        user_phone = form.phone.data
        user_message = form.message.data

        email_body = f"""
New Inquiry from Sunrise Tea Website:
                
Name: {user_name}
Email: {user_email}
Phone: {user_phone}
                
Message:
{user_message}
                
Please respond at your earliest convenience.
        """

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=user_email,
                    msg=f"Subject: New Contact Form Submission - Sunrise Tea\n"
                        f"{email_body}"
                )

            flash("Your message has been sent! We'll get back to you soon.", "success")
        except Exception as e:
            flash("An error occurred while sending the message. Please try again later.", "danger")
            print(f"Error sending email: {e}")

        return redirect(url_for("home"))

    return render_template("contact.html", form=form)


# Products Page
@app.route('/products')
def products():
    result = db.session.execute(db.select(Product))
    posts = result.scalars().all()
    return render_template('products.html', products=posts)

# Product Details Page
@app.route("/product-details/<int:product_id>")
def product_details(product_id):
    requested_product = db.get_or_404(Product,product_id)

    return render_template("product_details.html",product=requested_product)

# Blog Page
@app.route("/blogs/<int:blog_id>")
def tea_blog(blog_id):
    requested_blog = db.get_or_404(BlogPost,blog_id)
    return render_template("blog_page.html",blog=requested_blog)

@app.route("/new-post", methods=["GET", "POST"])
def add_new_blog():
    form = CreateBlog()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add-blog.html", form=form)



# Add Product Route (Admin Only)
@app.route('/add-product-sunrise-tea', methods=['GET', 'POST'])
# @login_required
def add_product():
    form = ProductForm()



    if form.validate_on_submit():
        product_description = request.form.get("product_description",
                                               "").strip()  # Get user input and remove extra spaces

        if not product_description:  # If empty, assign a default value
            product_description = "No description available"

        new_product = Product(
            product_title = form.product_heading.data,
            product_img = form.product_img_url.data,
            product_subtitle = form.product_subheading.data,
            product_description=product_description,
            actual_price = form.product_actual_price.data,
            discounted_price= form.product_discounted_price.data,
            product_rating=form.product_rating.data
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('products'))


    return render_template('add-product.html',form=form)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
