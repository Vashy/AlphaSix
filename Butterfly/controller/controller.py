from abc import ABC, abstractmethod

class Server (ABC):
    
    @abstractmethod
    def users(self):
        pass

    @abstractmethod
    def preferences(self):
        pass
        

class FlaskImpl (Server):

    def __init__(self, flask: Flask, fr: flask_restful):
        self._flask = flask
        self._fr = fr
        self._app = flask.Flask(__name__)
        self._api = fr.Api(app)
        
    class User(self._fr.Resource):
        def get(self, user):
            pass  # TODO

        def delete(self, user):
            pass  # TODO

        def put(self, user):
            pass
            # TODO
            
    self._api.add_resource(User, '/user/<user>')


    if __name__ == '__main__':
        self._app.run(debug=True)
    
    

class Observer (ABC):

    def update(self):
        pass


class Controller (Observer):

    def __init__(self, view: View, controller: Server, model: DB):
        self._view = view
        self._controller = controller
        self._model = model
        
    def update(self):
        #TODO
        return
