# -*- coding:utf-8 -*-
from brasil.gov.vcge.contentrules.condition import VCGECondition
from brasil.gov.vcge.contentrules.condition import VCGEEditForm
from brasil.gov.vcge.testing import INTEGRATION_TESTING
from plone import api
from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleCondition
from Products.CMFCore.PortalContent import PortalContent
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.interfaces import IObjectEvent
from zope.interface import implementer

import unittest


@implementer(IObjectEvent)
class DummyEvent(object):

    def __init__(self, object):
        self.object = object


class TestVCGECondition(unittest.TestCase):

    layer = INTEGRATION_TESTING

    term = 'http://vocab.e.gov.br/id/governo#cultura'

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.folder = api.content.create(
            type='Folder',
            container=self.portal,
            id='folder',
        )
        self.folder.skos = [self.term]

        self.sub_folder = api.content.create(
            type='Folder',
            container=self.folder,
            id='sub_folder',
        )
        self.sub_folder.skos = ['http://vocab.e.gov.br/2011/03/vcge#governo']
        o = PortalContent('cmf', 'CMF Content', '', '', '')
        self.folder._setObject('cmf', o, suppress_events=True)

    def test_registered(self):
        element = getUtility(IRuleCondition,
                             name='brasil.gov.vcge.conditions.VCGE')
        self.assertEqual('brasil.gov.vcge.conditions.VCGE', element.addview)
        self.assertEqual('edit', element.editview)
        self.assertEqual(None, element.for_)
        self.assertEqual(IObjectEvent, element.event)

    def test_invoke_add_view(self):
        element = getUtility(IRuleCondition,
                             name='brasil.gov.vcge.conditions.VCGE')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST),
                                 name='+condition')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        addview.createAndAdd(data={'skos': [self.term]})

        e = rule.conditions[0]
        self.assertTrue(isinstance(e, VCGECondition))
        self.assertEqual([self.term], e.skos)

    def test_invoke_edit_view(self):
        element = getUtility(IRuleCondition,
                             name='brasil.gov.vcge.conditions.VCGE')
        e = VCGECondition()
        editview = getMultiAdapter((e, self.folder.REQUEST),
                                   name=element.editview)
        self.assertTrue(isinstance(editview, VCGEEditForm))

    def test_summary_empty_vcge(self):
        e = VCGECondition()
        self.assertEqual(e.summary, u'Nenhum termo selecionado')

    def test_summary_with_vcge(self):
        from plone.app.contentrules import PloneMessageFactory as _
        e = VCGECondition()
        e.skos = [self.term]
        msg = _(u'VCGE contém ${skos}',
                mapping=dict(skos=' or '.join(e.skos)))
        self.assertEqual(e.summary, msg)

    def test_execute(self):
        e = VCGECondition()
        e.skos = [self.term]

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)
        self.assertEqual(True, ex())

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEqual(False, ex())

    def test_execute_empty(self):
        e = VCGECondition()
        e.skos = []

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)
        self.assertEqual(False, ex())

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEqual(False, ex())

        # Empty VCGE field
        self.sub_folder.skos = []
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEqual(True, ex())

    def test_execute_object_without_vcge(self):
        e = VCGECondition()
        e.skos = [self.term]

        ex = getMultiAdapter((self.folder, e,
                              DummyEvent(self.folder['cmf'])),
                             IExecutable)
        self.assertEqual(False, ex())
