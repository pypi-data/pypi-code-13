from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _

from ..nyssance.django.db.models import OwnerModel, PostModel, ShardModel
from ..nyssance.django.db.utils import get_object_or_none, db_master, db_slave


class Question(PostModel):
    """问题"""
    class Meta(PostModel.Meta):
        verbose_name = _('question')
        verbose_name_plural = _('questions')


class Answer(OwnerModel):
    """回答"""
    question_id = models.IntegerField(editable=False)
    text = models.CharField(_('text'), max_length=8000)
    upvote_count = models.PositiveIntegerField(_('upvote_count'), default=0, editable=False)
    downvote_count = models.PositiveIntegerField(_('downvote_count'), default=0, editable=False)

    class Meta(OwnerModel.Meta):
        verbose_name = _('answer')
        verbose_name_plural = _('answers')

    def __str__(self):
        return self.text


class Vote(ShardModel):
    """投票"""
    answer_id = models.IntegerField(default=0, editable=False)  # TODO: 默认值要解决掉:
    type = models.CharField(_('type'), max_length=1, choices=(('u', _('upvote')), ('d', _('downvote'))))

    class Meta(ShardModel.Meta):
        unique_together = ('user_id', 'answer_id')
        verbose_name = _('vote')
        verbose_name_plural = _('votes')


@receiver(post_save, sender=Vote)
def vote_update(sender, instance, *agrs, **kwargs):
    answer_obj = get_object_or_none(Vote, using=db_master(instance.user_id), pk=instance.pk)
    answer_id = answer_obj.answer_id
    answer = Answer.objects.get(pk=answer_id)
    if instance.created_time:
        if instance.type == 'u':
            answer.upvote_count += 1
            if answer.downvote_count > 0:
                answer.downvote_count -= 1
            answer.save()
        elif instance.type == 'd':
            answer.downvote_count += 1  # FIXME: 这里不对, 另外还要处理downvote_count的情况
            if answer.upvote_count > 0:
                answer.upvote_count -= 1
            answer.save()


@receiver(post_delete, sender=Vote)
def vote_delete(sender, instance, *args, **kwargs):
    answer = get_object_or_none(Answer, using=db_slave(), pk=instance.answer_id)
    if answer.type == 'u':
        answer.upvote_count -= 1
    elif instance.type == 'd':
        answer.downvote_count -= 1
