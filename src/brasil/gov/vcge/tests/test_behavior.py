# -*- coding: utf-8 -*-
from brasil.gov.vcge.browser.viewlets import VCGEViewlet
from brasil.gov.vcge.dx.behaviors import IVCGE
from brasil.gov.vcge.dx.behaviors import VCGE
from brasil.gov.vcge.dx.interfaces import IVCGEDx
from brasil.gov.vcge.testing import HAS_DEXTERITY
from brasil.gov.vcge.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.site.hooks import setSite

import unittest


DEXTERITY_FTI_FOLDER = 'folder'


def add_folder_type(portal):
    from plone.dexterity.fti import DexterityFTI

    fti = DexterityFTI(DEXTERITY_FTI_FOLDER)
    portal.portal_types._setObject(DEXTERITY_FTI_FOLDER, fti)
    fti.klass = 'plone.dexterity.content.Container'
    fti.filter_content_types = False
    fti.behaviors = (
        'plone.app.dexterity.behaviors.metadata.IBasic',
        'brasil.gov.vcge.dx.behaviors.IVCGE',
    )
    return fti


class TestVCGE(unittest.TestCase):

    def _makeOne(self):
        class Dummy(object):
            pass
        dummy = Dummy()
        return VCGE(dummy)

    def test_skos_setter(self):
        b = self._makeOne()
        token = 'http://vocab.e.gov.br/id/governo#cultura'
        b.skos = token
        self.assertEqual(token, b.context.skos)

    def test_skos_getter(self):
        b = self._makeOne()
        token = 'http://vocab.e.gov.br/id/governo#cultura'
        b.context.skos = token
        self.assertEqual(token, b.skos)


class TestBehavior(unittest.TestCase):
    """Test behavior applied in a content type."""

    layer = INTEGRATION_TESTING

    def setUpUser(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)

    def setUpContent(self):
        token = 'http://vocab.e.gov.br/id/governo#cultura'
        self.token = token
        portal = self.portal
        o = api.content.create(
            type=DEXTERITY_FTI_FOLDER,
            container=portal,
            id='content',
        )
        i = IVCGE(o)
        i.skos = [token]
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
        api.content.create(
            type=DEXTERITY_FTI_FOLDER,
            container=self.portal,
            id='folder',
        )
        self.setUpContent()

    def test_behavior_applied(self):
        content = self.content
        # Validamos se a marker interface foi aplicada
        self.assertTrue(IVCGEDx.providedBy(content))

    def test_content_information(self):
        content = self.content
        self.assertEqual(content.skos, [self.token])


class TestViewlet(unittest.TestCase):
    """Test viewlet implementation with Dexterity."""

    layer = INTEGRATION_TESTING

    def setUpUser(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)

    def setUpContent(self):
        token = 'http://vocab.e.gov.br/id/governo#cultura'
        portal = self.portal
        o = api.content.create(
            type=DEXTERITY_FTI_FOLDER,
            container=portal,
            id='content',
        )
        o.skos = [token]
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
        api.content.create(
            type=DEXTERITY_FTI_FOLDER,
            container=self.portal,
            id='folder',
        )
        self.setUpContent()

    def test_rel(self):
        content = self.content
        viewlet = VCGEViewlet(content, self.request, None, None)
        viewlet.update()
        rel = viewlet.rel()
        self.assertEqual(rel, u'dc:subject foaf:primaryTopic')

    def test_skos(self):
        content = self.content
        viewlet = VCGEViewlet(content, self.request, None, None)
        viewlet.update()
        skos = viewlet.skos()
        self.assertEqual(len(skos), 1)
        term = skos[0]
        self.assertEqual(term.get('title'), u'Cultura')

    def test_skos_not_existent(self):
        """Testa o que acontece quando nao temos o Extender aplicado a
        um tipo de conteudo (neste caso o proprio portal).
        """
        portal = self.portal
        viewlet = VCGEViewlet(portal, self.request, None, None)
        viewlet.update()
        skos = viewlet.skos()
        self.assertEqual(len(skos), 0)
