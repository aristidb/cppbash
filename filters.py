import models

class Filter(object):
    def __init__(self, name, alternatives, default = '', add_empty = True):
        self._name = name
        self._alternatives = list(alternatives)
        if add_empty:
            self._alternatives.append('')
        self._default = default

    def filter(self, request, response):
        data = request.args.get(self._name, None)
        if data != None:
            response.set_cookie(self._name, data)
        else:
            data = request.cookies.get(self._name, None)
            if data == None:
                data = self._default
                response.set_cookie(self._name, data)
        return data

    def alternatives(self, removed):
        result = self._alternatives[:]
        if removed != None:
            result.remove(removed)
        return result

    def compute(self, request, response):
        current = self.filter(request, response)
        other = self.alternatives(current)
        return (current, other)

language_filter = Filter('language', models.languages)
programming_language_filter = Filter('programming_language', models.programming_languages)
