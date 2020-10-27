from flask_restx import Resource, Namespace, reqparse

from app import db
from app.v1 import v1_api
from .auth import token_required, administrator
from ..models.user import User as UserModel

user_ns = Namespace('user')

parser = user_ns.parser()
parser.add_argument('Authorization', type=str,
                    location='headers',
                    help='Bearer Access Token',
                    required=True
                    )


@user_ns.route('/')
class UserList(Resource):
    @user_ns.marshal_with(UserModel.user_resource_model)
    @user_ns.doc('Access Token', parser=parser)
    @token_required
    @administrator
    def get(self, curret_user=None):
        """Get users list"""
        users = UserModel.query.all()
        return users


@user_ns.route('/<int:id>')
class User(Resource):
    @user_ns.response(404, 'Todo not found or you don\'t have permission to edit it')
    @user_ns.expect(UserModel.user_resource_model, validate=True)
    @user_ns.marshal_with(UserModel.user_resource_model)
    @user_ns.doc('Access Token', parser=parser)
    @token_required
    @administrator
    def put(self, id):
        """Updae user credits"""
        task = v1_api.payload['task']
        try:
            done = v1_api.payload['done']
        except KeyError:
            done = False

        user = UserModel.query.filter_by(id=id).first_or_404()

        user.credits += credits
        if 'done' in v1_api.payload:
            user.done = v1_api.payload['done']

        db.session.add(user)
        db.session.commit()

        return user
