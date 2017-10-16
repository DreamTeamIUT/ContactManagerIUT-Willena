import os
import shutil

import cherrypy
from jinja2 import Environment, FileSystemLoader

from appData.webData.handlers.Index import Index
from appData.webData.handlers.Manage import Manager
from appData.webData.handlers.View import View
from appData.webData.handlers.Convert import Convert

from appData import io_formats


class WebApp:
    DEFAULT_DB_FORMAT = "csv"
    TMP_FOLDER = "./tmp/"
    TEMPLATE_FOLDER = 'appData/webData/templates'

    def __init__(self, base="", port=80, ip="127.0.0.1"):
        if port is None:
            port = 80

        if ip is None:
            ip="127.0.0.1"

        if os.path.exists(base):
            self.base = os.path.abspath(base)
            self.contacts = io_formats.get_format(WebApp.DEFAULT_DB_FORMAT).import_data(base)
        else:
            self.contacts = []
        self.env = Environment(loader=FileSystemLoader(self.TEMPLATE_FOLDER))

        cherrypy.config.update({
            'server.socket_host': ip,
            'server.socket_port': port,
        })

        conf = {
            '/': {
                'tools.sessions.on': True,
                'tools.staticdir.root': os.path.abspath(os.getcwd())
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': './appData/webData/static'
            }
        }

        if os.path.exists(self.TMP_FOLDER):
            shutil.rmtree(self.TMP_FOLDER)

        os.makedirs(self.TMP_FOLDER)

        cherrypy.tree.mount(View(self), '/view', conf)
        cherrypy.tree.mount(Manager(self), '/manage', conf)
        cherrypy.tree.mount(Convert(self), '/convert', conf)
        cherrypy.quickstart(Index(self), '/', conf)