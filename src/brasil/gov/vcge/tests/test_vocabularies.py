# -*- coding: utf-8 -*-

from brasil.gov.vcge.testing import INTEGRATION_TESTING
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class VocabulariesTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_vcge_vocabulary(self):
        name = 'brasil.gov.vcge'
        util = queryUtility(IVocabularyFactory, name)
        self.assertTrue(util is not None)
        vcge = util(self.portal)
        self.assertEqual(len(vcge), 1464)
        token = 'http://vocab.e.gov.br/2011/03/vcge#achados-perdidos'
        title = u'Achados e perdidos'
        term = vcge.by_token[token]
        self.assertEqual(term.title, title)
