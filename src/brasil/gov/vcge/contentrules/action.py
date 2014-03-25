# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from brasil.gov.vcge.contentrules import utils
from OFS.SimpleItem import SimpleItem
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements
from zope.interface import Interface
from zope.schema import Bool
from zope.schema import Choice
from zope.schema import Set


VOCAB = 'brasil.gov.vcge'

FORM_NAME = _(u"Configurar a ação")

FORM_DESC = _(u'Uma ação que aplica termos do VGCE a um conteúdo')


class IVCGEAction(Interface):
    """ Interface utilizada para descrever os elementos configuraveis
        desta ação.
    """

    same_as_parent = Bool(title=_(u"Utilizar os termos da pasta"),
                          description=_(u"Selecione esta opção para que os "
                                        u"termos VCGE sejam herdados da "
                                        u"pasta que abriga o conteúdo. "
                                        u"Selecionar esta opção ignora "
                                        u"os termos do campo a seguir."))

    skos = Set(title=_(u'VCGE'),
               description=_(u'Termos a serem aplicados ao conteúdo.'),
               required=False,
               value_type=Choice(vocabulary=VOCAB))


class VCGEAction(SimpleItem):
    """ A implementacao persistente para a acao VCGE
    """
    implements(IVCGEAction, IRuleElementData)

    element = 'brasil.gov.vcge.actions.VCGE'
    same_as_parent = False
    skos = []

    @property
    def summary(self):
        same_as_parent = self.same_as_parent
        skos = self.skos
        if same_as_parent:
            msg = _(u"Aplica termos da pasta no conteúdo.")
        else:
            msg = _(u"Aplica os termos ${skos}",
                    mapping=dict(skos=", ".join(skos)))
        return msg


class VCGEActionExecutor(object):
    """ O executor para esta acao.
        Este codigo esta registrado como adaptador no configure.zcml
    """
    implements(IExecutable)
    adapts(Interface, IVCGEAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        '''  Apply selected layout to a content item
        '''
        obj = self.event.object
        same_as_parent = self.element.same_as_parent
        skos = self.element.skos
        if not (utils.vcge_available(obj)):
            return False
        if same_as_parent:
            parent = aq_parent(obj)
            if not (utils.vcge_available(parent)):
                return False
            skos = utils.vcge_for_object(parent)
        return utils.set_vcge(obj, skos)


class VCGEAddForm(AddForm):
    """ Formulario de adicao para acao VCGE
    """
    form_fields = form.FormFields(IVCGEAction)
    label = _(u"Adicionar ação VCGE na regra de conteúdo")
    description = FORM_DESC
    form_name = FORM_NAME

    def create(self, data):
        a = VCGEAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class VCGEEditForm(EditForm):
    """ Formulario de adicao para edicao VCGE
    """
    form_fields = form.FormFields(IVCGEAction)
    label = _(u"Editar ação VCGE na regra de conteúdo")
    description = FORM_DESC
    form_name = FORM_NAME
