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
        user_info = {'name': self.username}
        user_info.update({'dashboards': self.get_dashboards()})
        return user_info

    def add_dashboard(self, dashboard_name, dashboard_url):
        self.db.add_dashboard(self.username, dashboard_name, dashboard_url)
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
        self.query_db("Select count(*) from users where username = '" +
                      username + "' and password = md5('" + password + "')")
        if self.cursor.fetchone():
            return True
        return False

    def get_dashboards(self, username):
        dashboards = {}
        self.query_db("Select name, url from dashboards where username = '" + username + "'")
        for row in self.cursor:
            dashboards.update({row[0]: row[1]})
        return dashboards

    def add_dashboard(self, username, dashboard_name, dashboard_url):
        self.query_db("Insert into dashboards values('" + username + "','" +
                      dashboard_url + "','" + dashboard_name + "')")
