from mezzanine.conf import register_setting

register_setting(
    name="INSTAGRAM_ACCESS_TOKEN",
    description="Get instagram access token",
    editable=True,
    default="",
)
register_setting(
    name="INSTAGRAM_CLIENT_SECRET",
    description="Get instagram client secret",
    editable=True,
    default="",
)
