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
        fields=['vcge'],
    )

    form.widget(vcge=SkosFieldWidget)
    vcge = schema.Tuple(
        title=_(u'VCGE'),
        description=_(u'vcge_desc'),
        required=False,
        value_type=schema.Choice(vocabulary='brasil.gov.vcge'),
    )

    form.order_after(vcge='subjects')

    form.omitted('vcge')
    form.no_omit(IEditForm, 'vcge')
    form.no_omit(IAddForm, 'vcge')


# Mark these interfaces as form field providers
alsoProvides(IVCGE, IFormFieldProvider)


class VCGE(object):

    def __init__(self, context):
        self.context = context

    def _get_vcge(self):
        return self.context.vcge

    def _set_vcge(self, value):
        self.context.vcge = value
    vcge = property(_get_vcge, _set_vcge)
