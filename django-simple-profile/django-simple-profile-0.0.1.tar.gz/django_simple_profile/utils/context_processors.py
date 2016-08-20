# -*- coding: utf-8 -*-
import json

from .parameter import Parameter
from ..api import user_detail, user_profile


def add_user_profile(request):
    profile = Parameter()
    if request.user.is_authenticated:
        profile = user_profile.MyUserProfile.get_uid(request.user.id) or profile
        profile.settings = json.loads(profile.get('settings') or '{}')
    return {'user_profile': profile}


def add_user_detail(request):
    detail = Parameter()
    if request.user.is_authenticated:
        detail = user_detail.MyUserDetail.get_uid(request.user.id) or detail
    return {'user_detail': detail}
