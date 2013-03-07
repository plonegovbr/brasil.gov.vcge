# -*- coding: utf-8 -*-
from brasil.gov.vcge.config import PROJECTNAME

import logging


logger = logging.getLogger(PROJECTNAME)


def from0(context):
    ''' Passo de atualizacao para versao 1000
    '''
    logger.info('Instalacao inicial')
