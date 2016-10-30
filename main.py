#!/usr/bin/env python
import os
import jinja2
import webapp2
import math

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        self.render_template("hello.html")


class IzracunHandler(BaseHandler):
    def post(self):

        operacija = self.request.get("vnos")
        if "+" in operacija:
            x = operacija.find('+')
            rezultat = (int(operacija[0:x]) + (int(operacija[x + 1:])))
        if "-" in operacija:
            x = operacija.find('-')
            rezultat = (int(operacija[0:x]) - (int(operacija[x + 1:])))
        if "*" in operacija:
            x = operacija.find('*')
            rezultat = (int(operacija[0:x]) * (int(operacija[x + 1:])))
        if "/" in operacija:
            x = operacija.find('/')
            rezultat = (int(operacija[0:x]) / (int(operacija[x + 1:])))

        params = {"iznos": rezultat}

        self.render_template("izracun.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/izracun', IzracunHandler),
], debug=True)
