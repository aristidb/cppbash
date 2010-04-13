from tipfy.ext.jinja2 import get_env
from jinja2 import evalcontextfilter, Markup, escape
import re, urllib

_paragraph_re = re.compile(r'\n{2,}')

@evalcontextfilter
def linebreaks(eval_ctx, value):
    import sys
    value = escape(value).replace("\r\n", "\n")
    paragraphs = _paragraph_re.split(value)
    paragraphs = [u'<p>%s</p>' % p.replace('\n', Markup('<br>\n')) for p in paragraphs]
    result = u'\n\n'.join(paragraphs)
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

def urlparameter(value):
    return urllib.quote_plus(value)

def atomdatetime(value):
    return value.replace(microsecond=0, tzinfo=None).isoformat() + 'Z'

class JinjaMiddleware(object):
    def pre_dispatch_handler(self):
        env = get_env()
        env.autoescape = True
        env.filters['linebreaks'] = linebreaks
        env.filters['urlparameter'] = urlparameter
        env.filters['atomdatetime'] = atomdatetime

    
