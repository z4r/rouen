from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import ConfigParser
from rufus.models import *

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--filein', '-f', action='store',
                    dest='filein',
                    help='Configuration file'),
    )

    args = ('provider', 'service')
    help = 'Parse configuration file'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Only one argument accepted!')
        command = args[0]
        if command not in Command.args:
            raise CommandError('You can import only {0}'.format(' or '.join(Command.args)))
        if not options['filein']:
            raise CommandError('Need a file to parse; use --filein')
        config = ConfigParser.ConfigParser()
        try:
            config.readfp(open(options['filein']))
        except IOError:
            raise CommandError('File {0} Not Found'.format(options['filein']))
        except ConfigParser.Error as e:
            raise CommandError('File {0} isn\'t recognized'.format(options['filein']))
        getattr(Command, command)(config)

    @staticmethod
    def provider(config):
        providers = ( p for p in config.sections() if p.startswith('provider'))
        for provider in providers:
            params = Command.provider_mandatory(config, provider)
            provider_obj = Provider.objects.create(**params)
            if config.has_option(provider,'service'):
                service_values = config.get(provider, 'service').split(',')
                for service_value in service_values:
                    service_value = service_value.strip()
                    extra_section = "extra {0} {1}".format(params['name'], service_value)
                    if config.has_section(extra_section):
                        extra_obj = Extra.objects.create(name=service_value, provider=provider_obj)
                        for k,v in config.items(extra_section):
                            opt_key, created = OptionalKey.objects.get_or_create(name=k)
                            OptionalParameter.objects.create(key=opt_key, value=v, owner=extra_obj)
                        params['service'] = True
            for k,v in config.items(provider):
                if k not in params.keys():
                    opt_key, created = OptionalKey.objects.get_or_create(name=k)
                    OptionalParameter.objects.create(key=opt_key, value=v, owner=provider_obj)

    @staticmethod
    def provider_mandatory(config, section):
        adaptor                     = req_value(config, section, 'adaptor')
        country                     = req_value(config, section, 'country').upper()
        cdr_string                  = req_value(config, section, 'cdr_string')
        timeout                     = req_value(config, section, 'timeout')
        params                      = dict()
        params['name']              = section.replace('provider ', '')
        params['adaptor'], created  = Adaptor.objects.get_or_create(name=adaptor)
        try:
            params['country'] = Country.objects.get(config_name=country)
        except:
            raise CommandError('{0} Not Found'.format(country))
        params['cdr_string']       = cdr_string
        params['timeout']          = timeout
        return params

    @staticmethod
    def service(config):
        ServiceCode.objects.all().delete() 
        services = ( s for s in config.sections() if s.startswith('servicecode'))
        for service in services:
            params = Command.service_mandatory(config, service)
            try:
                service_obj = ServiceCode.objects.create(**params)
            except:
                raise CommandError('{0}: on Create'.format(service))
            for k,v in config.items(service):
                if k not in params.keys():
                    opt_key, created = OptionalKey.objects.get_or_create(name=k)
                    OptionalParameter.objects.create(key=opt_key, value=v, owner=service_obj)

    @staticmethod
    def service_mandatory(config, section):
        provider = req_value(config, section, 'provider')
        tariff   = req_value(config, section, 'tariff')
        params = dict()
        params['name']              = section.replace('servicecode ', '')
        try:
            params['provider']          = Provider.objects.get(name=provider)
        except:
            raise CommandError('{0}: Provider {1} Not Found'.format(section, provider))
        params['tariff']            = tariff
        if config.has_option(section, 'currency'):
            currency = config.get(section, 'currency')
            try:
                params['currency'] = Currency.objects.get(code=currency)
            except:
                raise CommandError('{0}: Currency {1} Not Found'.format(section, currency))
        return params


def req_value(config, section, option):
    if config.has_option(section, option):
        return config.get(section, option)
    ret = ''
    while not ret:
        ret = raw_input('Need value for {0} {1}:\n'.format(section,option))
    return ret
