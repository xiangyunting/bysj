# coding=utf-8

def getUserInfo(request):
    return {'manager': request.session.get('onlineuser', None)}
