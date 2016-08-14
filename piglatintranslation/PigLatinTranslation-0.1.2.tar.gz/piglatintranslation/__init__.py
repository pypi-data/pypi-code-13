"""A pig latin translation microservice.

.. moduleauthor:: Jai Chaudhary <jai.chaudhary.iitd@gmail.com>

"""

from flask import Flask

app = Flask(__name__)
from piglatintranslation import views
