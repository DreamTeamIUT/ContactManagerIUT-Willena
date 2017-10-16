import cherrypy

from appData.DataManipulation import DataManipulation


class View(object):
    def __init__(self, app):
        self.app = app

    @cherrypy.expose
    def index(self):
        return self.get_page_content("list", contacts=self.app.contacts)

    @cherrypy.expose
    def contact(self, id=""):
        found = False
        try:
            id = int(id)
            if 0 <= id < len(self.app.contacts):
                found = True
            return self.get_page_content("contact", found=found, c=self.app.contacts[id], i=id)
        except:
            return self.get_page_content("contact", found=found)

    @cherrypy.expose
    def search(self, keyword=""):
        print("k " + keyword)
        if keyword != "":
            r = DataManipulation.find_coresponding_contacts(self.app.contacts, keyword)
            print(r)
            return self.get_page_content("search", result=r)

        return self.get_page_content("search")

    def get_page_content(self, pagename, **kwargs):
        # print(kwargs)
        tmpl = self.app.env.get_template('head.html')
        content = self.app.env.get_template('view/content_' + pagename + '.html')
        content = content.render(kwargs)
        return tmpl.render(content=content)
