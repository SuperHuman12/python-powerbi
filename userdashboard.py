from flask import session
from flaskext.mysql import MySQL


class DashboardUser(object):

    def __init__(self, username, db):
        self.username = username
        self.db = db

    def set_session(self):
        session['username'] = self.username

    def unset_session(self):
        session.pop('username')

    def get_dashboards(self):
        self.db.get_dashboards(self.username)

    @staticmethod
    def is_login():
        return 'username' in session

    # def add_dashboard(self, dashboard_name, dashboard_url):
    #     self.query_db("Insert into dashboards values ('" + self.username + "','" + dashboard_name
    #                   + "','" + dashboard_url + "')")


class DashboardDB(MySQL):
    cursor = None

    def __init__(self):
        super(DashboardDB, self).__init__()

    def connect(self):
        self.cursor = super(DashboardDB, self).connect().cursor()

    def query_db(self, query):
        return self.cursor.execute(query)

    def validate_user(self, username, password):
        self.query_db("Select count(*) from users where username = '" + username + "' and password = md5('" + password + "')")
        if self.cursor.fetchone():
            return True
        return False

    def get_dashboards(self, username):
        dashboards = {}
        self.query_db("Select name, url from dashboards where username = '" + username + "'")
        for row in self.cursor:
            dashboards.update({row[0]: row[1]})
        return dashboards
