# -*- coding:utf-8 -*-
from brasil.gov.vcge import config
from plone.memoize import forever
from rdflib.namespace import SKOS

import os
import rdflib


@forever.memoize
def load_skos(data_file=config.DEFAULT_FILE):
    ''' Retorna os dados em formato de dicionarios
    '''
    path = os.path.dirname(__file__)
    data = open(os.path.join(path, 'data', data_file)).read()
    termos = parse_skos(data, format=config.DEFAULT_FORMAT)
    return termos


def parse_skos(data, format='xml'):
    ''' Realiza o parse de uma string skos
    '''
    g = rdflib.Graph()
    result = g.parse(data=data, format=format)

    objs = [s for s in result.triples((None, SKOS.prefLabel, None))]

    termos = {}
    for obj in objs:
        oId = obj[0].toPython()
        title = unicode(obj[2])
        lang = obj[2].language
        if oId not in termos:
            termos[oId] = {'title': u'', 'lang': u''}
        termos[oId]['title'] = title
        termos[oId]['lang'] = lang
    return termos
