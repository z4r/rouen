from rufus.models import *
from django.contrib import admin

class ExtraInline(admin.TabularInline):
    model = Extra
    fk_name = 'provider'

class ServiceCodeInline(admin.TabularInline):
    model = ServiceCode
    fk_name = 'provider'

class OptionalParameterInline(admin.TabularInline):
    model = OptionalParameter

class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'timeout', 'adaptor', 'cdr_string', 'service_count', )
    inlines = (OptionalParameterInline, ServiceCodeInline, ExtraInline, )
    search_fields = ('name', )
    list_filter = ('country', )

class ExtraAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider',)
    inlines = (OptionalParameterInline,)
    search_fields = ('name', )

class ServiceCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'tariff', 'currency', 'provider',)
    inlines = (OptionalParameterInline,)
    search_fields = ('name', )
    list_filter = ('currency', )

#admin.site.register(Country)
#admin.site.register(Currency)
admin.site.register(Provider, ProviderAdmin)
#admin.site.register(OptionalKey) 
#admin.site.register(OptionalParameter)
#admin.site.register(Adaptor)
admin.site.register(Extra, ExtraAdmin)
admin.site.register(ServiceCode, ServiceCodeAdmin)
