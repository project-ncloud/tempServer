import dotenv
import json


from os                 import getenv, path
from flask              import Flask, jsonify, request, send_file, send_from_directory, safe_join, abort
from Directories        import Directories
from pathlib            import Path
from middleware         import *
from validation         import *
from flask_cors import CORS, cross_origin

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)



app = Flask(__name__)
#cors = CORS(app, resources={r"*": {"origins": "*", "supports_credentials": True}})
CORS(app)
app.config['JWT_SECRET_KEY'] = getenv('SECRET_KEY')
jwt = JWTManager(app)

@app.route('/users/', methods = ['GET', 'POST', 'DELETE'])
def users():
    return jsonify({})

@app.route('/user/', methods = ['GET', 'POST', 'DELETE'])
def user():
    return jsonify({})

@app.route('/host/config/', methods = ['GET', 'POST', 'DELETE'])
def changeConfig():
    return jsonify({})

@app.route('/reset/', methods = ['GET', 'POST', 'DELETE'])
def resetServer():
    return jsonify({})

@app.route('/host/', methods = ['GET', 'POST', 'DELETE'])
def host():
    return jsonify({})

@app.route('/alive/', methods = ['GET', 'POST', 'DELETE'])
def is_alive():
    return jsonify({"is_running" : True, "status" : True})

@app.route('/init/', methods = ['GET', 'POST', 'DELETE'])
def alive():
    return jsonify({})


@app.route('/dir/')
@jwt_required
@onlyselfAllowed
def getDirs():
    req = request.json

    if isValidPath(req):
        return jsonify(Directories.getDirData(req.get('path')))
    else:
        return jsonify({"msg": "Invalid path"})






@app.route('/file/upload/', methods = ['GET', 'POST'])
def uploadFile():
    files = request.files
    req = request.args

    if isValidPath(req):
        files['file'].save(path.join(req.get('path'), files['file'].filename))
        return allowCors(jsonify({"msg":"Success"}))
    else:
        return allowCors(jsonify({"msg": "Invalid Path"}), 400)


@app.route("/testRoute/", methods = ["GET", "POST"])
def heelo():
    req = request.args
    if isValidPath({"path": safe_join(req.get('path'), req.get('file_name'))}, False):
        return send_from_directory(Path(req.get('path')), filename = req.get('file_name'), as_attachment=True)
    else:
        return allowCors(jsonify({"msg" : "Invalid Path"}), 400)


@app.route("/dir/", methods = ['POST'])
def getFolder():
    req = request.json
    path = req.get('path')

    if path:
        path = path.strip()

    if path == None or path == '':
        return allowCors(jsonify({"path":None, "data":[]}))

    if not Path(path).exists():
        return allowCors(jsonify({"path":None, "data":[]}))

    data = Directories.getDirData(req.get('path'))

    return allowCors(jsonify(data))

    


if __name__ == '__main__':
    app.run(debug=True)


