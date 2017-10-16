import cherrypy

from appData.webData.WebUtils import WebUtils


class Index(object):
    def __init__(self, app):
        self.app = app

    @cherrypy.expose
    def index(self):
        if WebUtils.is_logged():
            WebUtils.redirect_to("/manage")
        return self.get_page_content("login")

    @cherrypy.expose
    def login(self, username=None, password=None):
        if username == "Admin" and password == "password":
            WebUtils.set_session("logged", "true")
            WebUtils.redirect_to("/manage")
        else:
            raise WebUtils.redirect_to("/")

    @cherrypy.expose
    def logout(self):
        WebUtils.set_session("logged", "false")
        return "logout"

    def get_page_content(self, pagename, **kwargs):
        print(kwargs)
        tmpl = self.app.env.get_template('head.html')
        content = self.app.env.get_template('index/content_' + pagename + '.html')
        content = content.render(kwargs)
        return tmpl.render(content=content)
