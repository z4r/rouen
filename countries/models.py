#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Currency(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=25)
    symbol = models.CharField(max_length=1)

    class Meta:
        verbose_name        = _('Currency')
        verbose_name_plural = _('Currencies')

    def __unicode__(self):
        return self.code


class Country(models.Model):
    """
    International Organization for Standardization (ISO) 3166-1 Country list
    
     * ``iso`` = ISO 3166-1 alpha-2
     * ``name`` = Official country names used by the ISO 3166/MA in capital letters
     * ``printable_name`` = Printable country names for in-text use
     * ``iso3`` = ISO 3166-1 alpha-3
     * ``numcode`` = ISO 3166-1 numeric
    
    Note::
        This model is fixed to the database table 'country' to be more general.
        Change ``db_table`` if this cause conflicts with your database layout.
        Or comment out the line for default django behaviour.
    
    """
    iso = models.CharField(_('ISO alpha-2'), max_length=2, primary_key=True)
    name = models.CharField(_('Official name (CAPS)'), max_length=128)
    printable_name = models.CharField(_('Country name'), max_length=128)
    iso3 = models.CharField(_('ISO alpha-3'), max_length=3, null=True)
    numcode = models.PositiveSmallIntegerField(_('ISO numeric'), null=True)
    currency = models.ForeignKey(Currency, blank=True, null=True) 
    
    class Meta:
        db_table = 'country'
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ('name',)
        
    def __unicode__(self):
        return self.printable_name
