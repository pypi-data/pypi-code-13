# -*- coding: utf-8 -*-
from trytond.pool import Pool
from .user import NereidUser, NereidUserParty, Party


def register():
    Pool.register(
        NereidUser,
        NereidUserParty,
        Party,
        module='nereid_party_multi_user', type_='model')
