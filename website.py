from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from dataset import data_import, project_data
from Models import (cim_model, fpm_model, get_person_data,
                    cim_industry_model, fpm_industry_model,
                    cim_contract_model, fpm_contract_model)
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

        industry = data['industry']
        contract = data['contract']
        length   = int(data['length'].replace(',', ''))
        project  = {'industry': industry, 'contract': contract, 'length': length}

        # --- Row 1: Industry ---
        ind_cim = round(cim_industry_model(industry), 4)
        ind_fpm = round(fpm_industry_model(industry), 4)

        # --- Row 2: Contract Type ---
        con_cim = round(cim_contract_model(contract), 4)
        con_fpm = round(fpm_contract_model(contract), 4)

        # --- collect PM and Sup names ---
        pm_names  = []
        sup_names = []
        all_members = []

        for i in range(1, 11):
            name = data.get(f'name_{i}', '')
            role = data.get(f'role_{i}', '')
            if name != '':
                all_members.append({'name': name, 'role': role})
                if role == 'PM':
                    pm_names.append(name)
                elif role == 'Sup':
                    sup_names.append(name)

        # --- Row 3: Project Manager ---
        if pm_names:
            pm_cims = [cim_model(get_person_data(n, 'PM', P3, project)) for n in pm_names]
            pm_fpms = [fpm_model(get_person_data(n, 'PM', P3, project)) for n in pm_names]
            pm_cim = round(sum(pm_cims) / len(pm_cims), 4)
            pm_fpm = round(sum(pm_fpms) / len(pm_fpms), 4)
        else:
            pm_cim = round(cim_model(get_person_data(None, 'PM', P3, project)), 4)
            pm_fpm = round(fpm_model(get_person_data(None, 'PM', P3, project)), 4)

        # --- Row 4: Superintendent ---
        if sup_names:
            sup_cims = [cim_model(get_person_data(n, 'Sup', P3, project)) for n in sup_names]
            sup_fpms = [fpm_model(get_person_data(n, 'Sup', P3, project)) for n in sup_names]
            sup_cim = round(sum(sup_cims) / len(sup_cims), 4)
            sup_fpm = round(sum(sup_fpms) / len(sup_fpms), 4)
        else:
            sup_cim = round(cim_model(get_person_data(None, 'Sup', P3, project)), 4)
            sup_fpm = round(fpm_model(get_person_data(None, 'Sup', P3, project)), 4)

        # --- Row 5: Team (all members averaged) ---
        team_cims = [cim_model(get_person_data(m['name'], m['role'], P3, project)) for m in all_members]
        team_fpms = [fpm_model(get_person_data(m['name'], m['role'], P3, project)) for m in all_members]
        team_cim = round(sum(team_cims) / len(team_cims), 4)
        team_fpm = round(sum(team_fpms) / len(team_fpms), 4)

        # --- Row 6: All Factors (average of all 5 rows) ---
        all_cim = round((ind_cim + con_cim + pm_cim + sup_cim + team_cim) / 5, 4)
        all_fpm = round((ind_fpm + con_fpm + pm_fpm + sup_fpm + team_fpm) / 5, 4)

        # --- Summary Section ---
        def get_person_summary(name):
            row = P3[P3["Name"] == name].iloc[0]
            def safe(val):
                return round(float(val), 1) if str(val) != "nan" else "N/A"
            return {
                "name": name.title(),
                "Pri_D": safe(row["Pri_D"]),
                "Pri_E": safe(row["Pri_E"]),
                "Pri_P": safe(row["Pri_P"]),
                "Pri_C": safe(row["Pri_C"]),
                "Cons": safe(row["Cons"]),
                "Env_D": safe(row["Env_D"]),
                "Env_E": safe(row["Env_E"]),
                "Env_P": safe(row["Env_P"]),
                "Env_C": safe(row["Env_C"]),
                "High_Trait": str(row["High_Trait"]),
                "Low_Trait": str(row["Low_Trait"]),
                "Decision_Style": str(row["Decision_Style"]),
                "Leadership_Style": str(row["Leadership_Style"]),
                "Learning_Style": str(row["Learning_Style"]) if str(row["Learning_Style"]) != "nan" else "N/A",
                "Activist": safe(row["Activist"]),
                "Reflector": safe(row["Reflector"]),
                "Theorist": safe(row["Theorist"]),
                "Pragmatist": safe(row["Pragmatist"]),
                "Stress_Level": safe(row["Stress_Level"]),
                "Energy_Level": safe(row["Energy_Level"]),
                "Proactivity_Score": safe(row["Proactivity_Score"]),
                "Self_Monitoring_Score": safe(row["Self_Monitoring_Score"]),
            }

        pm_summary = get_person_summary(pm_names[0]) if pm_names else None
        sup_summary = get_person_summary(sup_names[0]) if sup_names else None

        numeric_cols = ["Pri_D", "Pri_E", "Pri_P", "Pri_C", "Cons",
                        "Env_D", "Env_E", "Env_P", "Env_C",
                        "Activist", "Reflector", "Theorist", "Pragmatist",
                        "Stress_Level", "Energy_Level", "Proactivity_Score", "Self_Monitoring_Score"]
        team_summary = {}
        for col in numeric_cols:
            vals = []
            for m in all_members:
                v = P3[P3["Name"] == m["name"]][col].iloc[0]
                if str(v) != "nan":
                    vals.append(float(v))
            team_summary[col] = round(sum(vals) / len(vals), 1) if vals else "N/A"

        styles = [str(P3[P3["Name"] == m["name"]]["Learning_Style"].iloc[0]) for m in all_members]
        styles = [s for s in styles if s != "nan"]
        team_summary["Learning_Style"] = max(set(styles), key=styles.count) if styles else "N/A"

        # --- Results based on Alexa's quartile thresholds ---
        def cim_result(val):
            if val < -0.00939:
                return 'Bottom 1/4 of teams'
            elif val < 0.01803:
                return '2nd quartile of teams'
            elif val < 0.07517:
                return '3rd quartile of teams'
            else:
                return 'Top 1/4 of teams'

        def fpm_result(val):
            if val < 0.09019:
                return 'Bottom 1/4 of teams & projects'
            elif val < 0.15883:
                return '2nd quartile of teams & projects'
            elif val < 0.24343:
                return '3rd quartile of teams & projects'
            else:
                return 'Top 1/4 of teams & projects'

        return json.dumps({
            'industry_cim':  str(ind_cim),
            'industry_fpm':  str(ind_fpm),
            'contract_cim':  str(con_cim),
            'contract_fpm':  str(con_fpm),
            'pm_cim':        str(pm_cim),
            'pm_fpm':        str(pm_fpm),
            'sup_cim':       str(sup_cim),
            'sup_fpm':       str(sup_fpm),
            'team_cim':      str(team_cim),
            'team_fpm':      str(team_fpm),
            'all_cim':       str(all_cim),
            'all_fpm':       str(all_fpm),
            'cim_result':    cim_result(all_cim),
            'fpm_result':    fpm_result(all_fpm),
            'pm_summary':    pm_summary,
            'sup_summary':   sup_summary,
            'team_summary':  team_summary,
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
