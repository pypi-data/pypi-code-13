# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AnonymousUser

from .settings import DEFAULT
from .constants import FILTER_TYPE, FILTER_ID, EXCLUDE_ID


class ObjectFilter(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=False, related_name='%(app_label)s_%(class)s_users', verbose_name=_(u'User'))
    content_type = models.ForeignKey(ContentType, null=False, blank=False, related_name='%(app_label)s_%(class)s_content_type', verbose_name=_(u'Class'))
    filter_type = models.SmallIntegerField(choices=FILTER_TYPE, null=False, blank=False, verbose_name=_(u'Filter Type'))
    filter_values = models.CharField(max_length=250, null=True, blank=True, verbose_name=_(u'Values'))

    class Meta:
        verbose_name = _(u'Data filter')
        verbose_name_plural = _(u'Data filter')

    def __unicode__(self):
        return u"%s - %s" % (', '.join([str(i) for i in self.users.all()]), self.content_type)

    @classmethod
    def _check_filter_values(self, record=None):
        self.filter_values = eval(record.filter_values)

        if not isinstance(self.filter_values, list):
            raise ValueError(_(u'Filter Values is not a List: %s' % record.filter_values))

    @classmethod
    def _update_filter_dict(self, model=None, field_name='id', filter_type=FILTER_ID, values=[]):
        if model and model._meta.label_lower not in self._filter_dict:
            self._filter_dict[model._meta.label_lower] = {FILTER_ID: {}, EXCLUDE_ID: {}}
        if values:
            self._filter_dict[model._meta.label_lower][filter_type]['%s__in' % field_name] = values
        else:
            self._filter_dict[model._meta.label_lower][filter_type]['%s__isnull' % field_name] = True

    @classmethod
    def create_filter_dict(self, user=None, session=None):
        DJ_AUTH = getattr(settings, 'DJ_AUTH', DEFAULT)

        self._filter_dict = {}

        for record in ObjectFilter.objects.filter(users=user):
            self._check_filter_values(record)

            content_type = ContentType.objects.get(pk=record.content_type_id)
            model_class = content_type.model_class()

            # Create filter for the own class
            self._update_filter_dict(model_class, field_name='id', filter_type=record.filter_type, values=eval(record.filter_values))

            related_models = []
            for field in model_class._meta.get_fields():
                if field.is_relation and field.related_model:
                    if field.related_model not in related_models:
                        related_models.append(field.related_model)

            # Create filter for the related classes
            for related_model in related_models:
                for field in related_model._meta.get_fields():
                    if field.is_relation and field.related_model and not field.auto_created and field.related_model == model_class:
                        if DJ_AUTH['global_fields_exclude'] and field.name in DJ_AUTH['global_fields_exclude']:
                            continue

                        if DJ_AUTH['related_filter_fields_exclude'] and related_model._meta.label_lower in DJ_AUTH['related_filter_fields_exclude'] and field.name in DJ_AUTH['related_filter_fields_exclude'][related_model._meta.label_lower]:
                            continue

                        self._update_filter_dict(related_model, field_name=field.name, filter_type=record.filter_type, values=eval(record.filter_values))

        if 'django.contrib.sessions' in settings.INSTALLED_APPS and session:
            session['dj_auth_filter_dict'] = str(self._filter_dict)

    @classmethod
    def build_filter(self, user=None, content_type=None, session=None):
        DJ_AUTH = getattr(settings, 'DJ_AUTH', DEFAULT)

        if 'django.contrib.sessions' in settings.INSTALLED_APPS and session and 'dj_auth_filter_dict' in session:
            self._filter_dict = eval(session['dj_auth_filter_dict'])
        else:
            self.create_filter_dict(user=user, session=session)

        filter_query = {}
        exclude_query = {}

        model_class = content_type.model_class()
        # filter for the own class
        if model_class._meta.label_lower in self._filter_dict:
            filter_query.update(self._filter_dict[model_class._meta.label_lower][FILTER_ID])
            exclude_query.update(self._filter_dict[model_class._meta.label_lower][EXCLUDE_ID])
        else:
            # if the class is not set as filter, check FK an M2M of the class
            related_models = {}
            for field in model_class._meta.get_fields():
                if field.is_relation and field.related_model and not field.auto_created:
                    if field.related_model._meta.label_lower in self._filter_dict:
                        if DJ_AUTH['global_fields_exclude'] and field.name in DJ_AUTH['global_fields_exclude']:
                            continue

                        if DJ_AUTH['related_filter_fields_exclude'] and model_class._meta.label_lower in DJ_AUTH['related_filter_fields_exclude'] and field.name in DJ_AUTH['related_filter_fields_exclude'][model_class._meta.label_lower]:
                            continue

                        if field.related_model not in related_models:
                            related_models[field.related_model] = []
                        related_models[field.related_model].append(field.name)

            for related_model, field_name_list in related_models.iteritems():
                for filter_text, filter_value in self._filter_dict[related_model._meta.label_lower][FILTER_ID].iteritems():
                    filter_to_add = {}
                    for field_name in field_name_list:
                        filter_to_add.update({'%s__%s' % (field_name, filter_text): filter_value})

                    filter_query.update(filter_to_add)

                for filter_text, filter_value in self._filter_dict[related_model._meta.label_lower][EXCLUDE_ID].iteritems():
                    filter_to_add = {}
                    for field_name in field_name_list:
                        filter_to_add.update({'%s__%s' % (field_name, filter_text): filter_value})

                    exclude_query.update(filter_to_add)

        logger.debug("%s filter %s" % (model_class._meta.label_lower, filter_query))
        logger.debug("%s exclude %s" % (model_class._meta.label_lower, exclude_query))

        return filter_query, exclude_query


class ObjectFilterQuerySetMixin(object):

    def apply_user_object_filter(self, user=None, session=None):
        queryset = self
        if user and not isinstance(user, AnonymousUser):
            filter_query, exclude_query = ObjectFilter.build_filter(user, ContentType.objects.get_for_model(self.model), session=session)
            if exclude_query:
                queryset = self.exclude(**exclude_query).distinct()
            if filter_query:
                queryset = self.filter(**filter_query).distinct()

        return queryset

    def apply_user_generic_objects_filter(self, user=None, session=None):
        queryset = self

        DATABASES = getattr(settings, 'DATABASES', {})
        if 'default' in DATABASES and 'ENGINE' in DATABASES['default'] and DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
            data = self.model.objects.distinct('content_type').order_by('content_type')
        else:
            data = self.model.objects.distinct()

        for record in data:
            model_class = record.content_type.model_class()
            filter_query, exclude_query = ObjectFilter.build_filter(user, content_type=record.content_type, session=session)

            if exclude_query:
                ids = model_class.objects.filter(**exclude_query).values_list('id', flat=True)
                queryset = queryset.exclude(content_type_id=record.content_type.id, object_id__in=model_class.objects.exclude(id__in=ids).values_list('id', flat=True))
            if filter_query:
                ids = model_class.objects.filter(**filter_query).values_list('id', flat=True)
                queryset = queryset.exclude(content_type_id=record.content_type.id, object_id__in=model_class.objects.exclude(id__in=ids).values_list('id', flat=True))

        return queryset
