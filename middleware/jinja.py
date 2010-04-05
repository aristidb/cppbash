from tipfy.ext.jinja2 import get_env

class JinjaMiddleware(object):
    def pre_dispatch_handler(self):
        env = get_env()
        env.autoescape = True

    
