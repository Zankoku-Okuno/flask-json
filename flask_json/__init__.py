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


class _Encoder(json.JSONEncoder):
    bytype = []

    def default(self, obj):
        for the_type, __json__ in _Encoder.bytype:
            if isinstance(obj, the_type):
                return __json__(obj)
        if hasattr(obj, '__jsonfields__'):
            return self._jsonfields(obj, obj.__jsonfields__)
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return super(_Encoder, self).default(obj)

    def _jsonfields(self, obj, fields):
        data = dict()
        def autofields(lst):
            for name in lst:
                data[name] = getattr(obj, name)
        if isinstance(fields, dict):
            for key, val in fields.items():
                if key == '__auto__':
                    autofields(val)
                elif callable(val):
                    data[key] = val(obj)
                else:
                    data[key] = val
        else:
            autofields(fields)
        return data


def jsonEncode(ty):
    if not isinstance(ty, type):
        raise TypeError("Must call the jsonEncode decorator with a type.")
    def decorate(__json__):
        _Encoder.bytype.insert(0, (ty, __json__))
        return __json__
    return decorate

def dumps(obj):
    return json.dumps(obj, cls=_Encoder)


def json_route(app, route, **kwargs):
    def decorate(handler):
        @wraps(handler)
        def inner(*args, **kwargs):
            # TODO check accept header
            obj = handler(*args, **kwargs)
            # TODO when an error occurs, provide JSON error pages
            it = dumps(obj)
            return Response(it, mimetype='application/json')
        app.route(route, **kwargs)(inner)
        return inner
    return decorate
