import models

class Filter(object):
    def __init__(self, name, alternatives, default = '', add_empty = True):
        self.name = name
        self._alternatives = list(alternatives)
        if add_empty:
            self._alternatives.append('')
        self._default = default

    def filter(self, request, response, cookies=True):
        data = request.args.get(self.name, None)
        if data != None:
            if cookies:
                response.set_cookie(self.name, data)
        else:
            if cookies:
                data = request.cookies.get(self.name, None)
            if data == None:
                data = self._default
                if cookies:
                    response.set_cookie(self.name, data)
        return data

    def alternatives(self, removed):
        result = self._alternatives[:]
        if removed != None:
            result.remove(removed)
        return result

    def compute(self, request, response, cookies=True):
        current = self.filter(request, response, cookies)
        other = self.alternatives(current)
        return (current, other)

    def make_instance(self, request, response, cookies=True):
        (current, other) = self.compute(request, response, cookies)
        return FilterInstance(self.name, current, other, self._alternatives)

class FilterInstance(object):
    def __init__(self, name, current, other, all_):
        self.name = name
        self.current = current
        self.other = other
        self.all = all_

    def add_to_query(self, query):
        if self.current:
            query.filter(self.name + ' =', self.current)

class FilterCollection(object):
    def __init__(self, filters, request, response, cookies=True):
        self.instances = dict()
        for filt in filters:
            self.instances[filt.name] = filt.make_instance(request, response, cookies)

    def __getitem__(self, key):
        return self.instances[key]

    def add_to_query(self, query):
        for key in sorted(self.instances.keys()):
            self.instances[key].add_to_query(query)

language_filter = Filter('language', models.languages, default = models.default_language)
programming_language_filter = Filter('programming_language', models.programming_languages)
filters = [language_filter, programming_language_filter]
