import cherrypy
import pathlib
from mongo_db.db_controller import DBConnection, DBController

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

    I metodi che iniziano con la parola `panel` sono usati per gestire
    l'interfaccia quando l'utente non invia dati tramite post http.
    """

    def __init__(self, controller):
        self._controller = controller

    @cherrypy.expose
    def index(self):
        if cherrypy.session.get("userid") is None:
            file = root / 'access.html'
            page = file.read_text()
            page = page.replace('*access*', '')
            page = page.replace('*userid*', '')
            return page
        file = root / 'panel.html'
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
            if controller.user_exists(userid):
                cherrypy.session["userid"] = userid
                file = root / 'panel.html'
                page = file.read_text()
                return page
        file = root / 'access.html'
        page = file.read_text()
        page = page.replace('*userid*', '%s' % userid)
        page = page.replace('*access*',
                            '<div>'
                            '<p>Email/Telegram non presente nel sistema.'
                            '</p>'
                            '</div>'
                            )
        return page

    @cherrypy.expose
    def paneladduser(
            self
    ):
        file = root / 'insertuser.html'
        page = file.read_text()
        page = page.replace('*userid*', '')
        page = page.replace('*nome*', '')
        page = page.replace('*cognome*', '')
        page = page.replace('*email*', '')
        page = page.replace('*telegram*', '')
        page = page.replace('*insert*', '')
        return page

    @cherrypy.expose
    def panelremoveuser(
            self
    ):
        file = root / 'removeuser.html'
        page = file.read_text()
        page = page.replace('*userid*', '')
        page = page.replace('*removeuser*', '')
        return page

    @cherrypy.expose
    def panelmodifyuser(
            self
    ):
        file = root / 'modifyuser.html'
        page = file.read_text()
        page = page.replace('*userid*', '')
        page = page.replace('*nome*', '')
        page = page.replace('*cognome*', '')
        page = page.replace('*email*', '')
        page = page.replace('*telegram*', '')
        page = page.replace('*modifyuser*', '')
        return page

    @cherrypy.expose
    def panelpreferences(self):
        file = root / 'preferences.html'
        page = file.read_text()
        with DBConnection('butterfly') as client:
            controller = DBController(client)
            topics = ''
            for topic in controller.topics():
                topics += '<fieldset><label for="'\
                          + str(topic['_id']) +\
                          '">'\
                          + str(topic['_id']) +\
                          '</label>' \
                          '<input name="'\
                          + str(topic['_id']) +\
                          '" type="checkbox"/>' \
                          '<p>Etichetta: '\
                          + topic['label'] +\
                          '</p>' \
                          '<p>Progetto: '\
                          + topic['project'] +\
                          '</p></fieldset>'
            page = page.replace('*topics*', topics)
            keywords = ''
            for keyword in controller.user_keywords(
                    cherrypy.session.get("userid")
            ):
                keywords += keyword + ','
            keywords = keywords.rstrip(',')
            page = page.replace('*textkeywords*', keywords)
        page = page.replace('*subscriptiontopic*','')
        page = page.replace('*indisponibilita*', '')
        page = page.replace('*favouriteplatform*', '')
        page = page.replace('*favouriteuser*', '')
        page = page.replace('*keywords*', '')
        return page

    @cherrypy.expose
    def adduser(
            self,
            adduser=None,
            nome='*nome*',
            cognome='*cognome*',
            email='*email*',
            telegram='*telegram*'
    ):
        file = root / 'insertuser.html'
        page = file.read_text()

        with DBConnection('butterfly') as client:
            controller = DBController(client)
            if not (
                    controller.user_exists(email)
                    or
                    controller.user_exists(telegram)
            ):
                controller.insert_user(
                    name=nome,
                    surname=cognome,
                    email=email,
                    telegram=telegram
                )
                page = page.replace('*insert*',
                                    '<div>'
                                    '<p>Utente inserito</p>'
                                    '</div>'
                                    )
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
                            '<div>'
                            '<p>'
                            'Utente già presente nel sistema'
                            '</p>'
                            '</div'
                            )
        return page

    @cherrypy.expose
    def removeuser(
            self,
            removeuser=None,
            userid='*userid*'
    ):
        file = root / 'removeuser.html'
        page = file.read_text()
        with DBConnection('butterfly') as client:
            controller = DBController(client)
            if controller.user_exists(userid):
                controller.delete_one_user(userid)
                page = page.replace('*removeuser*',
                                    '<div>'
                                    '<p>Utente rimosso</p>'
                                    '</div>'
                                    )
        page = page.replace('*userid*', '%s' % userid)
        page = page.replace('*userid*', '')
        page = page.replace('*removeuser*',
                            '<div>'
                            '<p>Utente non presente nel sistema.</p>'
                            '</div>'
                            )
        return page

    @cherrypy.expose
    def modifyuser(
            self,
            modifyuser=None,
            userid='*userid*',
            nome='*nome*',
            cognome='*cognome*',
            email='*email*',
            telegram='*telegram*'
    ):
        file = root / 'modifyuser.html'
        page = file.read_text()
        with DBConnection('butterfly') as client:
            controller = DBController(client)
            if controller.user_exists(userid):
                controller.update_user_name(userid, nome)
                controller.update_user_surname(userid, cognome)
                # TODO: DEVO SAPERE COSA STO AGGIORNANDO A QUESTO PUNTO
                controller.update_user_email(userid, email)
                controller.update_user_telegram(userid, telegram)
                page = page.replace('*modifyuser*',
                                    '<div>'
                                    '<p>Utente modificato</p>'
                                    '</div>'
                                    )

        page = page.replace('*userid*', '%s' % userid)
        page = page.replace('*nome*', '%s' % nome)
        page = page.replace('*cognome*', '%s' % cognome)
        page = page.replace('*email*', '%s' % email)
        page = page.replace('*telegram*', '%s' % telegram)
        page = page.replace('*userid*', '')
        page = page.replace('*nome*', '')
        page = page.replace('*cognome*', '')
        page = page.replace('*email*', '')
        page = page.replace('*telegram*', '')
        page = page.replace('*modifyuser*',
                            '<div>'
                            '<p>Utente non presente nel sistema.</p>'
                            '</div>'
                            )
        return page

    @cherrypy.expose
    def modifypreferences(self):
        file = root / 'preferences.html'
        page = file.read_text()
        return page


if __name__ == '__main__':
    with DBConnection('butterfly') as connection:
        controller = DBController(connection)

        cherrypy.quickstart(Handler(controller), "/", {
            "/": {
                "tools.sessions.on": True,
            }
        })