from django.db import models
from countries.models import Country
from django.utils.translation import ugettext_lazy as _


class OptionalKey(models.Model): 
    ''' list of named parameters. It's used as a dropdown menu list that can grow.
    '''
    name       = models.CharField(_('Key'), max_length=20, primary_key=True)

    class Meta:
        verbose_name        = _('Optional Key')
        verbose_name_plural = _('Optional Keys')

    def __unicode__(self):
        return self.name


class OptionalParameterOwner(models.Model):
    '''  references provider or extra section
    '''
    name = models.CharField(_('Name'), max_length=20, unique=True)

    def __unicode__(self):
        return self.name


class OptionalParameter(models.Model):
    ''' the content of sections in rufus.conf
    ''' 
    key   = models.ForeignKey(OptionalKey, related_name='owners')
    value = models.TextField(_('Value'))
    owner = models.ForeignKey(OptionalParameterOwner, related_name='owns')

    class Meta:
        verbose_name        = _('Optional Parameter')
        verbose_name_plural = _('Optional Parameters')
        unique_together     = (('key', 'owner',),)

    def __unicode__(self):
        return "%s: %s" % (self.owner, self.key)


class Adaptor(models.Model):
    '''Name of protocol adaptor that implements aggregator
       e.g. Dada::Rufus::Adaptor::Okto
    '''
    name = models.CharField(_('Name'), max_length=100, primary_key=True)

    class Meta:
        verbose_name        = _('Adaptor')
        verbose_name_plural = _('Adaptors')

    def __unicode__(self):
        return self.name


class Provider(OptionalParameterOwner):
    '''Name of phone company using an aggregator
       e.g. provider 100 uses adaptor Dada::Rufus::Adaptor::Okto
    '''
    adaptor    = models.ForeignKey(Adaptor)
    cdr_string = models.CharField(_('CDR String'), max_length=40)
    timeout    = models.PositiveSmallIntegerField(_('Timeout [sec]'), default=60)
    country    = models.ForeignKey(Country)

    class Meta:
        verbose_name        = _('Provider')
        verbose_name_plural = _('Providers')


class Extra(OptionalParameterOwner):
    '''Some providers share common params. Those params are inserted in a 
       special section with this name.
    '''
    provider    = models.ForeignKey(Provider, related_name='specialization')

    class Meta:
        verbose_name        = _('Extra')
        verbose_name_plural = _('Extra')
