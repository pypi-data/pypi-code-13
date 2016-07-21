import logging
from pyramid.i18n import TranslationStringFactory
from ringo.resources import get_resource_factory
from ringo.lib.i18n import translators
from ringo.lib.extension import register_modul
from ringo.lib.helpers import get_action_routename

# Import models so that alembic is able to autogenerate migrations
# scripts.
from ringo_news.model import News

log = logging.getLogger(__name__)

modul_config = {
    "name": "news",
    "clazzpath": "ringo_news.model.News",
    "label": "News",
    "label_plural": "News",
    "str_repr": "%s|subject",
    "display": "admin-menu",
    "actions": ["list", "read", "update", "create", "delete"]
}


def includeme(config):
    """Registers a new modul for ringo.

    :config: Dictionary with configuration of the new modul

    """
    modul = register_modul(config, modul_config)
    News._modul_id = modul.get_value("id")
    translators.append(TranslationStringFactory('ringo_news'))
    config.add_translation_dirs('ringo_news:locale/')

    config.add_route(get_action_routename(News, 'markasread', prefix="rest"),
                     'rest/news/{id}/markasread',
                     factory=get_resource_factory(News))
    config.scan()
