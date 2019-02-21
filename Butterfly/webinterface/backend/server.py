import cherrypy
import os, os.path

class Handler(object):
    
    @cherrypy.expose
    def index(self):
        return open('../frontend/public_html/index.html')
    
    @cherrypy.expose
    def access(self):
        return open('../frontend/public_html/index.html')
    
if __name__ == '__main__':
    cherrypy.quickstart(Handler())