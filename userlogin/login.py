from pageHandle import PageHandler
from pageHandle import User
from usefulFunctions import *


class LoginHandler(PageHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        raw_name = self.request.get('username')
        raw_password = self.request.get('password')
        hashed = None
        user_err = ''
        pass_err = ''
        query = User.gql("where username='%s'" % raw_name).get()
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
