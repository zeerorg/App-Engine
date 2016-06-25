from pageHandle import PageHandler
from pageHandle import User
from usefulFunctions import *


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
