"""Pytsite Content Endpoints.
"""
from datetime import datetime as _datetime
from pytsite import taxonomy as _taxonomy, odm_ui as _odm_ui, auth as _auth, http as _http, odm_auth as _odm_auth, \
    router as _router, metatag as _metatag, assetman as _assetman, odm as _odm, widget as _widget, \
    lang as _lang, tpl as _tpl, logger as _logger, hreflang as _hreflang, comments as _comments

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def index(args: dict, inp: dict):
    """Content Index.
    """
    # Delayed import to prevent exception during application initialization
    from . import _api

    # Checking if the model is registered
    model = args.get('model')
    if not model or not _api.is_model_registered(model):
        _logger.warn("Content model '{}' is not found. Redirecting to home.".format(model), __name__)
        return _http.response.Redirect(_router.base_url())

    # Getting finder
    f = _api.find(model)

    # Filter by term
    term_field = args.get('term_field')
    if term_field:
        term_model = f.mock.get_field(term_field).model
        term_alias = args.get('term_alias')
        if term_alias:
            term = _taxonomy.find(term_model).where('alias', '=', term_alias).first()
            if term:
                args['term'] = term
                if isinstance(f.mock.fields[term_field], _odm.field.Ref):
                    f.where(term_field, '=', term)
                elif isinstance(f.mock.fields[term_field], _odm.field.RefsList):
                    f.where(term_field, 'in', [term])
                _metatag.t_set('title', term.title)
            else:
                raise _http.error.NotFound()
        else:
            raise _http.error.NotFound()

    # Filter by author
    author_nickname = inp.get('author') or args.get('author')
    if author_nickname:
        author = _auth.get_user(nickname=author_nickname)

        if author:
            _metatag.t_set('title', _lang.t('pytsite.content@articles_of_author', {'name': author.full_name}))
            f.where('author', '=', author)
            args['author'] = author
        else:
            raise _http.error.NotFound()

    # Search
    if inp.get('search'):
        query = inp.get('search')
        f.where_text(query)
        _metatag.t_set('title', _lang.t('pytsite.content@search', {'query': query}))

    pager = _widget.static.Pager('content-pager', total_items=f.count(), per_page=10)

    args['entities'] = list(f.skip(pager.skip).get(pager.limit))
    args['pager'] = pager

    return _router.call_ep('$theme@content_' + model + '_index', args, inp)


def view(args: dict, inp: dict):
    """View Content Entity.
    """
    from . import _api

    model = args.get('model')
    entity = _api.find(model, status=None, check_publish_time=False).where('_id', '=', args.get('id')).first()
    """:type: pytsite.content._model.Content"""

    # Check entity existence
    if not entity:
        raise _http.error.NotFound()

    # Check permissions
    if not entity.check_perm('view'):
        raise _http.error.Forbidden()

    # Show non published entities only who can edit them
    if entity.has_field('publish_time') and entity.publish_time > _datetime.now():
        if not entity.check_perm('modify'):
            raise _http.error.NotFound()
    if entity.has_field('status') and entity.status != 'published':
        if not entity.check_perm('modify'):
            raise _http.error.NotFound()

    # Update entity's comments count
    _odm_auth.disable_perm_check()
    entity.f_set('comments_count', _comments.get_all_comments_count(entity.ui_view_url())).save()
    _odm_auth.enable_perm_check()

    # Meta title
    if entity.has_field('title'):
        title = entity.title
        _metatag.t_set('title', title)
        _metatag.t_set('og:title', title)
        _metatag.t_set('twitter:title', title)

    # Meta description
    if entity.has_field('description'):
        description = entity.description
        _metatag.t_set('description', description)
        _metatag.t_set('og:description', description)
        _metatag.t_set('twitter:description', description)

    # Meta keywords
    if entity.has_field('tags'):
        _metatag.t_set('keywords', entity.f_get('tags', as_string=True))

    # Meta image
    if entity.has_field('images') and entity.images:
        _metatag.t_set('twitter:card', 'summary_large_image')
        image_w = 900
        image_h = 500
        image_url = entity.images[0].f_get('url', width=image_w, height=image_h)
        _metatag.t_set('og:image', image_url)
        _metatag.t_set('og:image:width', str(image_w))
        _metatag.t_set('og:image:height', str(image_h))
        _metatag.t_set('twitter:image', image_url)
    else:
        _metatag.t_set('twitter:card', 'summary')

    # Other metatags
    _metatag.t_set('og:type', 'article')
    _metatag.t_set('author', entity.author.full_name)
    _metatag.t_set('article:author', entity.author.full_name)
    _metatag.t_set('og:url', entity.url)
    _metatag.t_set('article:publisher', entity.url)

    # Alternate languages URLs
    for lng in _lang.langs(False):
        f_name = 'localization_' + lng
        if entity.has_field(f_name) and entity.f_get(f_name):
            _hreflang.add(lng, entity.f_get(f_name).url)

    _assetman.add('pytsite.content@js/content.js')

    args['entity'] = entity

    return _router.call_ep('$theme@content_' + model + '_view', args, inp)


def modify(args: dict, inp: dict) -> str:
    """Get content entity create/modify form.
    """
    model = args['model']
    eid = args['id']

    try:
        frm = _odm_ui.get_m_form(model, eid if eid != 0 else None)

        if _router.is_ep_callable('$theme@content_' + model + '_modify'):
            args['frm'] = frm
            return _router.call_ep('$theme@content_' + model + '_modify', args, inp)

        else:
            return _tpl.render('pytsite.content@page/modify', {'frm': frm})

    except _odm.error.EntityNotFound:
        raise _http.error.NotFound()


def propose(args: dict, inp: dict) -> str:
    """Propose content endpoint.
    """
    model = args.get('model')

    frm = _odm_ui.get_m_form(model, redirect=_router.base_url())
    frm.title = None

    _metatag.t_set('title', _lang.t('pytsite.content@propose_content'))

    return _router.call_ep('$theme@content_' + model + '_propose', {
        'form': frm
    })


def unsubscribe(args: dict, inp: dict) -> _http.response.Redirect:
    """Unsubscribe from digest endpoint.
    """
    s = _odm.dispense('content_subscriber', args.get('id'))
    if s:
        s.f_set('enabled', False).save()
        _router.session().add_success(_lang.t('pytsite.content@unsubscription_successful'))

    return _http.response.Redirect(_router.base_url())
