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
            "username": self.request.get("username"),
            "realName": self.request.get("realName"),
        }
        self.response.write(calendar_template.render(values));

class ToDoListPage(webapp2.RequestHandler):
    def post(self):
        to_do_template = jinja_env.get_template('templates/todo.html')
        self.response.headers['Content-Type'] = "text/html"
        id = self.request.get("userID")
        itemList = ToDoItem.query().filter(ToDoItem.ownerID == id).order(-ToDoItem.urgency).fetch()
        userDict = UserCredentials.get_by_id(int(id))
        values = {
            "user": userDict,
            "toDoItems": itemList,
        }
        self.response.write(to_do_template.render(values))

class toDoListCSS(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/css";
        f = open("stylesheet/todo.css", "r")
        self.response.write(f.read());

class viewToDoItemPage(webapp2.RequestHandler):
    def post(self):
        view_item_template = jinja_env.get_template('templates/viewItem.html')
        self.response.headers['Content-Type'] = "text/html"
        id = self.request.get("userID");
        toDoItem = ToDoItem.get_by_id(int(self.request.get("itemID")));
        userDict = UserCredentials.get_by_id(int(id))
        values = {
            "user": userDict,
            "toDoItem": toDoItem,
        }
        self.response.write(view_item_template.render(values))

class addToDoItemParser(webapp2.RequestHandler):
    def post(self):
        to_do_template = jinja_env.get_template('templates/newToDoItem.html')
        self.response.headers['Content-Type'] = "text/html"
        id = self.request.get("userID")
        userDict = UserCredentials.get_by_id(int(id))
        urgencyMap = {
            "red": 3,
            "orange": 2,
            "yellow": 1,
        }

        if self.request.get("time") :

            newItem = ToDoItem(time =self.request.get("time"),
                           date =self.request.get("date"),
                           name=self.request.get("name"),
                           urgency=urgencyMap.get(self.request.get("urgency")),
                           note=self.request.get("note"),
                           ownerID=id)
            newItem.put()
        values = {
            "user": userDict,
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

        username = self.request.get("username");
        password = self.request.get("password");
        realName = self.request.get("realName");

        user = UserCredentials.get_by_id(int(id));

        user.username = username;
        user.realName = realName;

        if(password) :
            user.password = password;
        else:
            password = user.password;

        user.put();

        values = {
            "username": username,
            "password": password,
            "realName": realName,
            "userID": id
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
            newUser = UserCredentials(username=username, password=password, realName=username);
            key = newUser.put();
            self.response.write(key.integer_id());

class DashboardPage(webapp2.RequestHandler):
    def post(self):
        dashboardTemplate = jinja_env.get_template('templates/dashboard.html');
        self.response.headers['Content-Type'] = "text/html";
        values = {
            "userID": self.request.get("userID"),
            "username": UserCredentials.get_by_id(int(self.request.get("userID"))).username,
            "realName": UserCredentials.get_by_id(int(self.request.get("userID"))).realName,
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
            "realName": self.request.get("realName"),
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
        userID = self.request.get("userID");

        if filterBy == "clearAll":
            eventList = CalendarItem.query().filter(CalendarItem.ownerID == userID).fetch();

            for event in eventList:
                event.key.delete();

            self.response.write("Success");

        elif filterBy == "week":
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

                eventList = CalendarItem.query().filter(CalendarItem.date == dateString).filter(CalendarItem.ownerID == userID).fetch();

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
        userID = self.request.get("userID");

        query = CalendarItem.query();

        if title != '':
            query = query.filter(CalendarItem.title == title);

        if date != '':
            query = query.filter(CalendarItem.date == date);

        if time != '':
            query = query.filter(CalendarItem.time == time);

        if location != '':
            query = query.filter(CalendarItem.location == location);

        query = query.filter(CalendarItem.ownerID == userID);

        response = query.fetch();

        events = [];

        for event in response:

            data = {
                "title": str(event.title),
                "location": str(event.location),
                "date": str(event.date),
                "time": str(event.time),
                "id": str(event.key.integer_id())
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
            "realName": self.request.get("realName"),
        }
        self.response.write(dashboardTemplate.render(values));

class SearchCalCSS(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/css";
        f = open("stylesheet/searchCal.css", "r")
        self.response.write(f.read());

class AboutPage(webapp2.RequestHandler):
    def post(self):
        dashboardTemplate = jinja_env.get_template('templates/aboutUs.html');
        self.response.headers['Content-Type'] = "text/html";
        values = {
            "userID": self.request.get("userID"),
            "username": self.request.get("username"),
            "realName": self.request.get("realName"),
        }
        self.response.write(dashboardTemplate.render(values));

class AboutCSS(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/css";
        f = open("stylesheet/aboutUs.css", "r")
        self.response.write(f.read());

class NotificationsPage(webapp2.RequestHandler):
    def post(self):
        dashboardTemplate = jinja_env.get_template('templates/notifications.html');
        self.response.headers['Content-Type'] = "text/html";

        userID = self.request.get("userID")
        username = self.request.get("username")
        realName = self.request.get("realName")
        date = self.request.get("date");

        parseDate = datetime.strptime(date, "%m/%d/%Y %H:%M");

        query1 = ToDoItem.query().filter(ToDoItem.ownerID == userID);
        query2 = CalendarItem.query().filter(CalendarItem.ownerID == userID);
        TodoItems = query1.fetch();
        TodoItems2 = [];
        CalendarItems = query2.fetch();
        CalendarItems2 = [];

        for item in TodoItems:

            time = (datetime.strptime(str(item.date) + " " + str(item.time), "%Y-%m-%d %H:%M") - parseDate).total_seconds();

            if time < 24 * 60 * 60 and time > 0:
                TodoItems2.append(item)

        for item in CalendarItems:
            time = (datetime.strptime(str(item.date) + " " + str(item.time), "%m/%d/%Y %H:%M") - parseDate).total_seconds();

            if time < 24 * 60 * 60 and time > 0:
                CalendarItems2.append(item);

        item1 = [];
        item2 = [];

        for item in CalendarItems2:
            value = {
                "time": str(item.time),
                "date": str(item.date),
                "title": str(item.title),
                "location": str(item.location)
            }
            item2.append(value);

        for item in TodoItems2:
            value = {
                "time": str(item.time),
                "date": str(item.date),
                "name": str(item.name),
                "urgency": str(item.urgency),
                "note": str(item.note)
            }
            item1.append(value);

        values = {
            "userID": userID,
            "username": username,
            "realName": realName,
            "TodoItems": item1,
            "CalendarItems": item2,
        }
        self.response.write(dashboardTemplate.render(values));

class NotificationsCSS(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/css";
        f = open("stylesheet/notifications.css", "r")
        self.response.write(f.read());

class ProfileCSS(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/css";
        f = open("stylesheet/profile.css", "r")
        self.response.write(f.read());

class NewToDoItemCSS(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/css";
        f = open("stylesheet/newToDoItem.css", "r")
        self.response.write(f.read());

class ViewItemCSS(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/css";
        f = open("stylesheet/viewItem.css", "r")
        self.response.write(f.read());

class Favicon(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "image/x-icon";
        f = open("favicon.ico", "r")
        self.response.write(f.read());

class pic1(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "image/jpeg";
        f = open("templates/IMG_6487.JPG", "r")
        self.response.write(f.read());

class pic3(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "image/jpeg";
        f = open("templates/IMG3050.JPG", "r")
        self.response.write(f.read());

class pic2(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "image/png";
        f = open("templates/mikeyimage.png", "r")
        self.response.write(f.read());

class ToDoDelete(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = "text/plain";

        itemID = self.request.get("id");

        item = ToDoItem.get_by_id(int(itemID));

        item.key.delete();

        self.response.write("Success");

class CalDelete(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = "text/plain";

        itemID = self.request.get("id");

        item = CalendarItem.get_by_id(int(itemID));

        item.key.delete();

        self.response.write("Success");

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/deleteToDoItem', ToDoDelete),
    ('/deleteCalItem', CalDelete),
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
    ('/stylesheet/todo.css', toDoListCSS),
    ('/schedule.html', SchedulePage),
    ('/profile.html', ProfilePage),
    ('/searchCal.html', SearchCalPage),
    ('/stylesheet/searchCal.css', SearchCalCSS),
    ('/notifications.html', NotificationsPage),
    ('/stylesheet/notifications.css', NotificationsCSS),
    ('/aboutUs.html', AboutPage),
    ('/stylesheet/aboutUs.css', AboutCSS),
    ('/stylesheet/profile.css', ProfileCSS),
    ('/stylesheet/viewItem.css', ViewItemCSS),
    ('/stylesheet/newToDoItem.css', NewToDoItemCSS),
    ('/searchCalParser', SearchCalParser),
    ('/addToDoItem', addToDoItemParser),
    ('/favicon.ico', Favicon),
    ('/viewItem.html', viewToDoItemPage),
    ('/templates/IMG_6487.JPG', pic1),
    ('/templates/mikeyimage.png', pic2),
    ('/templates/IMG3050.JPG', pic3)

], debug=True);
