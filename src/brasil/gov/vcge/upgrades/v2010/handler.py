# -*- coding:utf-8 -*-
from brasil.gov.vcge.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile
from rdflib.namespace import DCTERMS
from plone import api
from Products.CMFCore.interfaces import IFolderish
from brasil.gov.vcge import config

import shutil
import os
import rdflib
import logging


logger = logging.getLogger(PROJECTNAME)


def apply_profile(context):
    """Atualiza perfil para versao 2010."""
    profile = 'profile-brasil.gov.vcge.upgrades.v2010:default'
    loadMigrationProfile(context, profile)
    recurse_all_content(api.portal.get())
    path = os.path.dirname(config.__file__)
    old_file = os.path.join(path, 'data', config.DEFAULT_FILE)
    os.remove(old_file)
    path = os.path.dirname(__file__)
    shutil.copy2(os.path.join(path, 'data', 'vcge2.0.3.n3'), old_file)
    ct = api.portal.get_tool('portal_catalog')
    ct.clearFindAndRebuild()
    logger.info('Atualizado para versao 2010')


def recurse_all_content(portal):
    """Atualizamos o metadado skos para vcge
    """
    termos = load_replacedBy()
    logger.info(termos)

    def recurse(context):
        """ Recurse through all content on Plone site """
        if hasattr(context, 'skos'):
            logger.info(context.title)
            logger.info(context.skos)
            skos_new = []
            for item in context.skos:
                skos_new.append(termos[str(item)]['replacedBy'])

            context.skos = skos_new
            logger.info("Novo valor: " + str(skos_new))

        logger.info("Recursing to item:" + str(context))

        # Make sure that we recurse to real folders only,
        # otherwise contentItems() might be acquired from higher level
        if IFolderish.providedBy(context):
            for id, item in context.contentItems():
                recurse(item)

    recurse(portal)
    logger.info('Atualizacao do VCGE 1 para 2 completa')


def load_replacedBy(data_file='vcge2.0.3.n3'):
    path = os.path.dirname(__file__)
    data = open(os.path.join(path, 'data', data_file)).read()
    termos = parse_replacedBy(data)
    return termos


def parse_replacedBy(data):
    g = rdflib.Graph()
    result = g.parse(data=data, format='n3')
    objs = [s for s in result.triples((None, DCTERMS.replaces, None))]

    termos = {}
    for obj in objs:
        oId = obj[2].toPython()
        replacedBy = unicode(obj[0])
        if oId not in termos:
            termos[oId] = {'replacedBy': u''}
        termos[oId]['replacedBy'] = replacedBy

    return termos
