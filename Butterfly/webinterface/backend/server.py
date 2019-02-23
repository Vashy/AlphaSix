import cherrypy
import pathlib
import json

root = pathlib.Path(__file__).parent / '..' / 'frontend' / 'public_html'
root = root.resolve()


class Handler(object):

    @cherrypy.expose
    def index(self):
        file = root / 'access.html'
        page = file.read_text()
        page = page.replace('*access*', '')
        page = page.replace('*username*', '')
        return page

    @cherrypy.expose
    def addpreferences(self):
        file = root / 'addpreferences.html'
        page = file.read_text()
        return page

    @cherrypy.expose
    def removepreferences(self):
        file = root / 'removepreferences.html'
        page = file.read_text()
        return page

    @cherrypy.expose
    def access(
            self,
            submit=None,
            username='*username*'
        ):
        if True:
            file = root / 'panel.html'
            page = file.read_text()
            return page
        file = root / 'access.html'
        page = file.read_text()
        page = page.replace('*username*', '%s' % username)
        page = page.replace('*access*',
                            '<div><p>Username errato</p></div>')
        return page

    @cherrypy.expose
    def adduser(
            self,
            submit=None,
            username='*username*',
            nome='*nome*',
            cognome='*cognome*',
            email='*email*',
            telegram='*telegram*'
        ):
        file = root / 'insertuser.html'
        page = file.read_text()

        not_found = True
        # TODO cercare negli altri campi e spostare in classe Utility

        if not_found:
            # TODO INSERT USER
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
        file = root / 'removeuser.html'
        page = file.read_text()
        page = page.replace('*username*', '')
        page = page.replace('*email*', '')
        page = page.replace('*telegram*', '')
        page = page.replace('*removeusername*', '')
        page = page.replace('*removeemail*', '')
        page = page.replace('*removetelegram*', '')
        return page

    @cherrypy.expose
    def removeusername(
            self,
            submit=None,
            username='*username*'
        ):
        file = root / 'removeuser.html'
        page = file.read_text()
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
    def removeemail(
            self,
                submit=None,
                email='*email*'
        ):
        file = root / 'removeuser.html'
        page = file.read_text()
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
    def removetelegram(
            self,
            submit=None,
            telegram='*telegram*'
        ):
        file = root / 'removeuser.html'
        page = file.read_text()
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
    def modifyuser(
            self,
            submit=None,
            nome='*nome*',
            cognome='*cognome*',
            email='*email*',
            telegram='*telegram*'
        ):
        file = root / 'modifyuser.html'
        page = file.read_text()
        if True:
            page = page.replace('*modifyuser*',
                                '<div><p>Utente modificato</p></div>')

        # TODO: for each user from mongo, new select option

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
