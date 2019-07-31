import webapp2
import os
import jinja2
from google.appengine.ext import ndb
from datetime import datetime
from datetime import timedelta
from models import *

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class CalendarPage(webapp2.RequestHandler):
    def post(self):
        calendar_template = jinja_env.get_template('templates/calendar.html')
        self.response.headers['Content-Type'] = "text/html"
        values = {
            "userID": self.request.get("userID"),
            "username": self.request.get("username")
        }
        self.response.write(calendar_template.render(values));

class ToDoListPage(webapp2.RequestHandler):
    def post(self):
        to_do_template = jinja_env.get_template('templates/todo.html')
        self.response.headers['Content-Type'] = "text/html"
        id = self.request.get("userID")
        values = {
            "user": UserCredentials.get_by_id(int(id))
        }
        self.response.write(to_do_template.render(values))

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
        profile_template = jinja_env.get_template("/templates/profile.html")
        self.response.headers['Content-Type'] = "text/html"
        id = self.request.get("userID")
        userDict = UserCredentials.get_by_id(int(id))
        realName = self.request.get("realName")
        userDict.realName = realName
        if len(userDict.realName) == 0:
            realName = self.request.get("realName")
            userDict.realName = realName
        else:
            userDict.realName
        userDict.put()
        values = {
            "user": userDict,
        }
        self.response.write(profile_template.render(values))

class CalItemParser(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = "text/plain";

        time = self.request.get("time");
        date = self.request.get("date");
        title = self.request.get("title");
        location = self.request.get("location");
        ownerID = self.request.get("userID");

        newCalItem = CalendarItem(time=time, date=date, title=title, location=location, ownerID=ownerID);
        key = newCalItem.put();
        self.response.write(key.integer_id());

class LoginParser(webapp2.RequestHandler):
    def post(self):
        username = self.request.get("username");
        password = self.request.get("password");
        realName = ""

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
            "username": UserCredentials.get_by_id(int(self.request.get("userID"))).username,
            "realName": self.request.get("realName"),
        }
        self.response.write(dashboardTemplate.render(values));

class LoginCSS(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/css";
        f = open("stylesheet/login.css", "r")
        self.response.write(f.read());

class NewCalendarItemPage(webapp2.RequestHandler):
    def post(self):
        dashboardTemplate = jinja_env.get_template('templates/newCalendarItem.html');
        self.response.headers['Content-Type'] = "text/html";
        values = {
            "userID": self.request.get("userID"),
            "username": self.request.get("username"),
        }
        self.response.write(dashboardTemplate.render(values));

class NewCalendarItemCSS(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/css";
        f = open("stylesheet/newCalendarItem.css", "r")
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

class QueryParser(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = "text/plain";
        filterBy = self.request.get("filterBy");
        filter = self.request.get("filter");
        if filterBy == "week":
            startDate = datetime.strptime(filter, "%m/%d/%Y");
            dates = [];
            events = [];

            for i in range(0, 7):
                dates.append(startDate);
                startDate += timedelta(days=1);

            for date in dates:
                startMonth = str(date.month);
                startYear = str(date.year);
                startDay = str(date.day);
                if(len(startMonth) == 1) :
                    startMonth = "0" + startMonth;
                    if(len(startDay) == 1) :
                        startDay = "0" + startDay;

                dateString = startMonth + "/" + startDay + "/" + startYear;

                eventList = CalendarItem.query().filter(CalendarItem.date == dateString).fetch();

                dayEvents = [];

                for event in eventList:
                    currentEvent = {
                        "date": str(event.date),
                        "location": str(event.location),
                        "title": str(event.title),
                        "time": str(event.time)
                    }
                    dayEvents.append(currentEvent);

                events.append(dayEvents);

            self.response.write(events);

class SearchCalParser(webapp2.RequestHandler):
    def post(self):

        title = self.request.get("title");
        date = self.request.get("date");
        time = self.request.get("time");
        location = self.request.get("location");

        query = CalendarItem.query();

        if title != '':
            query = query.filter(CalendarItem.title == title);

        if date != '':
            query = query.filter(CalendarItem.date == date);

        if time != '':
            query = query.filter(CalendarItem.time == time);

        if location != '':
            query = query.filter(CalendarItem.location == location);

        response = query.fetch();

        events = [];

        for event in response:

            data = {
                "title": str(event.title),
                "location": str(event.location),
                "date": str(event.date),
                "time": str(event.time)
            }

            events.append(data);

        self.response.headers['Content-Type'] = "text/plain";
        self.response.write(str(events));

class SearchCalPage(webapp2.RequestHandler):
    def post(self):
        dashboardTemplate = jinja_env.get_template('templates/searchCal.html');
        self.response.headers['Content-Type'] = "text/html";
        values = {
            "userID": self.request.get("userID"),
            "username": self.request.get("username"),
        }
        self.response.write(dashboardTemplate.render(values));

class SearchCalCSS(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/css";
        f = open("stylesheet/searchCal.css", "r")
        self.response.write(f.read());

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/login', LoginParser),
    ('/signup', SignupParser),
    ('/addCalItem', CalItemParser),
    ('/queryparser', QueryParser),
    ('/dashboard.html', DashboardPage),
    ('/calendar.html', CalendarPage),
    ('/stylesheet/calendar.css', CalendarCSS),
    ('/newCalendarItem.html', NewCalendarItemPage),
    ('/stylesheet/newCalendarItem.css', NewCalendarItemCSS),
    ('/stylesheet/login.css', LoginCSS),
    ('/stylesheet/dashboard.css', DashboardCSS),
    ('/todo.html', ToDoListPage),
    ('/schedule.html', SchedulePage),
    ('/profile.html', ProfilePage),
    ('/searchCal.html', SearchCalPage),
    ('/stylesheet/searchCal.css', SearchCalCSS),
    ('/searchCalParser', SearchCalParser)

], debug=True);
