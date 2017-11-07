# -*- coding: utf-8 -*-
from brasil.gov.vcge.testing import INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.site.hooks import setSite

import unittest


class BaseTestCase(unittest.TestCase):
    """Base test case to be used by other tests."""

    layer = INTEGRATION_TESTING

    def setUpUser(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)

    def setUp(self):
        portal = self.layer['portal']
        setSite(portal)
        self.portal = portal
        self.registry = getattr(self.portal, 'portal_registry')
        self.ct = getattr(self.portal, 'portal_catalog')
        self.prefix = 'plone.app.querystring.field.skos'
        self.setUpUser()


class TestCollectionRegistrySetup(BaseTestCase):
    """Garante que temos a opcao de filtrar colecoes pelo VCGE."""

    def test_querystring_field_available(self):
        registry = self.registry
        prefix = self.prefix
        self.assertTrue(prefix + '.title' in registry)

    def test_querystring_field_title(self):
        registry = self.registry
        prefix = self.prefix
        self.assertEqual(registry[prefix + '.title'], 'VCGE')

    def test_querystring_field_description(self):
        registry = self.registry
        prefix = self.prefix
        self.assertEqual(
            registry[prefix + '.description'],
            'Vocabulario Controlado do Governo Eletronico',
        )

    def test_querystring_field_is_enabled(self):
        registry = self.registry
        prefix = self.prefix
        self.assertEqual(registry[prefix + '.enabled'], True)

    def test_querystring_field_not_sortable(self):
        registry = self.registry
        prefix = self.prefix
        self.assertEqual(registry[prefix + '.sortable'], False)

    def test_querystring_field_vocabulary(self):
        registry = self.registry
        prefix = self.prefix
        self.assertEqual(registry[prefix + '.vocabulary'], 'brasil.gov.vcge')

    def test_querystring_field_group(self):
        registry = self.registry
        prefix = self.prefix
        self.assertEqual(registry[prefix + '.group'], 'Metadata')

    def test_querystring_field_operations(self):
        registry = self.registry
        prefix = self.prefix
        self.assertEqual(
            registry[prefix + '.operations'],
            [
                'plone.app.querystring.operation.selection.is',
                'plone.app.querystring.operation.string.is',
            ],
        )
