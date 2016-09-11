# ~*~~ coding: utf-8 ~*~

# Monkey patch SQLAlchemy to support some query constructs
from .util.patch import monkey_patch_sqlalchemy, monkey_patch_flask_restless
monkey_patch_sqlalchemy()
monkey_patch_flask_restless()

from .osmalchemy import OSMAlchemy
