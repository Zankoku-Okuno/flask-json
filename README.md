Flask-JSON
==========

Work with JSON in Flask in the most straightforward and idiomatic ways.

Install the extension to your flask instance like:

```python
from flask.ext.json import Json
Json(app)
```

Features
========

Json Routes
-----------

Your application is now equipped with a `json` method, which works much like the standard `route` method, but is more directed to creating json responses.

In particular, return a jsonifyable (see below) python object. A view registered with `@app.json(...)` will handle jsonifying the object and setting the response content-type.

We use normal old `json.dumps` to produce javascript, but we set up a new encoder which can handle a broader range of data. You can use a `__json__` method, a `__jsonfields__` class attribute or register the type after-the-fact.

Standard `__json__` method
--------------------------
Like other libraries, if there is a `__json__` method that returns a jsonifyable python object, then all is well.

Shortcut `__jsonfields__` class attribute
-----------------------------------------
Often, jsonifying an object simply means translating some attributes of a python object to properties of a javascript object. For this, we provide a shortcut. The following two examples are equivalent:

```python
def __json__(self):
    return {
        'foo': self.foo,
        'bar': self.bar,
    }
```

and

```python
__jsonfields__ = ('foo', 'bar',)
```

You can also add constants and functions on the object by setting `__jsonfields__` to a dictionary.
Whenever there are special fields mixed with basic fields, the basic fields go in the `__auto__` slot.

```python
__jsonfields__ = {
    'some_ints': [1, 2, 3],
    '__auto__': ('foo', 'bar',),
    'baz': lambda self: self.getBaz(),
}
```

If both `__json__` and `__jsonfields__` are defined, the latter takes precedence.

Register an encoding
--------------------
If you can't (well, don't want to) modify a pre-existing type, you can register an encoding function for objects of that type.
Any object that is an instance of the registered type will be encoded using that function.
This takes precedence over both `__json__` and `__jsonfields__`
New registrations take precedence old ones.

```python
from flask.ext.json import jsonEncode
@jsonEncode(datetime.date)
def iso8601(date):
    return str(date)
```

For this simple example, you could also use:

```python
from flask.ext.json import jsonEncode
jsonEncode(datetime.date)(str)
```

Issues
======

This extension should play nice with others. In particular, you should be able to
use other decorators on `.json`-enabled functions. If you experience problems or have
questions, [submit a bug report](https://github.com/Zankoku-Okuno/flask-verbs/issues).

One known issue is that using `@app.json(...)` twice on a single handler does not work; I'm not sure why.

