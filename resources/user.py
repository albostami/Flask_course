# import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username', required=True, help="username is reqireed"
    )
    parser.add_argument(
        'password', required=True, help="password is reqireed"
    )

    def post(self):

        data = UserRegister.parser.parse_args()
        username = data['username']
        if UserModel.get_user_by_name(username):
            return {'messae': 'User already defined'}, 400

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "INSERT INTO users values (NULL, ?,?)"
        # cursor.execute(query, (data['username'], data['password']))

        # connection.commit()
        # connection.close()
        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User registered successfully.'}, 201

    # Ehab: tried to add it this get but it did not work when linking to endpoint

    # def get(self, id):
    #     user = UserModel.get_user_by_id(id)
    #     if user:
    #         return vars(user), 200
    #     return {"message": "user not found"}, 404
