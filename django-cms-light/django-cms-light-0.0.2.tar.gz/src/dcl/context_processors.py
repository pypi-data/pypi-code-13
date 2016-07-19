from django.contrib.sites.models import Site

from pinax_theme_bootstrap.conf import settings


def theme(request):
    # Copy of pinax_theme_bootstrap.context_processors.theme
    # that uses request.site
    ctx = {
        "THEME_ADMIN_URL": settings.THEME_ADMIN_URL,
        "THEME_CONTACT_EMAIL": settings.THEME_CONTACT_EMAIL,
    }

    if Site._meta.installed:
        ctx.update({
            "SITE_NAME": request.site.name,
            "SITE_DOMAIN": request.site.domain
        })

    return ctx
