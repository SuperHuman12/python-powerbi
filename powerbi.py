from flask import Flask, render_template, request, redirect, url_for
from userdashboard import DashboardUser, DashboardDB
import json

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
    if DashboardUser.is_login():
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    if not DashboardUser.is_login() and db.validate_user(request.form['username'], request.form['password']):
        user = DashboardUser(request.form['username'], db)
        user.set_session()
        return index(user=user)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# @app.route('/dashboard', methods=['GET'])
# def dashboard():
#     return render_template('dashboard.html', dashboards=get_user_dashboards(session['username']))
#
#
# @app.route('/add-dashboard', methods=['POST'])
# def add_dashboard():
#     dashboard_name = request.form['dashboard-name']
#     url = request.form['dashboard-url']
#     return json.dumps(add_dashboard(dashboard_name, url))
#
#
# def add_dashboard(dashboard_name, dashboard_url):
#     cursor = mysql.connect().cursor()
#     cursor.execute("Insert into dashboards values('" + session['username'] + "','" + dashboard_url + "','"+ dashboard_name + "')")
#
#
# @app.route("/signout", methods=['POST'])
# def logout():
#     session.pop('username')
#     return redirect(render_template('index.html'))
#
# def get_user_dashboards(username):
#     dashboards = {}
#     cursor = mysql.connect().cursor()
#     cursor.execute("Select * from dashboards where username = '" + username + "'")
#     for row in cursor:
#         dashboards.update({row[2]: row[1]})
#     return dashboards
#
#
# def validate_login(username, password):
#     cursor = mysql.connect().cursor()
#     cursor.execute("Select count(*) from users where username = '"
#           + username + "' and password = md5('" + password + "')")
#     if cursor.fetchone():
#         return True
#     return False


if __name__ == '__main__':
    app.run(threaded=True)
