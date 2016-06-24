import re
import cgi

def username_valid(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)


def password_valid(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return PASS_RE.match(password)


def email_valid(email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return EMAIL_RE.match(email)


if password_valid('hrllo'):
    print 'True'
else:
    print 'False'

# print cgi.escape(None, quote=True)