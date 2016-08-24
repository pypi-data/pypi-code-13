
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..nyssance.django.db.models import ShardLCModel


class Like(ShardLCModel):
    """喜欢"""
    card_id = models.BigIntegerField(default=0, editable=False)  # TODO: 默认值要解决掉:
    card_image_urls = models.CharField(_('image_urls'), max_length=2000, blank=True, editable=False)
    card_caption = models.CharField(max_length=200, blank=True, editable=False)
    image_urls = models.CharField(_('image_urls'), max_length=2000, blank=True)

    class Meta(ShardLCModel.Meta):
        unique_together = ('user_id', 'card_id')
        db_table = 'cards_like'
        verbose_name = _('like')
        verbose_name_plural = _('likes')
