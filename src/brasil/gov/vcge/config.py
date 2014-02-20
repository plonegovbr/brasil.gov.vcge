# -*- coding:utf-8 -*-
from Products.CMFPlone import interfaces as plone_interfaces
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from zope.interface import implements

PROJECTNAME = "brasil.gov.vcge"

DEFAULT_FILE = 'vcge.n3'
DEFAULT_FORMAT = 'n3'
NAMESPACE = 'http://www.w3.org/2004/02/skos/core#'


class HiddenProducts(object):
    """ Oculta produtos do QuickInstaller """
    implements(qi_interfaces.INonInstallable)

    def getNonInstallableProducts(self):
        return [
            'brasil.gov.vcge.upgrades.v2000',
        ]


class HiddenProfiles(object):
    """ Oculta profiles da tela inicial de criacao do site """
    implements(plone_interfaces.INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            'brasil.gov.vcge:uninstall',
            'brasil.gov.vcge.upgrades.v2000:default'
        ]
