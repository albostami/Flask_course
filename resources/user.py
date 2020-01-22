
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username',
    required=True,
    help="username is reqireed"
)
_user_parser.add_argument(
    'password',
    required=True,
    help="password is reqireed"
)


class UserRegister(Resource):

    def post(self):

        data = _user_parser.parse_args()
        username = data['username']
        if UserModel.get_user_by_name(username):
            return {'messae': 'User already defined'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User registered successfully.'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.get_user_by_id(user_id)
        if not user:
            return {'message': 'User Not Found!'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.get_user_by_id(user_id)
        if not user:
            return {'message': 'User Not Found!'}, 404
        user.delete_from_db()
        return {'message': 'User Deleted'}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.get_user_by_name(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials!'}, 401
