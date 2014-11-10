# -*- coding:utf-8 -*-
from Acquisition import aq_inner
from OFS.SimpleItem import SimpleItem
from brasil.gov.vcge import _ as _
from brasil.gov.vcge.contentrules import utils
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from zope.component import adapts
from zope.formlib import form
from zope.interface import Interface
from zope.interface import implements
from zope.schema import Choice
from zope.schema import Set

VOCAB = 'brasil.gov.vcge'

FORM_NAME = _(u"Configure the condition")

FORM_DESC = _(u'A VGCE condition performs a content rule only if '
              u'one of the selected terms is present. If no term is selected, '
              u'the rule will be implemented only in content without '
              u'VCGE terms applied.')


class IVCGECondition(Interface):
    """ Interface utilizada para descrever os elementos configuraveis
        desta condicao.
    """

    skos = Set(title=_(u'VCGE'),
               description=_(u'Terms to be searched. Leave blank '
                             u'to select content with no VCGE term applied.'),
               required=False,
               value_type=Choice(vocabulary=VOCAB))


class VCGECondition(SimpleItem):
    """ A implementacao persistente para a condicao VCGE
    """
    implements(IVCGECondition, IRuleElementData)

    skos = []
    element = "brasil.gov.vcge.conditions.VCGE"

    @property
    def summary(self):
        skos = self.skos
        if not skos:
            msg = _(u"No terms selected")
        else:
            msg = _(u"VCGE contains ${skos}",
                    mapping=dict(skos=" or ".join(skos)))
        return msg


class VCGEConditionExecutor(object):
    """ O executor para esta condicao.
        Este codigo esta registrado como adaptador no configure.zcml
    """
    implements(IExecutable)
    adapts(Interface, IVCGECondition, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        expected = self.element.skos
        obj = aq_inner(self.event.object)

        if not (utils.vcge_available(obj)):
            return False

        skos = utils.vcge_for_object(obj)
        if not expected:
            return not (expected or skos)
        intersection = set(expected).intersection(skos)
        return intersection and True or False


class VCGEAddForm(AddForm):
    """ Formulario de adicao para condicoes
        de VCGE
    """
    form_fields = form.FormFields(IVCGECondition)
    label = _(u'Add VCGE condition')
    description = FORM_DESC
    form_name = FORM_NAME

    def create(self, data):
        c = VCGECondition()
        form.applyChanges(c, self.form_fields, data)
        return c


class VCGEEditForm(EditForm):
    """ Formulario de edicao para condicoes
        de VCGE
    """
    form_fields = form.FormFields(IVCGECondition)
    label = _(u"Edit condition VCGE")
    description = FORM_DESC
    form_name = FORM_NAME
