# -*- coding: utf-8 -*-
import os
import logging

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# Import packages from the project
import mc
from models import *
from tools import *


tdir = os.path.join(os.path.dirname(__file__), '../templates/')
_DEBUG = True


class BaseRequestHandler(webapp.RequestHandler):
  """Supplies a common template generation function.

  When you call generate(), we augment the template variables supplied with
  the current user in the 'user' variable and the current webapp request
  in the 'request' variable.
  """
  def generate(self, template_name, template_values={}):
    values = {
      'request': self.request,
      'user': users.get_current_user(),
      'prefs': UserPrefs.from_user(users.get_current_user()),
      'login_url': users.create_login_url(self.request.uri),
      'logout_url': users.create_logout_url(self.request.uri),
      'application_name': 'App Engine Boilerplate',
    }
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join(tdir, template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))

  def head(self, *args):
    pass

  def get(self, *args):
    pass

  def post(self, *args):
    pass


# OpenID Login
class LogIn(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        action = decode(self.request.get('action'))
        target_url = decode(self.request.get('continue'))
        if action and action == "verify":
            f = decode(self.request.get('openid_identifier'))
            url = users.create_login_url(target_url, federated_identity=f)
            self.redirect(url)
        else:
            self.response.out.write(template.render(tdir + "login.html", \
                    {"continue_to": target_url}))


class LogOut(webapp.RequestHandler):
    def get(self):
        url = users.create_logout_url("/")
        self.redirect(url)


# Custom sites
class Main(BaseRequestHandler):
    def get(self):
        self.generate("base.html", {})


class Account(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        prefs = UserPrefs.from_user(user)
        self.response.out.write(template.render(tdir + "index.html", \
                {"prefs": prefs}))
