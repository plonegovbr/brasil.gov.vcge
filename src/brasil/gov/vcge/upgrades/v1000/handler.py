# -*- coding:utf-8 -*-
from brasil.gov.vcge.config import PROJECTNAME

import logging


logger = logging.getLogger(PROJECTNAME)


def stub(context):
    """Passo de atualizacao vazio."""
    logger.info('Instalacao inicial')
