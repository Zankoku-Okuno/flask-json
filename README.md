Flask-JSON
==========

Work with JSON in Flask in the most straightforward and idiomatic ways.


TODO features include `@app.json(some_route)`, extending `json.dumps` to recognize `__json__` and install type-function pairs into an app to handle, say `if isinstance(o, set): return list(o)`


This extension should play nice with others. In particular, you should be able to
use decorators on `.json`-enabled functions. If you experience problems or have
questions, [submit a bug report](https://github.com/Zankoku-Okuno/flask-verbs/issues).
