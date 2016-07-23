# Copyright 2014-2015 Louis Paternault
#
# This file is part of Jouets.
#
# Jouets is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jouets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jouets.  If not, see <http://www.gnu.org/licenses/>.

"""Facilite la définition et l'utilisation de plugins."""

import importlib
import logging
import os
import pkgutil
import sys

LOGGER = logging.getLogger(__name__)

def basedir(base):
    """Renvoit le répertoire correspondant au module `base` (relatif à jouets).
    """
    module = importlib.import_module(
        'jouets.{}'.format(base)
        )
    if hasattr(module, "__file__"):
        return os.path.dirname(module.__file__)
    else:
        return os.path.dirname(module.__path__._path[0]) # pylint: disable=protected-access



def iter_modules(path, prefix):
    """Itérateur sur les modules situés dans un des `path`, avec le préfixe donné
    """
    for module_finder, name, __is_pkg in pkgutil.walk_packages(path, prefix):
        if name in sys.modules:
            module = sys.modules[name]
        else:
            try:
                module = module_finder.find_spec(name).loader.load_module()
            except ImportError as error:
                LOGGER.debug("[plugins] Could not load module {}: {}".format(name, str(error)))
                continue
        yield module

def get_plugin(base, path):
    """Renvoit le dictionnaire de plugins présents dans le chemin ``path``.

    Un plugin est un module contenant un attribut
    ``PATH`` (``path`` en lettres majuscules), de
    type dictionnaire (:type:`dict`).
    """
    base = "{}.{}".format(base, path)
    attr = path.upper()
    plugins = dict()

    prefix = "jouets.{}.".format(base)
    for module in iter_modules([basedir(base)], prefix):
        if hasattr(module, attr):
            plugins.update(getattr(module, attr))
    return plugins
