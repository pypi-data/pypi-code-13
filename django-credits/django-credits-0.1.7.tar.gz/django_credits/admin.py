from django.contrib import admin

from .models import (Contribution,
                     Contributor,
                     Credit)


class ContributionInline(admin.TabularInline):

    model = Contribution


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):

    list_display = ("given_name",
                    "family_name")
    inlines = [ContributionInline]


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):

    list_display = ("headline",)
    inlines = [ContributionInline]
