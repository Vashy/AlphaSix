import cherrypy
import os, os.path
from mongodb.mongodb import MyMongoClient

class Handler(object):
    _db_client = MyMongoClient()
    
    @cherrypy.expose
    def index(self):
        return open('../frontend/public_html/index.html')
    
    @cherrypy.expose
    def access(self):
        
    
if __name__ == '__main__':
    cherrypy.quickstart(Handler())