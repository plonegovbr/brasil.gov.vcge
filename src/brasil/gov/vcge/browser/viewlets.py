# -*- coding: utf-8 -*-
"""Modulo que implementa o(s) viewlet(s) do VCGE."""
from six.moves.urllib.parse import urlencode  # noqa: I001
from Acquisition import aq_base
from Acquisition import aq_inner
from plone.app.layout.viewlets import ViewletBase
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory


class VCGEViewlet(ViewletBase):
    """Viewlet adicionado a estrutura visual do portal."""
    # Indica qual o template sera usado por este viewlet
    index = ViewPageTemplateFile('templates/vcge.pt')

    def update(self):
        """Prepara/Atualiza os valores utilizados pelo Viewlet."""
        super(VCGEViewlet, self).update()
        ps = self.context.restrictedTraverse('@@plone_portal_state')
        self.nav_root_url = ps.navigation_root().absolute_url()

    def skos(self):
        """Retorna lista de itens selecionados neste conteudo."""
        context = aq_base(aq_inner(self.context))
        uris = []
        if safe_hasattr(context, 'skos'):
            uris = self.context.skos or []
        name = 'brasil.gov.vcge'
        util = queryUtility(IVocabularyFactory, name)
        vcge = util(self.context)
        skos = []
        for uri in uris:
            title = vcge.by_token[uri].title
            params = urlencode({'skos:list': uri})
            skos.append({'id': uri,
                         'title': title,
                         'url': '{0}/@@search?{1}'.format(
                             self.nav_root_url,
                             params,
                         )})
        return skos

    def rel(self):
        """Formata rel a ser utilizado no href de cada termo."""
        return u'dc:subject foaf:primaryTopic'


class VCGEHeadViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/vcge_head.pt')
