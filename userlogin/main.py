from login import LoginHandler
from form import FormHandler
from welcome import Welcome
from logout import Logout
import webapp2

app = webapp2.WSGIApplication([
    ('/login', LoginHandler),
    ('/signup', FormHandler),
    ('/logout', Logout),
    ('/welcome', Welcome)
], debug=True)