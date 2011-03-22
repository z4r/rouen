from countries.models import Country
from django.contrib import admin

class CountryAdmin(admin.ModelAdmin):
	list_display = ('printable_name', 'iso',)

admin.site.register(Country, CountryAdmin)
