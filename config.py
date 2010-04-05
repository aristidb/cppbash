# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~

    Configuration settings.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE for more details.
"""
config = {}

# Configurations for the 'tipfy' module.
config['tipfy'] = {
    'middleware': [
        'tipfy.ext.debugger.DebuggerMiddleware',
        'middleware.jinja.JinjaMiddleware'
    ],
}
