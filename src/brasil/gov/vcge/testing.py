# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone import api

import pkg_resources

HAS_DEXTERITY = 'plone.app.dexterity' in pkg_resources.AvailableDistributions()

VCGE_SKOS = ['http://vocab.e.gov.br/2011/03/vcge#regime-politico']


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import brasil.gov.vcge
        self.loadZCML(package=brasil.gov.vcge)

    def setUpPloneSite(self, portal):
        # Aplicamos os profiles para Archetypes e Dexterity
        self.applyProfile(portal, 'brasil.gov.vcge.at:default')
        if HAS_DEXTERITY:
            self.applyProfile(portal, 'brasil.gov.vcge.dx:default')
        with api.env.adopt_roles(roles=['Manager']):
            content = portal[portal.invokeFactory('News Item', 'my-news-item')]
            content.skos = VCGE_SKOS
            content.title = u"Test content"
            content.description = u"Just a test content"
            content.contributors = (u'Jane Doe', u'John Doe')
            portal['my-news-item'].reindexObject()


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='brasil.gov.vcge:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='brasil.gov.vcge:Functional')
