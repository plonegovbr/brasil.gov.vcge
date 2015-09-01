# -*- coding:utf-8 -*-
from Acquisition import aq_base


def vcge_available(obj):
    """ Valida se o objeto tem o atributo de
        armazenamento do VCGE
    """
    return hasattr(aq_base(obj), 'vcge')


def vcge_for_object(obj):
    """ Retorna valores armazenados no atributo
        VCGE de um objeto
    """
    vcge = []
    if hasattr(aq_base(obj), 'vcge'):
        vcge = obj.vcge
    return vcge


def set_vcge(obj, vcge):
    """ Armazena valores no atributo
        VCGE de um objeto
    """
    if hasattr(aq_base(obj), 'vcge'):
        obj.vcge = vcge
    return True
