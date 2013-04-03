# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import brasil.gov.vcge
        self.loadZCML(package=brasil.gov.vcge)

    def setUpPloneSite(self, portal):
        # Aplicamos os profiles para Archetypes e Dexterity
        self.applyProfile(portal, 'brasil.gov.vcge.at:default')
        self.applyProfile(portal, 'brasil.gov.vcge.dx:default')


FIXTURE = Fixture()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='brasil.gov.vcge:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='brasil.gov.vcge:Functional')
