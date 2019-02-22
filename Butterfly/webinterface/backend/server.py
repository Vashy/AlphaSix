import cherrypy
import os
import os.path

absDir = os.path.join(os.getcwd(), os.path.dirname(__file__))
absDir = os.path.join(absDir, '../frontend/public_html/')

class Handler(object):
    
    @cherrypy.expose
    def index(self):
        path = os.path.join(absDir, 'access.html')
        page = open(path).read()
        page = page.replace('*access*', '')
        page = page.replace('*username*', '')
        return page
    
    @cherrypy.expose
    def access(self,
               submit='*submit*',
               username='*username*'):
        if True:
            path = os.path.join(absDir, 'panel.html')
            page = open(path).read()
            return page
        path = os.path.join(absDir, 'access.html')
        page = open(path).read()
        page = page.replace('*username*', '%s' % username)
        page = page.replace('*access*',
                             '<div><p>Username errato</p></div>')
        return page
    
    @cherrypy.expose
    def adduser(self,
               submit='*submit*',
               username='*username*',
               nome='*nome*',
               cognome='*cognome*',
               email='*email*',
               telegram='*telegram*'):
        path = os.path.join(absDir, 'insertuser.html')
        page = open(path).read()
        if True:
            page = page.replace('*insert*',
                                 '<div><p>Utente inserito</p></div>')
        page = page.replace('*username*', '%s' % username)
        page = page.replace('*nome*', '%s' % nome)
        page = page.replace('*cognome*', '%s' % cognome)
        page = page.replace('*email*', '%s' % email)
        page = page.replace('*telegram*', '%s' % telegram)
        page = page.replace('*username*', '')
        page = page.replace('*nome*', '')
        page = page.replace('*cognome*', '')
        page = page.replace('*email*', '')
        page = page.replace('*telegram*', '')
        page = page.replace('*insert*',
                             '<div><p>Utente già presente nel sistema</p></div')
        return page

if __name__ == '__main__':
    cherrypy.quickstart(Handler())
