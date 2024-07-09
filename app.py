from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Product:
    def __init__(self, name, category, price, stock, image_url):
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.image_url = image_url



class RegistrationForm(FlaskForm):
    username = StringField('Ім\'я користувача', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Підтвердити пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зареєструватися')

class LoginForm(FlaskForm):
    email = StringField('Електронна пошта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запам\'ятати мене')
    submit = SubmitField('Увійти')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def home():
    products = [
        Product(
            name='Рис',
            category='Крупи',
            price=1.99,
            stock=100,
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/US_long_grain_rice.jpg/500px-US_long_grain_rice.png'
        ),

        Product(
            name='Пшениця',
            category='Крупи',
            price=2.49,
            stock=150,
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/%D0%9F%D1%88%D0%B5%D0%BD%D0%B8%D1%87%D0%BD%D0%B5_%D0%BF%D0%BE%D0%BB%D0%B5._%D0%97%D0%B0%D0%BF%D0%BE%D1%80%D1%96%D0%B7%D1%8C%D0%BA%D0%B5_%D0%9F%D1%80%D0%B0%D0%B2%D0%BE%D0%B1%D0%B5%D1%80%D0%B5%D0%B6%D0%B6%D1%8F.jpg/250px-%D0%9F%D1%88%D0%B5%D0%BD%D0%B8%D1%87%D0%BD%D0%B5_%D0%BF%D0%BE%D0%BB%D0%B5._%D0%97%D0%B0%D0%BF%D0%BE%D1%80%D1%96%D0%B7%D1%8C%D0%BA%D0%B5_%D0%9F%D1%80%D0%B0%D0%B2%D0%BE%D0%B1%D0%B5%D1%80%D0%B5%D0%B6%D0%B6%D1%8F.png'
        ),

        Product(
            name='Ячмінь',
            category='Крупи',
            price=1.79,
            stock=80,
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Gerstenkorrels_Hordeum_vulgare.jpg/500px-Gerstenkorrels_Hordeum_vulgare.jpg'
        ),

        Product(
            name='Морква',
            category='Овочі',
            price=0.99,
            stock=200,
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/CarrotRoots.jpg/220px-CarrotRoots.png'
        ),

        Product(
            name='Броколі',
            category='Овочі',
            price=1.25,
            stock=120,
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Broccoli2.jpg/265px-Broccoli2.png'
        ),

        Product(
            name='Томат',
            category='Овочі',
            price=1.49,
            stock=180,
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Pomodorini_sulla_pianta.jpg/275px-Pomodorini_sulla_pianta.png'
        ),

        Product(
            name='Яблуко',
            category='Фрукти',
            price=0.89,
            stock=300,
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Fuji_apple.jpg/220px-Fuji_apple.png'
        ),

        Product(
            name='Банан',
            category='Фрукти',
            price=1.10,
            stock=250,
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/%D0%97%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F-Luxor%2C_Banana_Island%2C_Banana_Tree%2C_Egypt%2C_June_2007.jpg/220px-%D0%97%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F-Luxor%2C_Banana_Island%2C_Banana_Tree%2C_Egypt%2C_June_2007.png'
        ),

        Product(
            name='Апельсин',
            category='Фрукти',
            price=1.20,
            stock=220,
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/OrangeBloss_wb.jpg/270px-OrangeBloss_wb.png'
        ),

        Product(
            name='Куряче філе',
            category='М\'ясо',
            price=5.99,
            stock=90,
            image_url='https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcRtOKw7xI684G1Btb4CoqTsFOEI447wId-wSerAOwZg4K_m8NmVFPjqhkK-S6-_SQilLclLnIiAy6Q3QKwWOsS1w3HUZzuWCO0HUwcTdMxrwJN3CyVwL1cs_0Q8tjDf&usqp=CAc.png'
        ),

        Product(
            name='Свиняче філе',
            category='М\'ясо',
            price=6.49,
            stock=70,
            image_url='https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcTUdo-2ZwF3iC30rd6iuEqD6Roetvv8ZaSw6BZAdPbZin48kKnEn14piWLSXnwcNb02NaVRjXKoWdmExa86kmGC_YTa479u_gh99y9SVOYCrW87UD7cYbSzfg&usqp=CAE.png'
        ),

        Product(
            name='Яловичий стейк',
            category='М\'ясо',
            price=8.99,
            stock=60,
            image_url='https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTC5qfcu8IqEW9aGnFFUdaEXgcxmOBBLugtit3L1iwu-XJ-1hw7TvytEAxhAYCvbi9FNJYdxaCVX4sQDW5rksOkUF8QlXkPFq9u92BJv61qx5E2FIRRxliAgA&usqp=CAE.png'
        ),

        Product(
            name='Молоко',
            category='Напої',
            price=1.50,
            stock=180,
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Glass_of_Milk_%2833657535532%29.jpg/274px-Glass_of_Milk_%2833657535532%29.png'
        ),

        Product(
            name='Апельсиновий сік',
            category='Напої',
            price=2.99,
            stock=140,
            image_url='https://images.silpo.ua/products/1600x1600/webp/4d60113d-3564-4e04-9591-87eeabefce62.png'
        ),

        Product(
            name='Вода',
            category='Напої',
            price=0.99,
            stock=500,
            image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT21zAmN8g4HKp_FvfV9AuIRrIECGExkNT8og&usqp=CAUя.png'
        )

    ]
    return render_template('index.html', products=products)

@app.route('/')
def index():
    search_query = request.args.get('search', '')
    category = request.args.get('category', '')
    if category:
        products = Product.query.filter(Product.category == category).all()
    else:
        products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Не вдалося увійти. Перевірте електронну пошту та пароль', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return render_template('register.html', form=form, success_message=f'Account created for {form.username.data}!')
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)