import logging
from ringo.lib.extension import register_modul
from pyramid.i18n import TranslationStringFactory
from ringo.lib.i18n import translators


# Import models so that alembic is able to autogenerate migrations
# scripts.
from ringo_contact.model import Contact

log = logging.getLogger(__name__)

modul_config = {
    "name": "contact",
    "label": "Contact",
    "clazzpath": "ringo_contact.model.Contact",
    "label_plural": "Contacts",
    "str_repr": "%s|fn",
    "display": "user-menu",
    "actions": ["list", "read", "update", "create", "delete"]
}


def includeme(config):
    """Registers a new modul for ringo.

    :config: Dictionary with configuration of the new modul

    """
    modul = register_modul(config, modul_config)
    Contact._modul_id = modul.get_value("id")
    translators.append(TranslationStringFactory('ringo_contact'))
    config.add_translation_dirs('ringo_contact:locale/')
