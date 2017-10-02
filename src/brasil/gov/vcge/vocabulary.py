# -*- coding:utf-8 -*-
from brasil.gov.vcge.utils import load_skos
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class VCGEVocabulary(object):
    """Vocabulario Controlado do Governo Eletronico

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context

      >>> name = 'brasil.gov.vcge'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> terms = util(context)
      >>> terms
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(terms.by_token)
      1464

      >>> token = 'http://vocab.e.gov.br/2011/03/vcge#achados-perdidos'
      >>> doc = terms.by_token[token]
      >>> doc.title, doc.token, doc.value
      (u'Achados e perdidos', token, token)
    """

    def __call__(self, context):
        items = []
        termos = load_skos()
        items = termos.items()
        items = [SimpleTerm(key, key, value['title'])
                 for (key, value) in items]
        return SimpleVocabulary(items)

VCGEVocabularyFactory = VCGEVocabulary()
