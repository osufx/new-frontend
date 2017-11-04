from helpers import mysql


def is_logged_in(request):
    username = request.cookies.get('username')
    password = request.cookies.get('password')

    if username and password:

        return {'username': username}

    else:

        return False


def does_user_exist(username=None, email=None):
    connection, cursor = mysql.connect()

    if username:
        search = mysql.execute(connection, cursor,
                               "SELECT username FROM users WHERE username = %s",
                               [username]).fetchone()
    else:
        search = mysql.execute(connection, cursor,
                               "SELECT username FROM users WHERE email = %s",
                               [email]).fetchone()

    if search != None and len(search) > 0:

        return True

    else:

        return False
