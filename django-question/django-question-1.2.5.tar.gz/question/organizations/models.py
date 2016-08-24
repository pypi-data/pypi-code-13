from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..nyssance.django.db.models import OwnerModel


TYPE_CHOICES = (
    ('i', '保险公司'),
    ('a', '代理商'),
    ('s', '超级代理商'),
    ('r', '维修厂'),
    ('o', '其他'),
)


class Organization(models.Model):
    name = models.CharField(_('name'), max_length=30)
    short_name = models.CharField(_('short_name'), max_length=10, blank=True)
    host = models.URLField(_('host'), blank=True)
    organization_code = models.CharField(_('organization_code'), max_length=20, blank=True)
    instruction_code = models.CharField(_('instruction_code'), max_length=20, blank=True)
    tax_code = models.CharField(_('tax_code'), max_length=20, blank=True)
    image_urls = models.CharField(_('image_urls'), max_length=2000, blank=True)
    remark = models.CharField(_('remark'), max_length=2000, blank=True)
    about = models.CharField(_('about'), max_length=200, blank=True)

    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')

    def __str__(self):
        return self.name


class Branch(models.Model):
    organization = models.ForeignKey(Organization)
    name = models.CharField(_('name'), max_length=50)
    short_name = models.CharField(_('short_name'), max_length=50, blank=True)
    description = models.TextField(_('description'), blank=True)
    image_urls = models.CharField(_('image_urls'), max_length=2000, blank=True)
    address = models.CharField(_('address'), max_length=200, blank=True)
    phone_number = models.CharField(_('phone_number'), max_length=200)
    type = models.CharField(_('type'), choices=TYPE_CHOICES, max_length=1, default='o')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('branch')
        verbose_name_plural = _('branches')


class PaymentAccount(OwnerModel):
    type = models.PositiveSmallIntegerField(_('type'), choices=((12, '银行'), (20, '中金账户')), default=12)
    account_name = models.CharField(_('bank_account_name'), max_length=50)  # 收款人名称:
    account_number = models.CharField(_('bank_account'), max_length=30)  # 银行账号:
    bank_code = models.PositiveSmallIntegerField(_('bank_code'), default=0)  # 银行编号:
    bank_name = models.CharField(_('bank_name'), max_length=50, blank=True)  # 开户行:
    bank_branch_name = models.CharField(_('bank_branch_name'), max_length=50, blank=True)  # 分行信息:
    bank_province = models.CharField(_('bank_province'), max_length=50, blank=True)  # 银行省份: FIXME: 字段名错误, 且不是特别需要继承OwnerModel
    bank_city = models.CharField(_('bank_city'), max_length=50, blank=True)  # 银行城市:
    image_urls = models.CharField(_('image_urls'), max_length=2000, blank=True)
    organization = models.ForeignKey(Organization)

    class Meta:
        verbose_name = _('payment_account')
        verbose_name_plural = _('payment_accounts')

    def __str__(self):
        return '{}({})'.format(self.account_name, self.bank_name)
