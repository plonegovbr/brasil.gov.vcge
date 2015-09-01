# -*- coding:utf-8 -*-
from brasil.gov.vcge.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile
from plone import api


import logging


logger = logging.getLogger(PROJECTNAME)


from Products.CMFCore.interfaces import IFolderish

def recurse_all_content(portal):
    """Atualizamos o metadado skos para vcge
    """
    def recurse(context):
        """ Recurse through all content on Plone site """
        if hasattr(context, 'skos'):
            logger.info(context.title)
            logger.info(context.skos)
            context.vcge = context.skos
            del context.skos

        logger.info("Recursing to item:" + str(context))

        # Make sure that we recurse to real folders only,
        # otherwise contentItems() might be acquired from higher level
        if IFolderish.providedBy(context):
            for id, item in context.contentItems():
                recurse(item)

    recurse(portal)
    logger.info('Atualizacao do skos_VCGE completa')

def apply_profile(context):
    """Atualiza perfil para versao 2001."""
    profile = 'profile-brasil.gov.vcge.upgrades.v2001:default'
    loadMigrationProfile(context, profile)
    recurse_all_content(api.portal.get())
    ct = api.portal.get_tool('portal_catalog')
    ct.clearFindAndRebuild()
    
    logger.info('Atualizado para versao 2001')
