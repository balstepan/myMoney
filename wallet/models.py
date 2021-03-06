from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

CURRENCIES = (
    ('BYN', 'Belarus Ruble'),
    ('RUB', 'Russian Ruble'),
    ('USD', 'United States Dollar'),
    ('EUR', 'Euro'),
)


class Account(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    slug = models.SlugField(max_length=80)
    balance = models.DecimalField(verbose_name='Balance',
                                  max_digits=10,
                                  decimal_places=2)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='accounts')
    image = models.ImageField(upload_to="icons/", null=True, blank=True)

    class Meta:
        unique_together = (('user', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wallet:account_details',
                       args=[self.user.pk, self.slug])


class CostCategory(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='cost_categories')
    slug = models.SlugField(max_length=80)
    parent = models.ForeignKey('self',
                               verbose_name='Parent category',
                               on_delete=models.CASCADE,
                               related_name='children',
                               default=None,
                               null=True,
                               blank=True)
    image = models.ImageField(upload_to="icons/", null=True, blank=True)

    class Meta:
        unique_together = (('user', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wallet:costcategory_details',
                       args=[self.user.pk, self.slug])


class Cost(models.Model):
    category = models.ForeignKey(CostCategory,
                                 verbose_name='Category',
                                 on_delete=models.CASCADE,
                                 related_name='costs')
    note = models.CharField(verbose_name='Note', max_length=250)
    value = models.DecimalField(verbose_name='Amount',
                                max_digits=10,
                                decimal_places=2)
    currency = models.CharField(max_length=30,
                                choices=CURRENCIES,
                                default='BYN')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    account = models.ForeignKey(Account,
                                null=True,
                                on_delete=models.SET_NULL,
                                related_name='costs')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='costs')

    def __str__(self):
        return self.note

    def get_absolute_url(self):
        return reverse('wallet:cost_details',
                       args=[self.id])


class IncomeCategory(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='income_categories')
    slug = models.SlugField(max_length=80)
    image = models.ImageField(upload_to="icons/", null=True, blank=True)

    class Meta:
        unique_together = (('user', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wallet:incomecategory_details',
                       args=[self.user.pk, self.slug])


class Income(models.Model):
    category = models.ForeignKey(IncomeCategory,
                                 verbose_name='Category',
                                 on_delete=models.CASCADE,
                                 related_name='incomes')
    note = models.CharField(verbose_name='Note', max_length=250)
    value = models.DecimalField(verbose_name='Amount',
                                max_digits=10,
                                decimal_places=2)
    currency = models.CharField(max_length=30,
                                choices=CURRENCIES,
                                default='BYN')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    account = models.ForeignKey(Account,
                                null=True,
                                on_delete=models.SET_NULL,
                                related_name='incomes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='incomes')

    def __str__(self):
        return self.note

    def get_absolute_url(self):
        return reverse('wallet:income_details',
                       args=[self.id])


class Transfer(models.Model):
    from_account = models.ForeignKey(Account,
                                     verbose_name='From',
                                     on_delete=models.CASCADE,
                                     related_name='transfers_from')
    to_account = models.ForeignKey(Account,
                                   verbose_name='To',
                                   on_delete=models.CASCADE,
                                   related_name='transfers_to')
    value_from = models.DecimalField(verbose_name='Value',
                                     max_digits=10,
                                     decimal_places=2)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='transfers')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'From {} to {} {} {}'.format(str(self.from_account),
                                            str(self.to_account),
                                            self.value_from,
                                            'BYN')


class Rates(models.Model):
    usd = models.DecimalField(verbose_name='USD', max_digits=10, decimal_places=4)
    eur = models.DecimalField(verbose_name='EUR', max_digits=10, decimal_places=4)
    rub = models.DecimalField(verbose_name='RUB', max_digits=10, decimal_places=4)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.updated_at)
