# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import pkg_resources


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
else:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE

HAS_DEXTERITY = 'plone.app.dexterity' in pkg_resources.AvailableDistributions()


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


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='brasil.gov.vcge:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='brasil.gov.vcge:Functional')
