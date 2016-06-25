#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import webapp2
import jinja2
import re
import hashlib
from google.appengine.ext import db
import random
import string

template_dir = os.path.join(os.getcwd(), 'Templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


def secret_word():
    secret = ''.join([random.choice(string.letters) for x in range(5)])
    return secret


def hashit(a, b, secret=None):
    if not secret:
        secret = secret_word()
    hashed_password = hashlib.sha256(a + b + secret).hexdigest()
    return '|'.join([hashed_password, secret])


def compare_hashes(user, password, hash):
    secret = hash.split('|')[1]
    return hashit(user, password, secret) == hash


def username_valid(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    search = db.GqlQuery("select * from User where username='%s'" % username)
    if USER_RE.match(username) and search.get() is None:
        return True
    elif not USER_RE.match(username):
        return 1
    else:
        return 2


def password_valid(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return PASS_RE.match(password)


def email_valid(email):
    if not email: return True
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return EMAIL_RE.match(email)


class PageHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))


class User(db.Model):
    username = db.StringProperty(required=True)
    hash_password = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    email = db.StringProperty()


class Logout(PageHandler):
    def get(self):
        self.response.delete_cookie('user')
        self.response.delete_cookie('hash')
        self.redirect('/login')
        pass


class LoginHandler(PageHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        raw_name = self.request.get('username')
        raw_password = self.request.get('password')
        hashed = None
        user_err = ''
        pass_err = ''
        query = db.GqlQuery("select * from User where username='%s'" % raw_name).get()
        if query:
            hashed = query.hash_password
            if compare_hashes(raw_name, raw_password, hashed):
                self.response.headers.add_header('Set-Cookie', str('user=%s' % raw_name))
                self.response.headers.add_header('Set-Cookie', str('hash=%s' % hashed))
                self.redirect('/welcome')
            else:
                pass_err = 'Invalid Password'
                user_err = ''
        else:
            user_err = 'User does not exist'
            pass_err = ''
        self.render("login.html", username=raw_name, pass_error=pass_err, user_error=user_err)


class FormHandler(PageHandler):
    def get(self):
        self.render("signup.html")

    def post(self):
        raw_name = self.request.get('username')
        raw_password = self.request.get('password')
        raw_verify = self.request.get('verify')
        raw_email = self.request.get('email')

        user_check = username_valid(raw_name)
        password = password_valid(raw_password)
        verify = True if raw_password == raw_verify else False
        email = email_valid(raw_email)

        if user_check == True and password and verify and email:
            hash_pass = hashit(raw_name, raw_password)
            self.response.headers.add_header('Set-Cookie', str('user=%s' % raw_name))
            self.response.headers.add_header('Set-Cookie', str('hash=%s' % hash_pass))
            u = User(username=raw_name, hash_password=hash_pass, email=raw_email)
            u.put()
            key = u.key()
            record = User.get(key)
            self.redirect('/welcome')
            # self.redirect('/welcome?username=' + raw_name)
        else:
            user_err = ''
            pass_err = ''
            verify_err = ''
            email_err = ''
            if user_check == 1:
                user_err = "That's not a valid username."
            elif user_check == 2:
                user_err = "User already exists."

            if not verify:
                verify_err = "Your passwords didn't match."

            if not password:
                verify_err = ''
                pass_err = "That wasn't a valid password."

            if not email:
                email_err = "That's not a valid email."

            self.render("signup.html",
                        username=raw_name,
                        email=raw_email,
                        user_error=user_err,
                        pass_error=pass_err,
                        verify_error=verify_err,
                        email_error=email_err)


class Welcome(PageHandler):
    def get(self):
        user = self.request.cookies.get('user', None)
        encrypted = self.request.cookies.get('hash', None)
        if not user and not encrypted:
            self.write('''
            <div style='color:red'>Not logged in<div>
            <a href='/login'>Login</a>
            ''')
        else:
            encrypted_key = db.GqlQuery("select * from User where username='%s'" % user)
            if encrypted == encrypted_key[0].hash_password:
                self.render('welcome.html', user=user)

app = webapp2.WSGIApplication([
    ('/login', LoginHandler),
    ('/signup', FormHandler),
    ('/logout', Logout),
    ('/welcome', Welcome)
], debug=True)
