from provider.models import *
from django.contrib import admin

class ExtraInline(admin.TabularInline):
    model = Extra
    fk_name = 'provider'

class OptionalParameterInline(admin.TabularInline):
    model = OptionalParameter

class ProviderAdmin(admin.ModelAdmin):
    inlines = (ExtraInline, OptionalParameterInline,)

class ExtraAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider')
    inlines = (OptionalParameterInline,)

admin.site.register(ConfigCountry)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(OptionalKey) 
admin.site.register(OptionalParameter)
admin.site.register(Adaptor)
admin.site.register(Extra, ExtraAdmin)
