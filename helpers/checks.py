def is_logged_in(request):

    username = request.cookies.get('username')
    password = request.cookies.get('password')

    if username and password:
        return {'username': username}

    else:
        return False