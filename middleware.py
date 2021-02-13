from os                 import getenv
from functools          import wraps
from flask_jwt_extended import get_jwt_identity, get_jwt_claims
from flask              import jsonify, request


def onlyAdminAllowed(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if get_jwt_identity() != "admin": return allowCors(jsonify({"msg":"Bad user", "status": False}), 401)
        return func(*args, **kwargs)
    return decorator


def VIPAllowed(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        tokenData = get_jwt_claims()

        if not (tokenData.get('is_admin') == True or tokenData.get('is_manager') == True):
            return allowCors(jsonify({"msg":"Bad user", "status": False}), 401)

        return func(*args, **kwargs)
    return decorator


def blockSpecialUsername(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        req = request.json
            
        if req.get('username').lower() in getenv('RESTRICT_KEYWORD'): return allowCors(jsonify({"msg":"Username not allowed", "status": False}), 400)
        return func(*args, **kwargs)
    return decorator


def onlyselfAllowed(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        req = request.form

        if req.get('username') == None:
            req = request.json

        identity = get_jwt_identity()
        if identity != req.get('username'): return allowCors(jsonify({"msg":"Username not allowed", "status": False}), 400)
        return func(*args, **kwargs)
    return decorator


def allowCors(response, status = 200):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, status