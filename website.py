from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from dataset import data_import, project_data
from Models import all_data_model, industry_model, revenue_model, length_model, contract_model
from models import db, User

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

print("Loading data...")
data = data_import()
P3 = data[0]
zip_codes = data[1]
names = P3['Name'].to_list()
print("Data loaded!")

@app.route("/")
def home():
    return render_template('index.html', team_names=names, logged_in=False)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('tool'))
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('tool'))
        flash('Invalid email or password')
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/tool", methods=['GET', 'POST'])
@login_required
def tool():
    if request.method == "GET":
        return render_template('index.html', team_names=names, logged_in=True)
    else:
        data = request.json
        row = project_data(data, P3, zip_codes)
        if type(row) == type('string'):
            return json.dumps({'error': row})
        all_data = round(all_data_model(row), 2)
        industry = round(industry_model(row), 2)
        revenue = round(revenue_model(row), 2)
        length = round(length_model(row), 2)
        contract = round(contract_model(row), 2)
        avg = round((all_data + industry + revenue + length + contract) / 5, 2)
        if avg < .604177:
            result = 'in bottom 1/4 of teams'
        elif avg < 1.205:
            result = 'in 2nd quartile of teams'
        elif avg < 2.39:
            result = 'in 3rd quartile of teams'
        else:
            result = 'in top 1/4 of teams'
        return json.dumps({
            'Overall': str(all_data),
            'Industry': str(industry),
            'Revenue': str(revenue),
            'Length': str(length),
            'Contract': str(contract),
            'Average': str(avg),
            'Result': result
        })

@app.route("/admin")
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('tool'))
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route("/admin/toggle/<int:user_id>")
@login_required
def toggle_admin(user_id):
    if not current_user.is_admin:
        return redirect(url_for('tool'))
    user = User.query.get(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
