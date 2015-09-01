# -*- coding: utf-8 -*-
from brasil.gov.vcge.config import PROJECTNAME
from brasil.gov.vcge.testing import HAS_DEXTERITY
from brasil.gov.vcge.testing import INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.browserlayer.utils import registered_layers
from Products.GenericSetup.upgrade import listUpgradeSteps
from zope.site.hooks import setSite

import unittest2 as unittest

STYLESHEETS = [
]


class BaseTestCase(unittest.TestCase):
    """base test case to be used by other tests"""

    layer = INTEGRATION_TESTING

    def setUpUser(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)

    def setUp(self):
        portal = self.layer['portal']
        setSite(portal)
        self.portal = portal
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.wt = getattr(self.portal, 'portal_workflow')
        self.st = getattr(self.portal, 'portal_setup')
        self.setUpUser()


class TestInstall(BaseTestCase):
    """ensure product is properly installed"""

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME),
                        '%s not installed' % PROJECTNAME)

    def test_dependencies_installed(self):
        for product in ['raptus.autocompletewidget', ]:
            self.assertTrue(self.qi.isProductInstalled(product),
                            '%s not installed' % product)

    @unittest.skipIf(not HAS_DEXTERITY, '"dexterity" extra not included')
    def test_dx_dependencies_installed(self):
        for product in ['plone.app.dexterity', ]:
            self.assertTrue(self.qi.isProductInstalled(product),
                            '%s not installed' % product)

    def test_browserlayer(self):
        from brasil.gov.vcge.interfaces import IVCGEInstalado
        self.assertIn(IVCGEInstalado, registered_layers())

    def test_cssregistry(self):
        portal_css = self.portal.portal_css
        for css in STYLESHEETS:
            self.assertTrue(css in portal_css.getResourceIds(),
                            '%s not installed' % css)


class TestUpgrade(BaseTestCase):
    """ensure product upgrades work"""

    profile = 'brasil.gov.vcge:default'

    def test_to1000_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '0')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('1000',))
                and (step[0]['source'] == ('0',))]
        self.assertEqual(len(step), 1)

    def test_to2000_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '1000')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('2000',))
                and (step[0]['source'] == ('1000',))]
        self.assertEqual(len(step), 1)

    def test_to2001_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '2000')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('2001',))
                and (step[0]['source'] == ('2000',))]
        self.assertEqual(len(step), 1)


class TestUninstall(BaseTestCase):
    """ensure product is properly uninstalled"""

    def setUp(self):
        BaseTestCase.setUp(self)
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer(self):
        from brasil.gov.vcge.interfaces import IVCGEInstalado
        self.assertTrue(IVCGEInstalado not in registered_layers())

    def test_cssregistry(self):
        portal_css = self.portal.portal_css
        for css in STYLESHEETS:
            self.assertTrue(css not in portal_css.getResourceIds(),
                            '%s installed' % css)
