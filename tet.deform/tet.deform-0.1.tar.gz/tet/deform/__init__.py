import deform
from deform import Form, ValidationFailure
from js.deform import resource_mapping
from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request
from pkg_resources import resource_filename


def auto_need(request, form):
    """Automatically ``need()`` the relevant Fanstatic resources for a form.
    This function automatically utilises libraries in the ``js.*`` namespace
    (such as ``js.jquery``, ``js.tinymce`` and so forth) to allow Fanstatic
    to better manage these resources (caching, minifications) and avoid
    duplication across the rest of your application.
    """

    requirements = form.get_widget_requirements()
    for library, version in requirements:
        resources = resource_mapping[library]
        if not isinstance(resources, list):  # pragma: no cover (bw compat only)
            resources = [resources]

        for resource in resources:
            request.need(resource)


def includeme(config=None):
    _marker = object()

    def form_render(self, appstruct=_marker, request=None, **kw):
        if appstruct is not _marker:  # pragma: no cover  (copied from deform)
            kw['appstruct'] = appstruct

        if request is None:
            request = get_current_request()

        html = super(Form, self).render(**kw)
        auto_need(request, self)

        return html

    def validation_failure_render(self, request=None):
        if request is None:
            request = get_current_request()

        auto_need(request, self.field)
        return self.field.widget.serialize(self.field, self.cstruct)

    def patch_deform():
        Form.render = form_render
        ValidationFailure.render = validation_failure_render

    patch_deform()

    def translator(term):
        return get_localizer(get_current_request()).translate(term)

    deform_template_dir = resource_filename('deform', 'templates/')
    zpt_renderer = deform.ZPTRendererFactory(
        [deform_template_dir],
        translator=translator)
    deform.Form.set_default_renderer(zpt_renderer)
