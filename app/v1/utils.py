import jwt
from flask import request, current_app
from app.v1.models.user import User
from . import v1_api


# required_token decorator
def token_required(f):
    def wrapper(*args, **kwargs):
        print(request.headers.get('Authorization'))
        access_token = request.headers.get('Authorization')
        current_user = None
        if access_token:
            try:
                try:
                    token = jwt.decode(access_token, current_app.config['SECRET_KEY'])
                    current_user = User.query.get(token['uid'])
                except jwt.ExpiredSignatureError as e:
                    raise e
                except (jwt.DecodeError, jwt.InvalidTokenError) as e:
                    raise e
                except:
                    v1_api.abort(401, 'Unknown token error')

            except IndexError:
                raise jwt.InvalidTokenError
        else:
            v1_api.abort(403, 'Token required')
        kwargs['current_user'] = current_user
        return f(*args, **kwargs)

    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = f.__name__
    return wrapper


# administrator decorator
def administrator(f):
    def wrapper(*args, **kwargs):
        if kwargs['current_user'].administrator:
            kwargs.pop('current_user', None)
            return f(*args, **kwargs)
        else:
            v1_api.abort(403, 'Permission denied')

    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = f.__name__
    return wrapper


def discount_credits(f):
    def wrapper(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
            if response.status_code == 200:
                print(kwargs['current_user']['credits'])
            return response
        except Exception as e:
            v1_api.abort(500, e)

    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = f.__name__
    return wrapper
