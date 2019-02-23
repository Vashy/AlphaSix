import cherrypy
import pathlib
from mongo_db.db_controller import DBConnection,DBController

root = pathlib.Path(__file__).parent / '..' / 'frontend' / 'public_html'
root = root.resolve()

class Handler(object):
    """Classe con la funzionalità di server http.
    Ogni metodo della classe corrisponde a un url http gestito da cherrypy.
    Gli argomenti passati ai metodi sono i parametri del metodo post http.

    Le parti contenenti *keyword* sono parole chiave usate per definire
    il comportamento lato server dell'interfaccia grafica.
    Vengono sostituite con frammenti html in base agli eventi
    scatenati dalle azioni dell'utente.
    """

    @cherrypy.expose
    def index(self):
        file = root / 'access.html'
        page = file.read_text()
        page = page.replace('*access*', '')
        page = page.replace('*userid*', '')
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
            access=None,
            userid='*userid*'
    ):
        with DBConnection('butterfly') as client:
            controller = DBController(client)
            email = userid
            telegram = userid


            if True:
                file = root / 'panel.html'
                page = file.read_text()
                return page
        file = root / 'access.html'
        page = file.read_text()
        page = page.replace('*userid*', '%s' % userid)
        page = page.replace('*access*',
                            '<div><p>userid errato</p></div>')
        return page

    @cherrypy.expose
    def adduser(
            self,
            submit=None,
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
            with DBConnection('butterfly') as client:
                controller = DBController(client)
                user = {
                    "name": nome,
                    "surname": cognome,
                    "email": email,
                    "telegram": telegram
                }
                print(controller.insert_user(user))
                page = page.replace('*insert*',
                                '<div><p>Utente inserito</p></div>')
        page = page.replace('*userid*', '%s' % "")
        page = page.replace('*nome*', '%s' % nome)
        page = page.replace('*cognome*', '%s' % cognome)
        page = page.replace('*email*', '%s' % email)
        page = page.replace('*telegram*', '%s' % telegram)
        page = page.replace('*userid*', '')
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
        page = page.replace('*userid*', '')
        page = page.replace('*removeuser*', '')
        return page

    @cherrypy.expose
    def removeuserid(
            self,
            removeuser=None,
            userid='*userid*'
    ):
        file = root / 'removeuser.html'
        page = file.read_text()
        if True:
            page = page.replace('*removeuserid*',
                                '<div><p>Utente rimosso</p></div>')
        page = page.replace('*userid*', '%s' % userid)
        page = page.replace('*userid*', '')
        page = page.replace('*removeuser*',
                            '<div><p>Utente non rimosso</p></div>')
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