from django.http import HttpResponse, HttpResponseNotFound
from cStringIO import StringIO
from ConfigParser import ConfigParser
from rufus.models import Provider, ServiceCode

def export(request, command):
    output = StringIO()
    config = ConfigParser()
    if command == 'provider':
        body, filename = provider(output, config)
    elif command == 'service':
        body, filename = service(output, config)
    else:
        return HttpResponseNotFound()
    #return HttpResponse(body)
    response = HttpResponse(body, mimetype="application/octet-stream")
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


def provider(output, config):
    for provider in Provider.objects.all():
        section = 'provider {0}'.format(provider.name)
        config.add_section(section)
        config.set(section, 'country', provider.country.config_name)
        config.set(section, 'timeout', provider.timeout)
        config.set(section, 'adaptor', provider.adaptor)
        config.set(section, 'cdr_string', provider.cdr_string)
        extras = provider.specialization.all()
        for opt in provider.owns.all():
            config.set(section, opt.key.name, opt.value)
        if extras:
            config.set(section, 'service', ','.join([extra.name for extra in extras]))
            for extra in extras:
                x_section = 'extra {0} {1}'.format(provider.name, extra.name)
                config.add_section(x_section)
                for opt in extra.owns.all():
                    config.set(x_section, opt.key.name, opt.value)
    config.write(output)
    return output.getvalue(), 'rufus.conf'

def service(output, config):
    for sc in ServiceCode.objects.all():
        section = 'servicecode {0}'.format(sc.name)
        config.add_section(section)
        config.set(section, 'country', sc.provider.country.config_name)
        config.set(section, 'tariff', sc.tariff)
        config.set(section, 'currency', sc.currency)
        for opt in sc.owns.all():
            config.set(section, opt.key.name, opt.value)
    config.write(output)
    return output.getvalue(), 'service_codes.conf'
