import os
import webapp2
import jinja2
import re
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


class SinglePost(PageHandler):
    def get(self, id):
        id = int(id)
        key = db.Key.from_path('BlogPost', id)
        posts = BlogPost.get(key)
        self.render("home_page.html", posts=[posts])


class BlogPost(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class MainHandler(PageHandler):
    def get(self):
        posts = db.GqlQuery("select * from BlogPost order by created desc")
        self.render("home_page.html", posts=posts)


class FormHandler(PageHandler):
    def get(self):
        self.render("form.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = BlogPost(subject=subject, content=content)
            p.put()
            key = p.key()
            record = BlogPost.get(key)
            id = record.key().id()
            print str(id)
            self.redirect("/blog/%s" % str(id))
            # self.redirect("/blog")

        else:
            error = "Invalid Entry! Try Again."
            self.render("form.html", error=error, subject=subject, content=content)


app = webapp2.WSGIApplication([
    ('/blog/?', MainHandler),
    ('/blog/newpost', FormHandler),
    ('/blog/([0-9]+)', SinglePost)
], debug=True)
