# Usage: python3 __file__.py

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

users = {}

class User(Resource):
    def get(self, user_id):
        """Restituisce lo User con l'id specificato

        Usage example:
            `curl http://localhost:5000/user/<user_id>`
        """
        return {user_id: users[user_id]} 
    
    def delete(self, user_id):
        """Rimuove un User

        Usage example:
            `curl http://localhost:5000/user/<user_id> -X DELETE`
        """
        if user_id in users:
            return users.pop(user_id)


class Users(Resource):
    def get(self):
        """Restituisce la collezione di Users.

        Usage example:
            `curl http://localhost:5000/users`
        """
        return users

    def post(self) -> dict:
        """Crea un User.

        Usage example:
            `curl http://localhost:5000/users -X POST -d "data=some data"`
        """
        user_id = len(users)
        users[user_id] = request.form['data']
        return {user_id: users[user_id]}


api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Users, '/users')

if __name__ == "__main__":
    app.run(debug=True)
