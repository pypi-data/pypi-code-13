from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..nyssance.django.db.models import ShardLCModel


class Comment(ShardLCModel):
    """评论"""
    card_id = models.BigIntegerField(editable=False)
    text = models.CharField(_('text'), max_length=200)
    like_count = models.PositiveIntegerField(_('like_count'), default=0, editable=False)

    class Meta(ShardLCModel.Meta):
        db_table = 'cards_comment'
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
