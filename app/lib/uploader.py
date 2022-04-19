from werkzeug.utils import secure_filename
import os
import datetime
import hashlib

ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']
UPLOAD_FOLDER = os.getcwd() + '/app/static/uploads'
MAX_FILE_SIZE = 2000


def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_size(file):
    chunk = 10
    data = None
    size += len(data)
    while data != b'':
        data = file.read(chunk)
        if size > MAX_FILE_SIZE:
            return False
    return True


def get_secure_filename(filename):
    return str(secure_filename(filename))


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def uploads(f):
    if f and allowed_extension(f.filename):
        fileOrigin = f.filename.rsplit('.', 1)
        fileExt = fileOrigin[1].lower()
        if fileExt == 'jpeg' or fileExt == 'jpg' or fileExt == 'png':
            encFile = hashlib.md5(get_secure_filename(
                f.filename).encode('utf-8')).hexdigest()
            pathFile = UPLOAD_FOLDER+'/images' + encFile+'.' + fileExt
            f.save(pathFile)
            return {
                'status': 'ok',
                'path_file': pathFile,
                'photo_name': encFile + '.' + fileExt
            }
        elif fileExt == 'pdf':
            encFile = hashlib.md5(get_secure_filename(
                f.filename).encode('utf-8')).hexdigest()
            pathFile = UPLOAD_FOLDER+'/files'+encFile+'.' + fileExt
            f.save(pathFile)
            return {
                'status': 'ok',
                'path_file': pathFile
            }
        else:
            return {
                'status': 'error'
            }
