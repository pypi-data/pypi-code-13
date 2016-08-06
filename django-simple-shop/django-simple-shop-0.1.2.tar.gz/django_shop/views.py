# coding=utf-8
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.forms import formset_factory
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView, TemplateView

from .models import ProductCategory, Product, DeliveryType, PaymentType, Order
from .forms import BasketModifyForm, OrderForm, ProductOrderForm, \
    ReceiverForm, AddressForm
from .basket import Basket, BasketModificationError


class ProductCategoriesListView(ListView):
    """Список категорий в магазине"""

    model = ProductCategory

    def get_queryset(self):
        qs = super(ProductCategoriesListView, self).get_queryset()
        return qs.prefetch_related('products')


class ProductCategoryDetailView(DetailView):
    """Список товаров в категории"""

    model = ProductCategory

    def get_queryset(self):
        qs = super(ProductCategoryDetailView, self).get_queryset()
        return qs.prefetch_related('products')


class ProductDetailView(DetailView):
    """Страница продукта"""

    model = Product

    def get_queryset(self):
        qs = super(ProductDetailView, self).get_queryset().filter(category__slug=self.kwargs.get('cat_slug'))
        return qs.select_related('category')


class BasketModifyFormView(FormView):
    """Ручка для изменения корзины в AJAX-запросе"""

    form_class = BasketModifyForm

    def get(self, request, *args, **kwargs):
        # GET запросы не принимаем
        return HttpResponseNotAllowed(['POST'])

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return super(BasketModifyFormView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        basket = Basket(self.request.session)
        try:
            form.perform_action(basket)
        except BasketModificationError as e:
            return JsonResponse({'success': False, 'error': e.message})
        basket_description = {
            'items_num': basket.items_num,
            'price': round(float(basket.price), 2),
        }
        if form.cleaned_data['response'] == BasketModifyForm.RESPONSE_FULL:
            # TODO: отдавать реальное описание продукта
            basket_description['items'] = []
        return JsonResponse({'success': True, 'basket': basket_description})

    def form_invalid(self, form):
        return JsonResponse({'success': False})


class CheckoutFormView(TemplateView):
    """Страница подтверждения заказа"""

    template_name = 'django_shop/cart.html'

    def get(self, request, *args, **kwargs):
        basket = Basket(request.session)
        products_form = formset_factory(ProductOrderForm, extra=0)(
            initial=[{'product': p.id, 'amount': a} for p, a, _ in basket]
        )
        return super(CheckoutFormView, self).get(
            request, *args,
            order_form=OrderForm(),
            products_form=products_form,
            reciever_form=ReceiverForm(),
            address_form=AddressForm(),
            delivery_types=DeliveryType.objects.filter(is_active=True),
            payment_types=PaymentType.objects.filter(is_active=True),
            **kwargs
        )

    def post(self, request, *_, **kwargs):
        products_form = formset_factory(ProductOrderForm, extra=0)(
            request.POST)
        order_form = OrderForm(request.POST)
        receiver_form = ReceiverForm(request.POST)
        address_form = AddressForm(request.POST)
        for f in (products_form, order_form, receiver_form, address_form):
            if not f.is_valid():
                break
        else:
            order = Order.from_forms(
                products_form.cleaned_data, order_form.cleaned_data,
                receiver_form.cleaned_data, address_form.cleaned_data,
                request.session.session_key)
            basket = Basket(request.session)
            basket.clean()

            order.send_emails()
            if order.payment is not None and not order.payment.is_started:
                return redirect(order.payment.get_payment_submit_url())
            return redirect(order)

        context = self.get_context_data(
            order_form=order_form,
            products_form=products_form,
            reciever_form=receiver_form,
            address_form=address_form,
            delivery_types=DeliveryType.objects.filter(is_active=True),
            payment_types=PaymentType.objects.filter(is_active=True),
            **kwargs
        )
        return self.render_to_response(context)


class OrderView(DetailView):
    """Страница с описанием товара. Доступна только тому, кто заказывал и стафу"""

    model = Order
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        c = super(OrderView, self).get_context_data(**kwargs)
        if 'success' in self.request.GET:
            c['payment_success'] = int(self.request.GET['success'])
        else:
            c['payment_success'] = None
        return c

    def get_queryset(self):
        qs = super(OrderView, self).get_queryset()
        if settings.DEBUG or self.request.user.is_staff:
            return qs
        return qs.filter(sid=self.request.session.session_key)
