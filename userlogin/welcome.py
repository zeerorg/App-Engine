from pageHandle import PageHandler
from pageHandle import User


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
            encrypted_key = User.gql("where username='%s'" % user)
            if encrypted == encrypted_key[0].hash_password:
                self.render('welcome.html', user=user)