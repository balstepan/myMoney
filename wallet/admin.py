from django.contrib import admin
from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'user')
    list_filter = ('name', 'user')
    search_fields = ('name',)
    ordering = ('name', 'user')


@admin.register(models.CostCategory)
class CostCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'user')
    list_filter = ('name', 'parent', 'user')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name', 'user')


@admin.register(models.Cost)
class CostAdmin(admin.ModelAdmin):
    list_display = ('category', 'note', 'value', 'currency', 'user')
    list_filter = ('currency', 'user', 'account', 'category')
    search_fields = ('note',)
    ordering = ('updated_at', 'user')


@admin.register(models.IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'user')
    list_filter = ('name', 'user')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name', 'user')


@admin.register(models.Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('category', 'note', 'value', 'currency', 'user')
    list_filter = ('currency', 'user', 'account', 'category')
    search_fields = ('note',)
    ordering = ('updated_at', 'user')


@admin.register(models.Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('from_account',
                    'to_account',
                    'value_from',
                    'user')
    list_filter = ('from_account',
                   'to_account',
                   'user')
    ordering = ('created_at', 'user')
