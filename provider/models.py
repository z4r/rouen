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
    name = models.CharField(_('Name'), max_length=20, primary_key=True)


class ProviderRoot(Provider):
    '''
    '''
    adaptor    = models.ForeignKey(Adaptor)
    cdr_string = models.CharField(_('CDR String'), max_length=40)
    timeout    = models.PositiveSmallIntegerField(_('Timeout [sec]'), default=60)
    country    = models.ForeignKey(Country)

    class Meta:
        verbose_name        = _('Provider')
        verbose_name_plural = _('Providers')


class Extra(Provider):
    '''
    '''
    provider    = models.ForeignKey(ProviderRoot)

    class Meta:
        verbose_name        = _('Extra')
        verbose_name_plural = _('Extra')


class OptionalKey(models.Model): 
    name       = models.CharField(_('Key'), max_length=20, primary_key=True)

    class Meta:
        verbose_name        = _('Optional Key')
        verbose_name_plural = _('Optional Keys')


class OptionalParameter(models.Model):
    key   = models.ForeignKey(OptionalKey)
    value = models.TextField(_('Value'))
    owner = models.ForeignKey(Provider)

    class Meta:
        verbose_name        = _('Optional Parameter')
        verbose_name_plural = _('Optional Parameters')
