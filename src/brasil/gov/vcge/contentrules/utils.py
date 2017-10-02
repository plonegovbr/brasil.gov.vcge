# -*- coding:utf-8 -*-
from Acquisition import aq_base
from Products.CMFPlone.utils import safe_hasattr


def vcge_available(obj):
    """Valida se o objeto tem o atributo de armazenamento do VCGE."""
    return safe_hasattr(aq_base(obj), 'skos')


def vcge_for_object(obj):
    """Retorna valores armazenados no atributo VCGE de um objeto."""
    skos = []
    if safe_hasattr(aq_base(obj), 'skos'):
        skos = obj.skos
    return skos


def set_vcge(obj, skos):
    """Armazena valores no atributo VCGE de um objeto."""
    if safe_hasattr(aq_base(obj), 'skos'):
        obj.skos = skos
    return True
