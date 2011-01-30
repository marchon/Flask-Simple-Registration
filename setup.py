from setuptools import setup


setup(
    name="Flask-Simple-Registration",
    version="0.1",
    url="http://github.com/mtrichardson/flask-simple-registration",
    license="MIT",
    author="Michael Richardson",
    author_email="michael@mtrichardson.com",
    description="Very basic registration support for Flask.",
    packages=["flaskext"],
    namespace_packages=["flaskext"],
    zip_safe=False,
    install_requires=["setuptools", "Flask", "Flask-SQLAlchemy", "Flask-WTF"]
)
