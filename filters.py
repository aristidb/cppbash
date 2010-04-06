def filter(name, request, response):
    data = request.args.get(name, None)
    if data != None:
        response.set_cookie(name, data)
    else:
        data = request.cookies.get(name, None)
        if data == None:
            data = ''
            response.set_cookie(name, data)
    return data

def alternatives(removed, standard):
    possible = standard[:]
    possible.append('')
    if removed != None:
        possible.remove(removed)
    return possible
