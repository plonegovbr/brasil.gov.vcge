# -*- coding:utf-8 -*-
from brasil.gov.vcge import MessageFactory as _
from brasil.gov.vcge.dx.widget import SkosFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import alsoProvides


class IVCGE(model.Schema):
    ''' VCGE Behaviour
    '''

    # categorization fieldset
    model.fieldset(
        'categorization',
        fields=['skos'],
    )

    form.widget(skos=SkosFieldWidget)
    skos = schema.Tuple(
        title=_(u'VCGE'),
        description=_(u'vcge_desc'),
        required=False,
        value_type=schema.Choice(vocabulary='brasil.gov.vcge'),
    )

    form.order_after(skos='subjects')

    form.omitted('skos')
    form.no_omit(IEditForm, 'skos')
    form.no_omit(IAddForm, 'skos')


# Mark these interfaces as form field providers
alsoProvides(IVCGE, IFormFieldProvider)


class VCGE(object):

    def __init__(self, context):
        self.context = context

    def _get_skos(self):
        return self.context.skos

    def _set_skos(self, value):
        self.context.skos = value
    skos = property(_get_skos, _set_skos)
