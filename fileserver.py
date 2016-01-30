# -*- coding: utf-8 -*- 

import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string
from tornado.options import define, options

define("port", default=8787, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/upload", UploadHandler)
        ]
        tornado.web.Application.__init__(self, handlers)
        
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("upload_form.html")
        
class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            file_img_name = self.request.files['file_img_name'][0]

            if (file_img_name is not None):
                original_fname = file_img_name['filename']
                folderpath = "/home/keydach/projects/electrolab/static/img/"
                content = file_img_name['body']
        except KeyError:
            print "file_img_name is empty"
        
        try:
            file_svg_name = self.request.files['file_svg_name'][0]

            if (file_svg_name is not None):
                original_fname = file_svg_name['filename']
                folderpath = "/home/keydach/projects/electrolab/static/text/"
                content = file_svg_name['body']
        except KeyError:
            print "file_img_name is empty"
        
        try:
            file_pdf_name = self.request.files['file_pdf_name'][0]

            if (file_pdf_name is not None):
                original_fname = file_pdf_name['filename']
                folderpath = "/home/keydach/projects/electrolab/static/pdf/"
                content = file_pdf_name['body']
        except KeyError:
            print "file_img_name is empty"
        
        output_file = open(folderpath + original_fname, 'w')
        output_file.write(content)
        
        #extension = os.path.splitext(original_img_fname)[1]

        #img_fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        #svg_fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        #pdg_fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))

        #final_filename= fname+extension

        self.finish(u"Файл " + original_fname + u" загружен")

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
    main()