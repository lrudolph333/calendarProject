import webapp2
import os
import jinja2
from google.appengine.ext import ndb
from models import *

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class CalendarPage(webapp2.RequestHandler):
    def post(self):
        calendar_template = jinja_env.get_template('templates/calendar.html')
        self.response.headers['Content-Type'] = "text/html"
        self.response.write(calendar_template.render())

class ToDoListPage(webapp2.RequestHandler):
    def post(self):
        to_do_template = jinja_env.get_template('templates/todo.html')
        self.response.headers['Content-Type'] = "text/html"
        self.response.write(to_do_template.render())

class SchedulePage(webapp2.RequestHandler):
    def post(self):
        schedule_template = jinja_env.get_template("/templates/schedule.html")
        self.response.header['Content-Type'] = "text/html"
        self.response.write(schedule_template.render())

class LoginPage(webapp2.RequestHandler):
    def get(self):
        f = open("templates/login.html", "r")
        self.response.headers['Content-Type'] = "text/html";
        self.response.write(f.read())

class ProfilePage(webapp2.RequestHandler):
    def post(self):
        profile_template = jinja2.get_template("/templates/profile.html")
        self.response.headers['Content-Type'] = "text/html"
        id = self.request.get("userID")
        values = {
            "user": UserCredentials.get_by_id(int(id))
        }
        self.response.write(profile_template.render(values))



class LoginParser(webapp2.RequestHandler):
    def post(self):
        username = self.request.get("username");
        password = self.request.get("password");

        self.response.headers['Content-Type'] = "text/plain";

        users = UserCredentials.query().filter(UserCredentials.username == username).fetch();

        if len(users) > 0:
            if users[0].password == password :
                self.response.write(users[0].key.integer_id())
            else :
                self.response.write("Incorrect password")
        else:
            self.response.write("Whoops, that username isn't in our database");

class SignupParser(webapp2.RequestHandler):
    def post(self):
        username = self.request.get("username");
        password = self.request.get("password");
        name = "";

        userAlreadyExists = len(UserCredentials.query().filter(UserCredentials.username == username).fetch()) > 0;
        self.response.headers['Content-Type'] = "text/plain";

        if userAlreadyExists:
            self.response.write("Sorry, that user already exists");
        else:
            newUser = UserCredentials(username=username, password=password);
            key = newUser.put();
            self.response.write(key.integer_id());

class DashboardPage(webapp2.RequestHandler):
    def post(self):
        dashboardTemplate = jinja_env.get_template('templates/dashboard.html');
        self.response.headers['Content-Type'] = "text/html";
        values = {
            "userID": self.request.get("userID"),
            "username": UserCredentials.get_by_id(int(self.request.get("userID"))).username
        }
        self.response.write(dashboardTemplate.render(values));

class LoginCSS(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/css";
        f = open("stylesheet/login.css", "r")
        self.response.write(f.read());

class DashboardCSS(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/css";
        f = open("stylesheet/dashboard.css", "r")
        self.response.write(f.read());

class CalendarCSS(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/css";
        f = open("stylesheet/calendar.css", "r")
        self.response.write(f.read());

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/login', LoginParser),
    ('/signup', SignupParser),
    ('/dashboard.html', DashboardPage),
    ('/calendar.html', CalendarPage),
    ('/stylesheet/calendar.css', CalendarCSS),
    ('/stylesheet/login.css', LoginCSS),
    ('/stylesheet/dashboard.css', DashboardCSS),
    ('/todo.html', ToDoListPage),
    ('/schedule.html', SchedulePage),
    ('/profile.html', ProfilePage),

], debug=True);
