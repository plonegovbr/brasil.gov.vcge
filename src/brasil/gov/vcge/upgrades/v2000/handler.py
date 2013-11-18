# -*- coding:utf-8 -*-
from brasil.gov.vcge.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

import logging


logger = logging.getLogger(PROJECTNAME)


def apply_profile(context):
    """Atualiza perfil para versao 2000."""
    profile = 'profile-brasil.gov.vcge.upgrades.v2000:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 2000')
