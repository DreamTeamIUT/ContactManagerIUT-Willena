import cherrypy


class WebUtils:
    @staticmethod
    def get_session(name):
        try:
            return cherrypy.session[name]
        except:
            return ""

    @staticmethod
    def set_session(name, value):
        cherrypy.session[name] = value

    @staticmethod
    def is_logged():
        return WebUtils.get_session('logged') == "true"

    @staticmethod
    def redirect_to(path):
        raise cherrypy.HTTPRedirect(path)
