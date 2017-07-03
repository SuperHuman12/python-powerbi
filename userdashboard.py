from flaskext.mysql import MySQL


class DashboardUser(object):

    def __init__(self, username, db):
        self.username = username
        self.db = db

    def set_username(self, username):
        self.username = username

    def get_dashboards(self):
        return self.db.get_dashboards(self.username)

    def serialize(self):
        user_info = {'name': self.username,
                     'dashboards': self.get_dashboards(),
                     'is_admin': self.username == 'admin'
                     }
        return user_info

    def add_user(self, new_username, password, brand_name='', parent_company='', status=''):
        self.db.add_user(new_username, password, brand_name, parent_company, status)

    def add_dashboard(self, username, url, msg_dashboard):
        self.db.add_dashboard(username, url, msg_dashboard)


class DashboardDB(MySQL):
    cursor = None

    def __init__(self):
        super(DashboardDB, self).__init__()

    def connect(self):
        self.cursor = super(DashboardDB, self).connect().cursor()

    def query_db(self, query):
        return self.cursor.execute(query)

    def add_user(self, new_username, password, brand_name='', parent_company='', status=''):
        self.query_db("INSERT INTO users (username, password, brand_name, parent_company, status) VALUES ('" +
                      new_username + "',md5('" + password + "'),'" + brand_name + "','" + parent_company + "','" +
                      status + "')")

    def validate_user(self, username, password):
        self.query_db("Select count(*) from users where username = '" +
                      username + "' and password = md5('" + password + "')")
        if self.cursor.fetchone()[0] == 1:
            return True
        return False

    def get_dashboards(self, username):
        dashboards = {}
        self.query_db("Select username, url, msg_dashboard from dashboards where username = '" + username + "'")
        for row in self.cursor:
            dashboards.update({row[2]: row[1]})
        return dashboards

    def add_dashboard(self, username, dashboard_url, msg_dashboard):
        self.query_db("INSERT INTO dashboards (username, url, msg_dashboard) VALUES ('" + username + "','" +
                      dashboard_url + "','" + msg_dashboard + "')")
