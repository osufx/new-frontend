import hashlib

def password(p : str):
    sha1 = hashlib.sha1(("i8Ey{}o94C".format(hashlib.md5(("y7Tj{}pLn5".format(p)).encode('utf-8')).hexdigest())).encode('utf-8')).hexdigest()

    return sha1