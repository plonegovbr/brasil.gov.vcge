# -*- coding: utf-8 -*-
from brasil.gov.vcge.browser.viewlets import VCGEViewlet
from brasil.gov.vcge.testing import INTEGRATION_TESTING
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
        oId = portal.invokeFactory('Document', 'doc')
        o = portal[oId]
        o.Schema().getField('vcge').set(o, [token, ])
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
