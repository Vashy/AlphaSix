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

    def select_user(self):
        users = '<select name="userid" id = "userid">'
        for user in self._controller.users():
            value = user['telegram']
            if user['telegram'] is None:
                user['telegram'] = ''
                value = user['email']
            if user['email'] is None:
                user['email'] = ''
                value = user['telegram']
            users += '<option value="' \
                     + value + '">' \
                     + user['telegram'] + ' ' \
                     + user['email'] + '</option>'
        users += '</select>'
        return users

    def check_user_insertable(self, email, telegram):

        if email == '' and telegram == '':
            return False

        if email == '':
            return not self._controller.user_exists(telegram)

        if telegram == '':
            return not self._controller.user_exists(email)

        return (not self._controller.user_exists(telegram) and
                not self._controller.user_exists(email))

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
        if self._controller.user_exists(userid):
            cherrypy.session["userid"] = userid
            file = root / 'panel.html'
            page = file.read_text()
            return page
        file = root / 'access.html'
        page = file.read_text()
        page = page.replace('*userid*', '%s' % userid)
        page = page.replace(
            '*access*',
            '<div>'
            '<p>Email/ID Telegram non presente nel sistema.'
            '</p>'
            '</div>'
        )
        return page

    @cherrypy.expose
    def paneladduser(
            self
    ):
        if cherrypy.session.get("userid") is not None:
            file = root / 'insertuser.html'
            page = file.read_text()
            page = page.replace('*userid*', '')
            page = page.replace('*nome*', '')
            page = page.replace('*cognome*', '')
            page = page.replace('*email*', '')
            page = page.replace('*telegram*', '')
            page = page.replace('*insert*', '')
            return page

        return self.index()

    @cherrypy.expose
    def panelremoveuser(
            self
    ):
        if cherrypy.session.get("userid") is not None:
            users = self.select_user()
            file = root / 'removeuser.html'
            page = file.read_text()
            page = page.replace('*userids*', users)
            page = page.replace('*removeuser*', '')
            return page
        return self.index()

    @cherrypy.expose
    def panelmodifyuser(
            self
    ):
        if cherrypy.session.get("userid") is not None:
            users = self.select_user()
            file = root / 'modifyuser.html'
            page = file.read_text()
            page = page.replace('*userids*', users)
            page = page.replace('*nome*', '')
            page = page.replace('*cognome*', '')
            page = page.replace('*email*', '')
            page = page.replace('*telegram*', '')
            page = page.replace('*modifyuser*', '')
            return page
        return self.index()

    @cherrypy.expose
    def panelpreferences(self):
        if cherrypy.session.get("userid") is not None:
            file = root / 'preferences.html'
            page = file.read_text()
            topics = ''
            for topic in self._controller.topics():
                # topics += '<fieldset><label for="'\
                #           + str(topic['_id']) +\
                #           '">'\
                #           + str(topic['_id']) +\
                #           '</label>' \
                #           '<input name="'\
                #           + str(topic['_id']) +\
                #           '" type="checkbox"/>' \
                #           '<p>Etichetta: '\
                #           + topic['label'] +\
                #           '</p>' \
                #           '<p>Progetto: '\
                #           + topic['project'] +\
                #           '</p></fieldset>'
                topics += ''.join([
                    '<fieldset><label for="',
                    str(topic['_id']),
                    '">',
                    str(topic['_id']),
                    '</label>',
                    '<input name="',
                    str(topic['_id']),
                    '" type="checkbox"/>',
                    '<p>Etichetta: ',
                    topic['label'],
                    '</p>',
                    '<p>Progetto: ',
                    topic['project'],
                    '</p></fieldset>',
                ])
            page = page.replace('*topics*', topics)
            keywords = ''
            for keyword in self._controller.user_keywords(
                    cherrypy.session.get("userid")
            ):
                keywords += keyword + ','
            keywords = keywords.rstrip(',')
            page = page.replace('*textkeywords*', keywords)
            page = page.replace('*subscriptiontopic*', '')
            page = page.replace('*indisponibilita*', '')
            page = page.replace('*favouriteplatform*', '')
            page = page.replace('*favouriteuser*', '')
            page = page.replace('*keywords*', '')
            return page
        return self.index()

    @cherrypy.expose
    def adduser(
            self,
            adduser=None,
            nome='*nome*',
            cognome='*cognome*',
            email='*email*',
            telegram='*telegram*'
    ):
        if cherrypy.session.get("userid") is not None:
            file = root / 'insertuser.html'
            page = file.read_text()
            if self.check_user_insertable(email, telegram):

                if email == '':
                    email = None
                if telegram == '':
                    telegram = None

                self._controller.insert_user(
                    name=nome,
                    surname=cognome,
                    email=email,
                    telegram=telegram
                )
                page = page.replace(
                    '*insert*',
                    '<div>'
                    '<p>Utente inserito</p>'
                    '</div>'
                )
            else:
                page = page.replace(
                    '*insert*',
                    '<div>'
                    '<p>Utente già presente nel sistema '
                    'o id non inserito.</p>'
                    '</div>'
                )

            if email is None:
                email = ''
            if telegram is None:
                telegram = ''
            page = page.replace('*nome*', '%s' % nome)
            page = page.replace('*cognome*', '%s' % cognome)
            page = page.replace('*email*', '%s' % email)
            page = page.replace('*telegram*', '%s' % telegram)
            page = page.replace('*nome*', '')
            page = page.replace('*cognome*', '')
            page = page.replace('*email*', '')
            page = page.replace('*telegram*', '')
            return page
        return self.index()

    @cherrypy.expose
    def removeuser(
            self,
            removeuser=None,
            userid='*userids*'
    ):
        if cherrypy.session.get("userid") is not None:
            file = root / 'removeuser.html'
            page = file.read_text()
            if self._controller.user_exists(userid):
                self._controller.delete_one_user(userid)
                page = page.replace(
                    '*removeuser*',
                    '<div>'
                    '<p>Utente rimosso</p>'
                    '</div>'
                )
            users = self.select_user()
            page = page.replace('*userids*', users)
            page = page.replace(
                '*removeuser*',
                '<div>'
                '<p>Utente non presente nel sistema.</p>'
                '</div>'
            )
            return page
        return self.index()

    @cherrypy.expose
    def modifyuser(
            self,
            modifyuser=None,
            userid='*userids*',
            nome='*nome*',
            cognome='*cognome*',
            email='*email*',
            telegram='*telegram*'
    ):
        if cherrypy.session.get("userid") is not None:
            users = self.select_user()
            file = root / 'modifyuser.html'
            page = file.read_text()
            if self.check_user_insertable(email, telegram):
                if email is None:
                    email = ''
                if telegram is None:
                    telegram = ''
                if self._controller.user_exists(userid):
                    self._controller.update_user_name(userid, nome)
                    self._controller.update_user_surname(userid, cognome)
                    # TODO: DEVO SAPERE COSA STO AGGIORNANDO A QUESTO PUNTO
                    self._controller.update_user_email(userid, email)
                    self._controller.update_user_telegram(userid, telegram)
                    page = page.replace('*modifyuser*',
                                        '<div>'
                                        '<p>Utente modificato</p>'
                                        '</div>'
                                        )
                else:
                    page = page.replace(
                        '*modifyuser*',
                        '<div>'
                        '<p>Utente non presente nel '
                        'sistema.</p>'
                        '</div>'
                    )
            page = page.replace('*userids*', users)
            page = page.replace('*nome*', '%s' % nome)
            page = page.replace('*cognome*', '%s' % cognome)
            page = page.replace('*email*', '%s' % email)
            page = page.replace('*telegram*', '%s' % telegram)
            page = page.replace('*nome*', '')
            page = page.replace('*cognome*', '')
            page = page.replace('*email*', '')
            page = page.replace('*telegram*', '')
            page = page.replace(
                '*modifyuser*',
                '<div>'
                '<p>Email/Telegram'
                ' già presente nel sistema.</p>'
                '</div>'
            )
            return page
        return self.index()

    @cherrypy.expose
    def modifypreferences(self):
        file = root / 'preferences.html'
        page = file.read_text()
        return page


if __name__ == '__main__':
    with DBConnection('butterfly') as connection:
        controller = DBController(connection)
        cherrypy.quickstart(Handler(controller), "/", {
            '/favicon.ico': {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': str(root / 'a6.ico')
            },
            "/": {
                "tools.sessions.on": True,
            }
        })
