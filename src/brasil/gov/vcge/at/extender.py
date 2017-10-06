# -*- coding:utf-8 -*-
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from brasil.gov.vcge import MessageFactory as _
from brasil.gov.vcge.interfaces import IVCGEInstalado
from Products.Archetypes import public as atapi
from Products.Archetypes.interfaces import IBaseContent
from raptus.autocompletewidget.widget import AutocompleteMultiSelectionWidget
from zope.component import adapter
from zope.interface import implementer


AcMSW = AutocompleteMultiSelectionWidget


class ExtensionLinesField(ExtensionField, atapi.LinesField):
    """ Usamos um campo tipo Linhas (LinesField) como base
        e o extendemos.
    """


# Este adaptador sera aplicado a todos os tipos baseados em Archetypes
@adapter(IBaseContent)
# We use both orderable and browser layer aware sensitive properties
@implementer(IBrowserLayerAwareExtender)
class VCGEExtender(object):
    """ Adaptador que extende os tipos de conteudo base do Plone
        com o campo skos (representando o VCGE)
    """

    layer = IVCGEInstalado

    fields = [
        ExtensionLinesField('skos',
                            schemata='categorization',
                            vocabulary_factory='brasil.gov.vcge',
                            enforceVocabulary=True,
                            widget=AcMSW(label=_(u'VCGE'),
                                         description=_(u'vcge_desc'),))
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        """
        @return: Lista de campos adicionados ao conteudo
        """
        return self.fields
