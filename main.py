import webapp2
import jinja2
import os

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class LoginPage(webapp2.RequestHandler):
    def get(self):
        login_template = jinja_env.get_template('login.html');
        self.response.write(login_template.render())

app = webapp2.WSGIApplication([
    ('/', LoginPage),
], debug=True);
