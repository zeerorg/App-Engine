import webapp2
import jinja2
import os

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

class FirstBoot(PageHandler):
    def get(self):
        self.render("boots.html")
        
class SecondBoot(PageHandler):
    def get(self):
        self.render("boots2.html")
    

app = webapp2.WSGIApplication([
    ('/boot1', FirstBoot),
    ('/boot2', SecondBoot)
], debug=True)