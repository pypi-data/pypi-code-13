# -*- coding: utf-8 -*-
from repositories.integration.base import notifications
from repositories.catalogo.models import (
    Produto,
    Marca,
    Categoria,
    ProdutoEstoque,
    ProdutoImagem,
    ProdutoGradeVariacao)
from repositories.integration.serializers import (
    ProdutoSerializer, MarcaSerializer, CategoriaSerializer,
    ProdutoImagemSerializer, ProdutoVariacaoSerializer,
    PedidoVendaSerializer, ProdutoEstoqueSerializer
)
from repositories.pedido.models import PedidoVenda
from repositories.plataforma.models import Feature
from repositories.integration.models import ModelIntegration


class ProdutoNotifier(notifications.BaseNotificationService):

    model = Produto
    serializer = ProdutoSerializer

    def model_select_is_valid(self, obj, slug):
        result = super(ProdutoNotifier, self).model_select_is_valid(obj, slug)
        if result:
            if obj.conta.id != self.account_id:
                raise ValueError(
                    u"A conta informada ({}) não é "
                    u"valida para este Produto ({})".format(
                        obj.conta.id, self.account_id))
            result = obj.ativo
        return result and Feature.is_enabled(slug, obj.conta, plan=self.plan)


class MarcaNotifier(notifications.BaseNotificationService):

    model = Marca
    serializer = MarcaSerializer

    def model_select_is_valid(self, obj, slug):
        result = super(MarcaNotifier, self).model_select_is_valid(obj, slug)
        if result:
            if obj.conta.id != self.account_id:
                raise ValueError(
                    u"A conta informada ({}) não é "
                    u"valida para esta Marca ({})".format(
                        obj.conta.id, self.account_id))
            return obj.ativo and Feature.is_enabled(
                slug, obj.conta, plan=self.plan)


class CategoriaNotifier(notifications.BaseNotificationService):

    model = Categoria
    serializer = CategoriaSerializer

    def model_select_is_valid(self, obj, slug):
        result = super(
            CategoriaNotifier,
            self).model_select_is_valid(
            obj,
            slug)
        if result:
            if obj.conta.id != self.account_id:
                raise ValueError(
                    u"A conta informada ({}) não é "
                    u"valida para esta Categoria ({})".format(
                        obj.conta.id, self.account_id))
            return obj.ativa and Feature.is_enabled(
                slug, obj.conta, plan=self.plan)


class ProdutoImagemNotifier(notifications.BaseNotificationService):

    model = ProdutoImagem
    serializer = ProdutoImagemSerializer

    def model_select_is_valid(self, obj, slug):
        result = super(
            ProdutoImagemNotifier,
            self).model_select_is_valid(
            obj,
            slug)
        if result:
            if obj.conta.id != self.account_id:
                raise ValueError(
                    u"A conta informada ({}) não é "
                    u"valida para esta Imagem ({})".format(
                        obj.conta.id, self.account_id))
            return obj.produto.ativo and Feature.is_enabled(
                slug, obj.conta, plan=self.plan)


class ProdutoVariacaoNotifier(notifications.BaseNotificationService):

    model = ProdutoGradeVariacao
    serializer = ProdutoVariacaoSerializer

    def model_select_is_valid(self, obj, slug):
        result = super(
            ProdutoVariacaoNotifier,
            self).model_select_is_valid(obj, slug)
        if result:
            if obj.conta.id != self.account_id:
                raise ValueError(
                    u"A conta informada ({}) não é "
                    u"valida para esta Variação ({})".format(
                        obj.conta.id, self.account_id))
            return obj.produto_pai.ativo and Feature.is_enabled(
                slug, obj.conta, plan=self.plan)


class PedidoVendaNotifier(notifications.BaseNotificationService):
    model = PedidoVenda
    serializer = PedidoVendaSerializer

    def model_select_is_valid(self, obj, slug):
        result = super(
            PedidoVendaNotifier,
            self).model_select_is_valid(obj, slug)
        if result:
            if obj.conta.id != self.account_id:
                raise ValueError(
                    u"A conta informada ({}) não é "
                    u"valida para este Pedido ({})".format(
                        obj.conta.id, self.account_id))
            return Feature.is_enabled(slug, obj.conta, plan=self.plan)


class ProdutoEstoqueNotifier(notifications.BaseNotificationService):
    model = ProdutoEstoque
    serializer = ProdutoEstoqueSerializer

    def model_select_is_valid(self, obj, slug):
        print("ENTROU VALIDACAO PRODUTOESTOQUE")
        result = super(
            ProdutoEstoqueNotifier,
            self).model_select_is_valid(
            obj,
            slug)
        if result:
            if obj.conta.id != self.account_id:
                raise ValueError(
                    u"A conta informada ({}) não é "
                    u"valida para este Produto ({})".format(
                        obj.conta.id, self.account_id))
            if obj.produto.pai:
                active = obj.produto.pai.ativo
            else:
                active = obj.produto.ativo

            found_integration = False
            prod_model = None
            try:
                prod_model = ModelIntegration.objects.get(
                    account_id=obj.conta.id,
                    model_selected='produtogradevariacao'
                    if obj.produto.pai else 'produto',
                    model_selected_id=obj.id,
                    integration__slug=slug
                )
            except ModelIntegration.DoesNotExist:
                print('NÃO ENCONTROU A REFERENCIA EXTERNA DO PRODUTO NO BANCO')
                found_integration = False
            except Exception as e:
                print(
                    'Ocorreu um erro ao buscar '
                    'a referencia externa do estoque: {}'.format(e))
                found_integration = False

            if prod_model and (
                    prod_model.external_id or prod_model.external_sku_id):
                found_integration = True
            else:
                print('NÃO ENCONTROU A REFERENCIA EXTERNA DO PRODUTO NO MODELO')

            return found_integration and active and Feature.is_enabled(
                slug, obj.conta, plan=self.plan)
