from flask import Flask
from flask import render_template


app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clanky.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)

app.secret_key = 'tvoj_krastny_sigma_klucik'


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/requests")
def requests():
    return render_template('requests.html')


@app.route("/processed_requests")
def processed_requests():
    return render_template('processed_requests.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')