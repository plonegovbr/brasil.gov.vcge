Alterações
------------

2.0.3 (unreleased)
^^^^^^^^^^^^^^^^^^

- Nothing changed yet.


2.0.2 (2017-12-22)
^^^^^^^^^^^^^^^^^^

- Corrige ``UnicodeEncodeError`` ao buscar termos no vocabulário (fecha `#48 <https://github.com/plonegovbr/brasil.gov.vcge/issues/48>`_).
  [hvelarde]

- Adiciona suporte para Python 3 e dependencia com o future.
  [caduvieira, hvelarde]

- Remove suporte para Python 2.6 e Plone 4.2.
  [hvelarde]

- Remove dependencia no unittest2.
  [hvelarde]


2.0.1 (2017-10-31)
^^^^^^^^^^^^^^^^^^

- Remove dependência desnecessária no collective.z3cform.widgets.
  [hvelarde]


2.0.0 (2014-08-08)
^^^^^^^^^^^^^^^^^^

* Atualiza o VCGE para sua versão 2.0.2, substituindo o arquivo vcge.n3.
  [cfviotti]

* Corrige a namespace URI, e retira acentuação gráfica da id de Vigilância
  Sanitária do arquivo vcge.n3.
  [cfviotti]

* Atualiza os arquivos de testes do plugin para funcionarem com a nova
  versão do arquivo vcge.n3. Modificou-se o termo utilizado nos tokens
  para um que estivesse disponível nesta nova versão, no caso,
  o termo #Cultura. Atualizado também o número de termos do VCGE, de 1464
  para 114.
  [cfviotti]

Previous entries can be found in the HISTORY.rst file.
