from distutils.core import setup

setup(
    name = 'Erlenmeyer',
    version = '0.1.5',
    author = 'Patrick Perini',
    author_email = 'pperini@megabitsapp.com',
    packages = ['erlenmeyer', 'erlenmeyer.libs', 'erlenmeyer.templates'],
    scripts = ['bin/erlenmeyer'],
    url = 'http://MegaBits.github.com/Erlenmeyer',
    license = 'LICENSE.txt',
    description = 'Automatically generate Flask servers from Core Data.',
    long_description = open('README.txt').read(),
    install_requires = [
        'Flask >= 0.9',
        'Flask-SQLAlchemy >= 0.16',
        'Jinja2 >= 2.6'
    ]
)