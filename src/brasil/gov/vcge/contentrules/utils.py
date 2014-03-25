# -*- coding:utf-8 -*-
from Acquisition import aq_base


def vcge_available(obj):
    """ Valida se o objeto tem o atributo de
        armazenamento do VCGE
    """
    return hasattr(aq_base(obj), 'skos')


def vcge_for_object(obj):
    """ Retorna valores armazenados no atributo
        VCGE de um objeto
    """
    skos = []
    if hasattr(aq_base(obj), 'skos'):
        skos = obj.skos
    return skos


def set_vcge(obj, skos):
    """ Armazena valores no atributo
        VCGE de um objeto
    """
    if hasattr(aq_base(obj), 'skos'):
        obj.skos = skos
    return True
