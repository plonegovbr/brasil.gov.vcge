# -*- coding:utf-8 -*-
from Acquisition import aq_base


def vcge_available(obj):
    ''' '''
    return hasattr(aq_base(obj), 'skos')


def vcge_for_object(obj):
    ''' '''
    skos = []
    if hasattr(aq_base(obj), 'skos'):
        skos = obj.skos
    return skos


def set_vcge(obj, skos):
    ''' '''
    if hasattr(aq_base(obj), 'skos'):
        obj.skos = skos
    return True
