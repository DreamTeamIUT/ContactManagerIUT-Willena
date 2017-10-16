import os
from zipfile import ZipFile

import cherrypy
from cherrypy.lib.static import serve_file

from appData import io_formats


class Convert:
    def __init__(self, app):
        self.app = app

    @cherrypy.expose
    def index(self, **kwargs):
        values = cherrypy.request.params
        print(values)
        if values != {}:
            try:
                format_chosen = values['format']
                filename = values['filename']

                if filename == "":
                    return self.get_page_content("index", formats=io_formats.get_formats(), complete=False)

                files = values['importfile']
                if type(files) is not list:
                    files = [files]

                for file in files:
                    import_format = io_formats.get_format_from_ext(os.path.splitext(file.filename)[1])

                    upload_path = os.path.normpath(self.app.TMP_FOLDER)
                    upload_file = os.path.join(upload_path, file.filename)
                    with open(upload_file, 'wb') as out:
                        while True:
                            data = file.file.read(8192)
                            if not data:
                                break
                            out.write(data)

                    i = import_format.import_data(upload_file)
                    print(i)

                    original_dest = self.app.TMP_FOLDER + filename

                    dest = io_formats.get_format(format_chosen).export_data(i, original_dest)

                    if type(dest) is list:
                        zipfilename = os.path.splitext(original_dest)[0] + ".zip"
                        with ZipFile(zipfilename, 'w') as myzip:
                            for d in dest:
                                myzip.write(os.path.abspath(d), os.path.normcase(d))
                        return serve_file(os.path.abspath(zipfilename), "application/x-download",
                                          os.path.basename(zipfilename))
                    else:
                        return serve_file(os.path.abspath(dest), "application/x-download", filename)
            except KeyError:
                return self.get_page_content("index", formats=io_formats.get_formats(), complete=False)
            except NotImplementedError:
                return self.get_page_content("index", wrongtype=True, formats=io_formats.get_formats())

        return self.get_page_content('index', formats=io_formats.get_formats(), complete=True)

    def get_page_content(self, pagename, **kwargs):
        tmpl = self.app.env.get_template('head.html')
        content = self.app.env.get_template('convert/content_' + pagename + '.html')
        content = content.render(kwargs)
        return tmpl.render(content=content)
