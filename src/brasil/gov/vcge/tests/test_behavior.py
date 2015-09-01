# -*- coding: utf-8 -*-
from brasil.gov.vcge.dx.behaviors import IVCGE
from brasil.gov.vcge.dx.behaviors import VCGE
from brasil.gov.vcge.dx.interfaces import IVCGEDx
from brasil.gov.vcge.browser.viewlets import VCGEViewlet
from brasil.gov.vcge.testing import HAS_DEXTERITY
from brasil.gov.vcge.testing import INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.site.hooks import setSite

import unittest2 as unittest


def add_folder_type(portal):
    from plone.dexterity.fti import DexterityFTI

    fti = DexterityFTI('folder')
    portal.portal_types._setObject('folder', fti)
    fti.klass = 'plone.dexterity.content.Container'
    fti.filter_content_types = False
    fti.behaviors = (
        'plone.app.dexterity.behaviors.metadata.IBasic',
        'brasil.gov.vcge.dx.behaviors.IVCGE')
    return fti


class TestVCGE(unittest.TestCase):

    def _makeOne(self):
        class Dummy(object):
            pass
        dummy = Dummy()
        return VCGE(dummy)

    def test_vcge_setter(self):
        b = self._makeOne()
        token = 'http://vocab.e.gov.br/id/governo#cultura'
        b.vcge = token
        self.assertEqual(token, b.context.vcge)

    def test_vcge_getter(self):
        b = self._makeOne()
        token = 'http://vocab.e.gov.br/id/governo#cultura'
        b.context.vcge = token
        self.assertEqual(token, b.vcge)


class TestBehavior(unittest.TestCase):
    """Test behavior applied in a content type """

    layer = INTEGRATION_TESTING

    def setUpUser(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)

    def setUpContent(self):
        token = 'http://vocab.e.gov.br/id/governo#cultura'
        self.token = token
        portal = self.portal
        oId = portal.invokeFactory('folder', 'content')
        o = IVCGE(portal[oId])
        o.vcge = [token, ]
        self.content = portal[oId]

    def setUp(self):
        if not HAS_DEXTERITY:
            self.skipTest('"dexterity" extra not included')
            return
        portal = self.layer['portal']
        self.request = self.layer['app'].REQUEST
        setSite(portal)
        self.portal = portal
        self.fti = add_folder_type(self.portal)
        self.setUpUser()
        self.portal.invokeFactory('folder', 'folder')
        self.setUpContent()

    def test_behavior_applied(self):
        content = self.content
        # Validamos se a marker interface foi aplicada
        self.assertTrue(IVCGEDx.providedBy(content))

    def test_content_information(self):
        content = self.content
        self.assertEquals(content.vcge, [self.token, ])


class TestViewlet(unittest.TestCase):
    """Test viewlet implementation with dexterity"""

    layer = INTEGRATION_TESTING

    def setUpUser(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)

    def setUpContent(self):
        token = 'http://vocab.e.gov.br/id/governo#cultura'
        portal = self.portal
        oId = portal.invokeFactory('folder', 'content')
        o = portal[oId]
        o.vcge = [token, ]
        self.content = o

    def setUp(self):
        if not HAS_DEXTERITY:
            self.skipTest('"dexterity" extra not included')
            return
        portal = self.layer['portal']
        self.request = self.layer['app'].REQUEST
        setSite(portal)
        self.portal = portal
        self.fti = add_folder_type(self.portal)
        self.setUpUser()
        self.portal.invokeFactory('folder', 'folder')
        self.setUpContent()

    def test_rel(self):
        content = self.content
        viewlet = VCGEViewlet(content, self.request, None, None)
        viewlet.update()
        rel = viewlet.rel()
        self.assertEquals(rel, u'dc:subject foaf:primaryTopic')

    def test_vcge(self):
        content = self.content
        viewlet = VCGEViewlet(content, self.request, None, None)
        viewlet.update()
        vcge = viewlet.vcge()
        self.assertEquals(len(vcge), 1)
        term = vcge[0]
        self.assertEquals(term.get('title'), u'Cultura')

    def test_vcge_not_existent(self):
        ''' Testa o que acontece quando nao temos o Extender
            aplicado a um tipo de conteudo (neste caso o proprio portal)
        '''
        portal = self.portal
        viewlet = VCGEViewlet(portal, self.request, None, None)
        viewlet.update()
        vcge = viewlet.vcge()
        self.assertEquals(len(vcge), 0)
