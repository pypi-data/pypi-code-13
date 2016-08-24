from collections import OrderedDict
import os

from rest_framework import serializers

from nyssance.django.db.utils import get_object_or_none
from nyssance.utils.active_code import Active_code

# from ..projects.models import Contract


class CardIdStrMixin(serializers.Serializer):
    card_id_str = serializers.SerializerMethodField()

    def get_card_id_str(self, obj):
        return str(obj.card_id)


class UserMixin(serializers.Serializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        data = [{'url': item.strip()} for item in obj.user_image_urls.split('\n')]
        return OrderedDict([
            ('id', obj.user_id),
            ('images', OrderedDict([('count', len(data)), ('next', None), ('previous', None), ('results', data)]))
        ])


class UserOrderMixins(serializers.Serializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        data = [{'url': item.strip()} for item in obj.image_urls.split('\n')]
        return OrderedDict([
            ('id', obj.user_id),
            ('nickname', self.get_nickname(obj.nickname)),
            ('images', OrderedDict([('count', len(data)), ('next', None), ('previous', None), ('results', data)]))
        ])

    def get_nickname(self, nickname):
        temp_list = []
        if len(nickname) != 0:
            for x in range(len(nickname) - 1):
                temp_list.append('*')
            return nickname[0] + ''.join(temp_list)
        return nickname


class CardMixin(serializers.Serializer):
    card = serializers.SerializerMethodField()

    def get_card(self, obj):
        data = [{'url': item.strip()} for item in obj.image_urls.split('\n')]
        return OrderedDict([
            ('id', obj.card_id),
            ('id_str', str(obj.card_id)),
            ('caption', obj.card_caption),
            ('images', OrderedDict([('count', len(data)), ('next', None), ('previous', None), ('results', data)]))
        ])

'''
class ContractUrlsMixin(serializers.Serializer):
    contracts = serializers.SerializerMethodField()

    def get_contracts(self, obj):
        data = []
        if obj.contract_urls.strip() != '':
            contract_urls_list = [item for item in obj.contract_urls.split('\n')]
            for contrace_url in contract_urls_list:
                contrace_id = os.path.basename(contrace_url).split('.')[0].split('_')[-1]
                contrace_obj = get_object_or_none(Contract, using='default', pk=contrace_id)
                if contrace_obj:
                    data.append({'url': contrace_url, 'name': contrace_obj.name})
        return OrderedDict([('count', len(data)), ('next', None), ('previous', None), ('results', data)])

'''


class PromotionCodeMixin(serializers.Serializer):
    promotion_code = serializers.SerializerMethodField()

    def get_promotion_code(self, obj):
        return Active_code().encode(obj.id)


class IdCardNumberNameMixin(serializers.Serializer):
    id_card_number = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_id_card_number(self, obj):
        temp_list = []
        if len(obj.id_card_number) != 0:
            for x in range(len(obj.id_card_number) - 7):
                temp_list.append('*')
            return obj.id_card_number[:3] + ''.join(temp_list) + obj.id_card_number[-4:]
        return obj.id_card_number

    def get_name(self, obj):
        temp_list = []
        if len(obj.name) != 0:
            for x in range(len(obj.name) - 1):
                temp_list.append('*')
            return ''.join(temp_list) + obj.name[-1:]
        return obj.name
