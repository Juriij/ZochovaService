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
        # If the user is logged in (teacher or janitor), show the index page
        return render_template('index.html')
    return redirect(url_for('register'))  # If not authenticated, redirect to the registration page




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
@login_required
def requests():
    if current_user.role != 'teacher':
        flash('Access denied: Only teachers can view this page.', 'error')
        return redirect(url_for('home'))  
    
    active_requests = Request.query.order_by(Request.priority.desc()).all()
    return render_template('requests.html', active_requests=active_requests)








@app.route('/add_request', methods=['GET', 'POST'])
def add_request():
    active_requests = Request.query.order_by(Request.priority.desc()).all()

    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        place = request.form.get('place')
        priority = request.form.get('priority')

        # Create a new request object
        new_request = Request(title=title, description=description, place=place, priority=priority)

        # Add to database
        db.session.add(new_request)
        db.session.commit()

        active_requests = Request.query.order_by(Request.priority.desc()).all()

        # Optionally, flash a message or redirect
        flash('Request submitted successfully!', 'success')


    return render_template('requests.html', active_requests=active_requests)





@app.route("/request/<int:request_id>")
@login_required
def view_request(request_id):
    # Fetch the request by its ID
    request = Request.query.get_or_404(request_id)
    
    # Render the full request details on a separate page
    return render_template('view_request.html', request=request)




@app.route("/processed_requests")
@login_required
def processed_requests():
    return render_template('processed_requests.html')



@app.route("/admin")
@login_required
def admin():
    if current_user.role != 'janitor':
        flash('Access denied: Only janitors can view this page.', 'error')
        return redirect(url_for('index'))  # Redirect to the index page if not a janitor
    return render_template('admin.html')




with app.app_context():
    db.create_all()