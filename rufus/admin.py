from rufus.models import *
from django.contrib import admin

class ExtraInline(admin.TabularInline):
    model = Extra
    fk_name = 'provider'

class OptionalParameterInline(admin.TabularInline):
    model = OptionalParameter

class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'timeout', 'adaptor', 'cdr_string', )
    inlines = (OptionalParameterInline, ExtraInline, )

class ExtraAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider',)
    inlines = (OptionalParameterInline,)

admin.site.register(Country)
admin.site.register(Currency)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(OptionalKey) 
admin.site.register(OptionalParameter)
admin.site.register(Adaptor)
admin.site.register(Extra, ExtraAdmin)
