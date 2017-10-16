import os
from zipfile import ZipFile

import cherrypy
from cherrypy.lib.static import serve_file

from appData import io_formats
from appData.Contact import Contact
from appData.DataManipulation import DataManipulation
from appData.webData.WebUtils import WebUtils


class Manager(object):
    def __init__(self, app):
        self.app = app

    @cherrypy.expose
    def index(self):
        if WebUtils.get_session('logged') != "true":
            WebUtils.redirect_to("/")
        return self.get_page_content("manage", basepath=self.app.base, contacts=self.app.contacts)

    @cherrypy.expose
    def add(self, **kwargs):
        values = cherrypy.request.params
        print(values)
        ident_id= -1

        try:
            ident_id = int(values['editMode'])
            editmode = True
        except:
            editmode = False
        c = Contact()

        not_valid = {}
        added = False

        for v in values:
            h = c.get_header_by_id(v)
            if h is not None:
                if not h.is_valid(values[v]):
                    not_valid[v] = {'message': h.get_error_message(), 'name': h.name}
                    continue
                h.set_value(values[v])

        if not_valid == {} and len(values) > 0 and not editmode:
            self.app.contacts.append(c)
            added = True

        if not_valid == {} and len(values) > 0 and editmode:
            added = True
            self.app.contacts[ident_id] = c

        return self.get_page_content("add", headers=c.available_headers, err=not_valid, added=added, editmode=editmode)

    @cherrypy.expose
    def exports(self, iden="", **kwargs):
        values = cherrypy.request.params

        print(values)
        if values != {}:
            try:
                format_chosen = values['format']
                filename = values['filename']
                choise = values['chk']
            except:
                return self.get_page_content("exports", formats=io_formats.get_formats(), contacts=self.app.contacts,
                                             emptyquery=True)

            original_dest = "./webData/tmp/" + filename

            chosen_contacts = DataManipulation.get_selected_from_index(self.app.contacts,
                                                                       DataManipulation.string_list_to_int(choise))
            dest = io_formats.get_format(format_chosen).export_data(chosen_contacts, original_dest)

            if type(dest) is list:
                zipfilename = os.path.splitext(original_dest)[0] + ".zip"
                with ZipFile(zipfilename, 'w') as myzip:
                    for d in dest:
                        myzip.write(os.path.abspath(d), os.path.normcase(d))
                return serve_file(os.path.abspath(zipfilename), "application/x-download", os.path.basename(zipfilename))
            else:
                return serve_file(os.path.abspath(dest), "application/x-download", filename)

        return self.get_page_content("exports", formats=io_formats.get_formats(), contacts=self.app.contacts, iden=iden)

    @cherrypy.expose
    def imports(self, **kwargs):
        value = cherrypy.request.params
        print(value)
        if value != {}:
            try:
                files = value['file']
                if type(files) is not list:
                    files = [files]

                for file in files:
                    import_format = io_formats.get_format_from_ext(os.path.splitext(file.filename)[1])

                    upload_path = os.path.normpath('./webData/tmp')
                    upload_file = os.path.join(upload_path, file.filename)
                    with open(upload_file, 'wb') as out:
                        while True:
                            data = file.file.read(8192)
                            if not data:
                                break
                            out.write(data)

                    i = import_format.import_data(upload_file)
                    print(i)
                    self.app.contacts += i
                return self.get_page_content("imports", importok=True, addnumber=len(i), totalfiles=len(files))

            except KeyError:
                return self.get_page_content("imports", emptyquery=True)
            except NotImplementedError:
                return self.get_page_content("imports", wrongtype=True, formats=io_formats.get_formats())

        return self.get_page_content("imports")

    @cherrypy.expose
    def delete(self, iden=""):
        print(iden)
        try:
            iden = int(iden)
            if 0 <= iden < len(self.app.contacts):
                self.app.contacts.remove(self.app.contacts[iden])
            WebUtils.redirect_to("/manage")
        except:
            WebUtils.redirect_to("/manage")

    @cherrypy.expose
    def edit(self, id=""):
        print(id)
        # try:
        id = int(id)
        if 0 <= id < len(self.app.contacts):
            c = self.app.contacts[id]
            return self.get_page_content("add", headers=c.available_headers, editmode=True, err={}, id=id)
            # except:
            #    WebUtils.redirect_to("/manage")

    def get_page_content(self, pagename, **kwargs):
        # print(kwargs)
        tmpl = self.app.env.get_template('head.html')
        menu = self.app.env.get_template('manager/menu.html')
        content = self.app.env.get_template('manager/content_' + pagename + '.html')
        content = content.render(kwargs)
        menu = menu.render(content=content)

        return tmpl.render(content=menu)
