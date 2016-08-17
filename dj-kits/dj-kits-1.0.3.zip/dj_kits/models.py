# -*- coding: utf-8 -*-
try:
    from caching.base import CachingManager, CachingQuerySet, CachingMixin
    from safedelete import SOFT_DELETE
    from safedelete.models import safedelete_mixin_factory
except ImportError:
    SoftDeleteMixinSupportCachingMachine = CachingMixinWithSoftDelete = object
else:

    SoftDeleteMixinSupportCachingMachine = safedelete_mixin_factory(SOFT_DELETE,
                                                                    manager_superclass=CachingManager,
                                                                    queryset_superclass=CachingQuerySet)

    class CachingMixinWithSoftDelete(CachingMixin, SoftDeleteMixinSupportCachingMachine):

        class Meta:
            abstract = True