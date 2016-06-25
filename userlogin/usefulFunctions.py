import re
import hashlib
from google.appengine.ext import db
import random
import string


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
