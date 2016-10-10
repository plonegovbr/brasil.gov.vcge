# -*- coding: utf-8 -*-
from brasil.gov.vcge.browser.viewlets import VCGEViewlet
from brasil.gov.vcge.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.site.hooks import setSite

import unittest2 as unittest


class TestViewlet(unittest.TestCase):
    """Test viewlet implementation"""

    layer = INTEGRATION_TESTING

    def setUpUser(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)

    def setUpContent(self):
        token = 'http://vocab.e.gov.br/id/governo#cultura'
        portal = self.portal
        o = api.content.create(
            type='Document',
            container=portal,
            id='doc'
        )
        o.Schema().getField('skos').set(o, [token, ])
        self.content = o

    def setUp(self):
        portal = self.layer['portal']
        self.request = self.layer['app'].REQUEST
        setSite(portal)
        self.portal = portal
        self.setUpUser()
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
        ''' Testa o que acontece quando nao temos o Extender
            aplicado a um tipo de conteudo (neste caso o proprio portal)
        '''
        portal = self.portal
        viewlet = VCGEViewlet(portal, self.request, None, None)
        viewlet.update()
        skos = viewlet.skos()
        self.assertEqual(len(skos), 0)
