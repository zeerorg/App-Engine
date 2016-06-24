import os
import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.getcwd(), 'Templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class PageHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))


class Art(db.Model):
    title = db.StringProperty(required=True)
    ascii = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class Congratulations(PageHandler):
    def get(self):
        self.response.write("Congratulations.")

class MainHandler(PageHandler):
    def write_form(self, title='', ascii='', error=''):
        artwork = db.GqlQuery("select * from Art order by created desc")
        self.render("ascii.html", title=title, ascii=ascii, artwork=artwork, error=error)

    def get(self):
        self.write_form()

    def post(self):
        title = self.request.get("title")
        ascii = self.request.get("ascii")

        if title and ascii:
            a = Art(title=title, ascii=ascii)
            a.put()
            key = a.key()
            record = Art.get(key)
            self.redirect('/congo')
        else:
            error = "Invalid entry!! Enter Again"
            self.write_form(title=title, ascii=ascii, error=error)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/congo', Congratulations)
], debug=True)
