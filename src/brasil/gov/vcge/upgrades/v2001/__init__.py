# -*- coding:utf-8 -*-
from brasil.gov.vcge.dx.interfaces import IVCGEDx
from brasil.gov.vcge.logger import logger
from plone import api

import csv
import os


INFO_URL = 'https://www.governoeletronico.gov.br/documentos-e-arquivos/VCGE_DEPARA_01.pdf'


class Migrator():
    """Context manager to handle term migration."""

    def __init__(self):
        path = os.path.dirname(__file__)
        self.filename = os.path.join(path, 'VCGE_DEPARA_01.csv')

    def __enter__(self):
        """Read equivalences file and create dictionary."""
        self.equivalences = {}
        logger.debug('Reading equivalence file')
        with open(self.filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                new = row['termo_vcge_2B']
                if new:
                    old = row['termo_vcge_1']
                    self.equivalences[old] = new

    def __exit__(self, *args):
        pass  # update the catalog?

    def migrate(self, obj):
        """Migrate existing terms on objects."""
        if obj is None:
            return  # invalid object

        if not obj.skos:
            return  # nothing to do (empty or None)

        new = ()
        # ignore terms with no equivalence
        for term in obj.skos:
            if term in self.equivalences:
                new += self.equivalences[term]
        obj.skos = new


def term_migration(context):
    """Migrate terms from VCGE 1 to 2B."""
    msg = 'Some terms of VCGE 1 will be ignored. For more information see: '
    logger.warning(msg + INFO_URL)
    with Migrator() as migrator:
        results = api.content.find(object_provides=IVCGEDx.__identifier__)
        logger.info('{0} objects will be processed'.format(len(results)))
        for brain in results:
            try:
                obj = brain.getObject()
            except (AttributeError, KeyError):
                continue  # the object referenced is invalid
            migrator.migrate(obj)

    logger.info('VCGE terms migrated from 1 to 2B')
