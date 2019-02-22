import cherrypy
import os
import os.path
# import pathlib
import json

absDir = os.path.join(os.getcwd(), os.path.dirname(__file__))
absDir = os.path.join(absDir, '../frontend/public_html/')
# Modo più 'moderno' per ottenere un path assoluto
# absDir2 = pathlib.Path(__file__).parent / '..' / 'frontend' / 'public_html'
# absDir2 = absDir2.resolve()
# print(absDir)
# print(absDir2)

path = os.path.join(absDir, '../../../mongodb/db.json')
data=open(path).read()

class Handler(object):
    
    @cherrypy.expose
    def index(self):
        path = os.path.join(absDir, 'access.html')
        page = open(path).read()
        page = page.replace('*access*', '')
        page = page.replace('*username*', '')
        return page
    
    @cherrypy.expose
    def addpreferences(self):
        path = os.path.join(absDir, 'addpreferences.html')
        page = open(path).read()
        return page
    
    @cherrypy.expose
    def removepreferences(self):
        path = os.path.join(absDir, 'removepreferences.html')
        page = open(path).read()
        return page
    
    @cherrypy.expose
    def access(self,
               submit=None,
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
               submit=None,
               username='*username*',
               nome='*nome*',
               cognome='*cognome*',
               email='*email*',
               telegram='*telegram*'):
        path = os.path.join(absDir, 'insertuser.html')
        page = open(path).read()
        
        not_found = True
        for user in data['users']['username']:
            if username in user:
                not_found = False
        #TODO cercare negli altri campi e spostare in classe Utility
        
        if not_found:
            #TODO INSERT USER
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
    
    @cherrypy.expose
    def removeuser(self):
        path = os.path.join(absDir, 'removeuser.html')
        page = open(path).read()
        page = page.replace('*username*', '')
        page = page.replace('*email*', '')
        page = page.replace('*telegram*', '')
        page = page.replace('*removeusername*', '')
        page = page.replace('*removeemail*', '')
        page = page.replace('*removetelegram*', '')
        return page
    
    @cherrypy.expose
    def removeusername(self,
                   submit=None,
                   username='*username*'):
        path = os.path.join(absDir, 'removeuser.html')
        page = open(path).read()
        if True:
            page = page.replace('*removeusername*',
                                 '<div><p>Utente rimosso</p></div>')
        page = page.replace('*username*', '%s' % username)
        page = page.replace('*username*', '')
        page = page.replace('*email*', '')
        page = page.replace('*telegram*', '')
        page = page.replace('*removeusername*',
                            '<div><p>Utente non rimosso</p></div>')
        page = page.replace('*removeemail*', '')
        page = page.replace('*removetelegram*', '')
        return page
    
    @cherrypy.expose
    def removeemail(self,
                   submit=None,
                   email='*email*'):
        path = os.path.join(absDir, 'removeuser.html')
        page = open(path).read()
        if True:
            page = page.replace('*removeemail*',
                                 '<div><p>Utente rimosso</p></div>')
        page = page.replace('*email*', '%s' % email)
        page = page.replace('*username*', '')
        page = page.replace('*email*', '')
        page = page.replace('*telegram*', '')
        page = page.replace('*removeemail*',
                            '<div><p>Utente non rimosso</p></div>')
        page = page.replace('*removeusername*', '')
        page = page.replace('*removetelegram*', '')
        return page
    
    @cherrypy.expose
    def removetelegram(self,
                   submit=None,
                   telegram='*telegram*'):
        path = os.path.join(absDir, 'removeuser.html')
        page = open(path).read()
        if True:
            page = page.replace('*removetelegram*',
                                 '<div><p>Utente rimosso</p></div>')
        page = page.replace('*telegram*', '%s' % telegram)
        page = page.replace('*username*', '')
        page = page.replace('*email*', '')
        page = page.replace('*telegram*', '')
        page = page.replace('*removetelegram*',
                            '<div><p>Utente non rimosso</p></div>')
        page = page.replace('*removeusername*', '')
        page = page.replace('*removeemail*', '')
        return page
    
    @cherrypy.expose
    def modifyuser(self,
                   submit=None,
                   nome='*nome*',
                   cognome='*cognome*',
                   email='*email*',
                   telegram='*telegram*'):
        path = os.path.join(absDir, 'modifyuser.html')
        page = open(path).read()
        if True:
            page = page.replace('*modifyuser*',
                                 '<div><p>Utente modificato</p></div>')
        
        #TODO: for each user from mongo, new select option
        
        page = page.replace('*nome*', '%s' % nome)
        page = page.replace('*cognome*', '%s' % cognome)
        page = page.replace('*email*', '%s' % email)
        page = page.replace('*telegram*', '%s' % telegram)
        page = page.replace('*nome*', '')
        page = page.replace('*cognome*', '')
        page = page.replace('*email*', '')
        page = page.replace('*telegram*', '')
        page = page.replace('*modifyuser*',
                            '<div><p>Utente non modificato</p></div>')
        return page

if __name__ == '__main__':
    cherrypy.quickstart(Handler())
