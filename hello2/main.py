import os
import webapp2
import jinja2

template_dir = os.path.join(os.getcwd(), 'Templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class PageHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, kw))


class MainHandler(PageHandler):
    def get(self):
        items = self.request.get_all('food')
        if items:
            self.render("shopping_list.html", items=items)
        else:
            self.render("shopping_list.html")


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
