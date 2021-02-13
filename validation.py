import pathlib

DATABASE = {
    "name": "serverName",
    "address": "127.0.0.1:3000",
    "autoStart": False,
    "hosts": [{
        "name": "Guuner Host",
        "path": "D:/save",
        "writable": False,
        "public": False,
        "admin": {
            "name": "souravgain605",
            "writable": True,
            "sharedUsers": ["botai69"]
        },
        "validUsers": ["souravgain605", "botai69"]
    }]
}



def isValidPath(req, onlyDir = True):
    is_technically_valid = pathlib.Path(req.get('path')).exists() and (onlyDir or pathlib.Path(req.get('path')).is_file())

    if not is_technically_valid : 
        return False

    if req.get('path').find(DATABASE.get('hosts')[0].get('path')) == 0:
        return True
    else:
        return False
