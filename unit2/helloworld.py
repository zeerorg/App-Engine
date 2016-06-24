import webapp2
import cgi
import re

form = """
<h1>Enter some text to ROT13:</h1>
<form method="post">
    <textarea name="data" rows='8' cols='60'>%(data)s</textarea>
    <br>
    <input type="submit">
</form>
"""

user_form = """
<form method="post">
    <h1>Signup</h1>
    <label>
        Name
        <input name='username' value="%(name)s">
    </label>
    <font color="red">%(nameErr)s</font> <br>
    <label>
        Password
        <input type='password' name='password'>
    </label>
    <font color="red">%(passErr)s</font> <br>
    <label>
        Verify Password
        <input type='password' name='verify'>
    </label>
    <font color="red">%(verifyErr)s</font> <br>
    <label>
        Email(Optional)
        <input name='email' value="%(email)s">
    </label>
    <font color="red">%(emailErr)s</font> <br>
    <input type='submit'>
</form>
"""


def rot13(s):
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    raw = alphabets + alphabets
    raw_cap = raw.upper()
    cpy_s = str(s)
    s = list(s)

    for ind, obj in enumerate(cpy_s):
        if obj.isalpha():
            if obj.isupper(): s[ind] = raw_cap[raw_cap.index(obj) + 13]
            if obj.islower(): s[ind] = raw[raw.index(obj) + 13]

    return ''.join(s)


def username_valid(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)


def password_valid(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return PASS_RE.match(password)


def email_valid(email):
    if not email: return True
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return EMAIL_RE.match(email)


class MainPage(webapp2.RequestHandler):
    def get(self):
        main_page = """
        <a href="/rot13">Rot13</a> <br>
        <a href="/signin">Sign In</a>
        """
        self.response.out.write(main_page)


class UserSign(webapp2.RequestHandler):
    def print_form(self, name='', nameErr='', passErr='', verifyErr='', emailErr='', email=''):
        self.response.out.write(user_form % {'name': cgi.escape(name, quote=True),
                                             'nameErr': nameErr,
                                             'passErr': passErr,
                                             'verifyErr': verifyErr,
                                             'emailErr': emailErr,
                                             'email': cgi.escape(email, quote=True)})

    def get(self):
        self.print_form()

    def post(self):
        raw_name = self.request.get('username')
        raw_password = self.request.get('password')
        raw_verify = self.request.get('verify')
        raw_email = self.request.get('email')

        username = username_valid(raw_name)
        password = password_valid(raw_password)
        verify = True if raw_password == raw_verify else False
        email = email_valid(raw_email)

        if username and password and verify and email:
            self.redirect('/welcome?username='+ raw_name)
        else:
            user_err = ''
            pass_err = ''
            verify_err = ''
            email_err = ''
            if not username:
                user_err = "That's not a valid username."

            if not verify:
                verify_err = "Your passwords didn't match."

            if not password:
                verify_err = ''
                pass_err = "That wasn't a valid password."

            if not email:
                email_err = "That's not a valid email."

            self.print_form(name=raw_name, email=raw_email, nameErr=user_err, passErr=pass_err, verifyErr=verify_err,
                            emailErr=email_err)


class WelcomeUser(webapp2.RequestHandler):
    def get(self):
        user = self.request.get('username')
        self.response.out.write("<h1>Welcome, "+user)


class RotPage(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(form % {'data': ''})

    def post(self):
        data = self.request.get('data')
        data = rot13(data)
        data = cgi.escape(data, quote=True)
        self.response.out.write(form % {'data': data})


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rot13', RotPage),
    ('/signin', UserSign),
    ('/welcome', WelcomeUser)
], debug=True)
