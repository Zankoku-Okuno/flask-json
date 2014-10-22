import json
from functools import wraps
from flask import Response


class Json:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        from types import MethodType
        app.json = MethodType(json_route, app)
        return self

def json_route(app, route, **kwargs):
    def decorate(handler):
        @wraps(handler)
        def inner(*args, **kwargs):
            # TODO check accept header
            obj = handler(*args, **kwargs)
            # TODO when an error occurs, provide JSON error pages
            # TODO figure out how to extend json.dumps
            it = json.dumps(obj, cls=_Encoder)
            return Response(it, mimetype='application/json')
        app.route(route, **kwargs)(inner)
        return inner
    return decorate

class _Encoder(json.JSONEncoder):
    def default(self, obj):
        # FIXME check a registry of type-function pairs
        for type, func in []:
            if isinstance(obj, type):
                return func(obj)
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return super(json.JSONEncoder, self).default(obj)
