from pageHandle import PageHandler

class Logout(PageHandler):
    def get(self):
        self.response.delete_cookie('user')
        self.response.delete_cookie('hash')
        self.redirect('/login')
        pass