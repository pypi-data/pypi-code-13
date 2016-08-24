from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _

from ..nyssance.django.db.models import ShardModel
from ..nyssance.django.db.utils import get_object_or_none, get_user_id, db_master
#
# from ..articles.models import Article
from ..comments.models import Comment
from ..likes.models import Like
# from ..products.models import Product
from ..questions.models import Question
# from ..videos.models import Video


TYPE_CHOICES = (
    (_('product'), (
        ('p', _('product')),)),
    (_('content'), (
        ('a', _('article')),
        ('q', _('question')),
        ('v', _('video'))))
)


SITE_CHOICES = (
    ('jd', '京东'),
    ('taobao', '淘宝'),
    ('chuchujie', '楚楚街'),
    ('meilishuo', '美丽说'),
    ('mogujie', '蘑菇街'),
    ('metao', '蜜淘'),
    ('weidian', '微店'),
    ('tmall', '天猫'),
    ('z.cn', '中亚'),
    ('suning', '苏宁'),
    ('guomei', '国美'),
    ('yixun', '易迅'),
    ('yhd', '一号店'),
    ('dangdang', '当当'),
    ('amazon', '美亚'),
    ('amazon.de', '得亚'),
    ('amazon.co.jp', '日亚'),
    ('lotte', '日本乐天'),
    ('ebay', 'eBay'),
    ('itunes', 'App Store'),
    ('others', '其他')
)


class Card(ShardModel):
    """卡片"""
    caption = models.CharField(_('caption'), max_length=200)
    type = models.CharField(_('type'), max_length=1, choices=TYPE_CHOICES, editable=False)
    image_urls = models.CharField(_('image_urls'), max_length=2000, blank=True)
    url = models.URLField(blank=True)
    like_count = models.PositiveIntegerField(_('like_count'), default=0, editable=False)
    comment_count = models.PositiveIntegerField(_('comment_count'), default=0, editable=False)
    tags = models.CharField(_('tags'), max_length=200, blank=True)
    object_id = models.IntegerField(editable=False)
    stream = models.URLField(blank=True, editable=False)
    player = models.URLField(blank=True, editable=False)
    site = models.CharField(_('site'), max_length=12, choices=SITE_CHOICES, default='others')
    tips = models.CharField(_('tips'), max_length=30, blank=True)  # TODO: 有什么何用?
    repost_count = models.PositiveIntegerField(_('repost_count'), default=0, editable=False)

    class Meta(ShardModel.Meta):
        verbose_name = _('card')
        verbose_name_plural = _('cards')

    def __str__(self):
        return self.caption


@receiver(post_delete, sender=Like)
def like_delete(sender, instance, *arge, **kwargs):
    pk = instance.card_id
    using = db_master(get_user_id(pk))
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~", instance.is_origin)
    if instance.is_origin:
        card = get_object_or_none(Card, using=using, pk=pk)
        if card:
            card.like_count -= 1
            card.save(using=using)


@receiver(post_save, sender=Like)
def like_save(sender, instance, *arge, **kwargs):
    pk = instance.card_id
    using = db_master(get_user_id(pk))
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~", instance.is_origin)
    if instance.is_origin:
        card = get_object_or_none(Card, using=using, pk=pk)
        if card:
            card.like_count += 1
            card.save(using=using)


@receiver(post_delete, sender=Comment)
def comment_delete(sender, instance, *arge, **kwargs):
    pk = instance.card_id
    using = db_master(get_user_id(pk))
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~", instance.is_origin)
    if instance.is_origin:
        card = get_object_or_none(Card, using=using, pk=pk)
        if card:
            card.comment_count -= 1
            card.save(using=using)


@receiver(post_save, sender=Comment)
def comment_save(sender, instance, *arge, **kwargs):
    pk = instance.card_id
    using = db_master(get_user_id(pk))
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~", instance.is_origin)
    if instance.is_origin:
        card = get_object_or_none(Card, using=using, pk=pk)
        if card:
            card.comment_count += 1
            card.save(using=using)


@receiver(post_delete, sender=Question)
def question_delete(sender, instance, *arge, **kwargs):
    Card.objects.filter(type='q', object_id=instance.pk, caption=instance.title).delete()


@receiver(post_save, sender=Question)
def question_save(sender, instance, *args, **kwargs):
    cards = Card.objects.filter(object_id=instance.pk)

    if not len(cards):
        Card(type='q', object_id=instance.pk, user_id=instance.user_id, username=instance.username,
             caption=instance.title, tags=instance.tags,
             created_time=instance.created_time).save()
    else:
        Card.objects.update(object_id=instance.pk, caption=instance.title, tags=instance.tags)
