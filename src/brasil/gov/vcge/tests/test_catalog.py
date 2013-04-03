# -*- coding: utf-8 -*-
from brasil.gov.vcge.testing import INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.site.hooks import setSite

import unittest2 as unittest


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
        self.ct = getattr(self.portal, 'portal_catalog')
        self.setUpUser()


class TestCatalogSetup(BaseTestCase):
    """ Garante que temos o indice e a coluna criados"""

    def test_index(self):
        self.assertTrue('skos' in self.ct.Indexes)

    def test_column(self):
        self.assertTrue('skos' in self.ct.schema())
