from countries.models import Country, Currency
from django.contrib import admin

class CountryAdmin(admin.ModelAdmin):
	list_display = ('printable_name', 'iso',)

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol', )

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Country, CountryAdmin)
