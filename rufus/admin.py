from rufus.models import *
from rufus.exporter import get_ini
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseNotFound

class ExtraInline(admin.TabularInline):
    model = Extra
    fk_name = 'provider'
    extra = 0


class ServiceCodeInline(admin.TabularInline):
    model   = ServiceCode
    fk_name = 'provider'
    extra   = 0


class OptionalParameterInline(admin.TabularInline):
    model = OptionalParameter
    readonly_fields = ('key',)
    extra = 0


class ProviderAdmin(admin.ModelAdmin):
    list_display    = ('name', 'country', 'timeout', 'adaptor', 'cdr_string', 'service_count', )
    inlines         = (OptionalParameterInline, ServiceCodeInline, ExtraInline, )
    search_fields   = ('name', )
    list_filter     = ('country', )


class ExtraAdmin(admin.ModelAdmin):
    list_display    = ('name', 'provider',)
    inlines         = (OptionalParameterInline,)
    search_fields   = ('name', )


class ServiceCodeAdmin(admin.ModelAdmin):
    list_display    = ('name', 'tariff', 'currency', 'provider',)
    inlines         = (OptionalParameterInline,)
    search_fields   = ('name', )
    list_filter     = ('currency', )
    actions         = ('export_ini',)

    def export_ini(self, request, queryset):
        body = get_ini(queryset)
        response = HttpResponse(body, mimetype="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename={0}'.format('rufus.ini')
        return response
    export_ini.short_description = _('Export INI Files')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('iso', 'printable_name', 'currency', )


admin.site.register(Country, CountryAdmin)
admin.site.register(Currency)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(OptionalKey) 
admin.site.register(OptionalParameter)
admin.site.register(Adaptor)
admin.site.register(Extra, ExtraAdmin)
admin.site.register(ServiceCode, ServiceCodeAdmin)
