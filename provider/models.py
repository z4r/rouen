from django.db import models
from countries.models import Country
from django.utils.translation import ugettext_lazy as _

class Adaptor(models.Model):
    '''
    '''
    name = models.CharField(_('Name'), max_length=20, primary_key=True)

    class Meta:
        verbose_name        = _('Adaptor')
        verbose_name_plural = _('Adaptors')


class Provider(models.Model):
    '''
    '''
    name       = models.CharField(_('Name'), max_length=20, primary_key=True)
    adaptor    = models.ForeingKey(Adaptor)
    cdr_string = models.CharField(_('CDR String'), max_length=40)
    timeout    = models.PositiveSmallIntegerField(_('Timeout [sec]'), default=60)
    country    = models.ForeingKey(Country)

    class Meta:
        verbose_name        = _('Provider')
        verbose_name_plural = _('Providers')


class Extra(models.Model):
    '''
    '''
    name       = models.CharField(_('Name'), max_length=20, primary_key=True)
    provider    = models.ForeingKey(Provider)

    class Meta:
        verbose_name        = _('Extra')
        verbose_name_plural = _('Extra')


class OptionalKey(models.Model): 
    name       = models.CharField(_('Key'), max_length=20, primary_key=True)

    class Meta:
        verbose_name        = _('Optional Key')
        verbose_name_plural = _('Optional Keys')

class AbstractOptionalParameter(models.Model):
    key   = models.ForeingKey(OptionalKey)
    value = models.TextField(_('Value'))

    class Meta:
        abstract = True

class ProviderOptionalParameter(AbstractOptionalParameter):
    provider = models.ForeingKey(Provider)

    class Meta:
        verbose_name        = _('Optional Provider Parameter')
        verbose_name_plural = _('Optional Provider Parameters')


class ExtraOptionalParameter(AbstractOptionalParameter):
    extra = models.ForeingKey(Extra)

    class Meta:
        verbose_name        = _('Optional Extra Parameter')
        verbose_name_plural = _('Optional Extra Parameters')
