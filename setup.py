from distutils.core import setup

setup(
    name = 'Erlenmeyer',
    version = '0.1.6',
    author = 'Patrick Perini',
    author_email = 'pperini@megabitsapp.com',
    packages = [
        'erlenmeyer',
        'erlenmeyer.libs'
    ],
    scripts = [
        'bin/erlenmeyer'
        'bin/erlenmeyer_templates/project.tmpl.py',
        'bin/erlenmeyer_templates/handlers/ModelObjectHandler.tmpl.py',
        'bin/erlenmeyer_templates/models/ModelObject.tmpl.py',
        'bin/erlenmeyer_templates/settins/settins.tmpl.json'
    ],
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