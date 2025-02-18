from flask import Flask
from flask import render_template
from flask_login import LoginManager
from flask import render_template, url_for, redirect, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from forms import RegistrationForm, LoginForm
from models import db, User, Request
from flask_login import current_user


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = 'tvoj_krastny_sigma_klucik'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'teacher':
            return redirect(url_for('teacher_page'))
        elif current_user.role == 'janitor':
            return redirect(url_for('janitor_page'))
    return redirect(url_for('register'))



@app.route("/teacher_dashboard")
@login_required
def teacher_page():
    return render_template("teacher_dashboard.html")


@app.route("/janitor_dashboard")
@login_required
def janitor_page():
    return render_template("janitor_dashboard.html")




@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email už existuje', 'error')
            return redirect(url_for('register'))

        # Assign roles based on user input (for simplicity)
        role = request.form.get("role")  # Get role from form

        new_user = User(username=form.username.data, email=form.email.data, role=role)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrovaný úspešne!', 'success')
        return redirect(url_for('login'))
    

    return render_template('register.html', form=form)







@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Prihlásenie úspešné', 'success')
            return redirect(url_for('home'))
        else:
            flash('Nesprávny email alebo heslo', 'error')

    return render_template('login.html', form=form)






@app.route("/requests")
def requests():
    return render_template('requests.html')


@app.route("/processed_requests")
def processed_requests():
    return render_template('processed_requests.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')





with app.app_context():
    db.create_all()