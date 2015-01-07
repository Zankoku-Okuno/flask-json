from distutils.core import setup

setup(
    name='Flask-Json',
    version='0.1.0',
    author='Zankoku Okuno',
    author_email='zankoku.okuno@gmail.com',
    packages=['flask_json'],
    url='https://github.com/Zankoku-Okuno/flask-json',
    license='LICENSE',
    description='Extend Flask with nice syntax for working with JSON responses.',
    long_description=open('README.md').read(), #FIXME do this relative to this file
    install_requires=[
        "Flask >= 0.10.0", #FIXME this probably works with lower versions of flask
    ],
)
