from flask import Flask, render_template, request, redirect, url_for, session
from userdashboard import DashboardUser, DashboardDB


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'powerbi'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
db = DashboardDB()
db.init_app(app)
db.connect()


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    if 'username' not in session and db.validate_user(request.form['username'], request.form['password']):
        session['username'] = request.form['username']
        return index()


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', user_info=DashboardUser(session['username'], db).serialize())
    else:
        index()


@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/add-dashboard', methods=['POST'])
def add_dashboard():
    if 'username' in session:
        user_info = DashboardUser(session['username'], db)
        user_info.add_dashboard(request.form['dashboard-name'], request.form['dashboard-url'])
        return "Success"
    else:
        index()


@app.route('/logout', methods=['POST'])
def logout():
    if 'username' in session:
        session.pop('username')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(threaded=True)
