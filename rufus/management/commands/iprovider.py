from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import ConfigParser
from rufus.models import *
from countries.models import Country

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--filein', '-f', action='store',
                    dest='filein',
                    help='Configuration file'),
    )

    args = ''
    help = 'Parse configuration file'

    def handle(self, *args, **options):
        if not options['filein']:
            raise CommandError('Need a file to parse; use --filein')
        config = ConfigParser.ConfigParser()
        try:
            config.readfp(open(options['filein']))
        except IOError:
            raise CommandError('File {0} Not Found'.format(options['filein']))
        except ConfigParser.Error as e:
            raise CommandError('File {0} isn\'t\
                               recognized'.format(options['filein']))
        providers = ( p for p in config.sections() if p.startswith('provider'))
        for provider in providers:
            params = self.provider_mandatory(config, provider)
            provider_obj = Provider.objects.create(**params)
            if config.has_option(provider,'service'):
                service_values = config.get(provider, 'service').split(',')
                for service_value in service_values:
                    service_value = service_value.strip()
                    extra_section = "extra {0} {1}".format(params['name'], service_value)
                    if config.has_section(extra_section):
                        extra_obj = Extra.objects.create(name=service_value,
                                             provider=provider_obj)
                        for k,v in config.items(extra_section):
                            opt_key, created = OptionalKey.objects.get_or_create(name=k)
                            OptionalParameter.objects.create(key=opt_key,
                                                             value=v,
                                                             owner=extra_obj,)
                        params['service'] = True
            for k,v in config.items(provider):
                if k not in params.keys():
                    opt_key, created = OptionalKey.objects.get_or_create(name=k)
                    OptionalParameter.objects.create(key=opt_key,
                                                     value=v,
                                                     owner=provider_obj,)

    def provider_mandatory(self, config, section):
        adaptor = req_value(config, section, 'adaptor')
        country = req_value(config, section, 'country').upper()
        cdr_string = req_value(config, section, 'cdr_string')
        timeout = req_value(config, section, 'timeout')
        params = dict()
        params['name']             = section.replace('provider ', '')
        params['adaptor'], created = Adaptor.objects.get_or_create(name=adaptor)
        try:
            real_country = Country.objects.get(pk=country)
            params['country'], created = ConfigCountry.objects.get_or_create(pk=country, country=real_country)
        except:
            while True:
                try:
                    real_country_name  = raw_input("{0} NOT FOUND, Insert a valid country:\n".format(country))
                    real_country = Country.objects.get(pk=real_country_name)
                    params['country'], created = ConfigCountry.objects.get_or_create(pk=country, country=real_country)
                    break
                except:
                    pass


        params['cdr_string']       = cdr_string
        params['timeout']          = timeout
        return params

def req_value(config, section, option):
    if config.has_option(section, option):
        return config.get(section, option)
    ret = ''
    while not ret:
        ret = raw_input('Need value for {0} {1}:\n'.format(section,option))
    return ret
