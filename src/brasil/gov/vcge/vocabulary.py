# -*- coding:utf-8 -*-
from brasil.gov.vcge.utils import load_skos

from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class VCGEVocabulary(object):
    """ TODO
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = []
        termos = load_skos()
        items = termos.items()
        items = [SimpleTerm(key, key, value['title'])
                 for (key, value) in items]
        return SimpleVocabulary(items)

VCGEVocabularyFactory = VCGEVocabulary()
