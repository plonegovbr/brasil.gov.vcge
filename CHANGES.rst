Alterações
------------

2.0.1 (unreleased)
^^^^^^^^^^^^^^^^^^

- Nothing changed yet.


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

1.0.3 (unreleased)
^^^^^^^^^^^^^^^^^^

* Adiciona ação de regra de conteúdo para aplicação de termos
  VCGE a conteúdos
  [ericof]

* Adiciona condição de regra de conteúdo baseada nos termos
  VCGE
  [ericof]

1.0.2 (2014-02-28)
^^^^^^^^^^^^^^^^^^

* Renomeia pacote para .gov.br.
  [ericof]

* Inclui collective.z3cform.widgets como requerimento.
  [dbarbato]

* Oculta upgrade steps.
  [dbarbato]


1.0.1 (2013-11-18)
^^^^^^^^^^^^^^^^^^^

* Removido suporte as versoes 4.0 e 4.1 do Plone
  [ericof]

* Suporte a filtros em Colecoes do Plone (plone.app.collection)
  [ericof]

* Refatoracao dos upgrade steps
  [ericof]

* Melhor suporte a testes e a coverage
  [hvelarde]


1.0 (2013-10-29)
^^^^^^^^^^^^^^^^^^^

* Adicionado nome ao extender do Archetypes
  [lepri]


1.0rc1 (2013-08-26)
^^^^^^^^^^^^^^^^^^^^^

* Alterado id categorias do vcge para que ele não entre em conflito com o
  id do collective.nitf, dando erro de validação w3c.
  [rodfersou]
* Altera o mecanismo de busca de termos. Privilegiamos os termos
  com tamanho menor (Cultura ao invés de Escultura)
  [ericof]

* Corrige problema com widget quando não existem valores
  para o atributo skos
  [ericof]


1.0a1 (2013-07-22)
^^^^^^^^^^^^^^^^^^

* Versão inicial do pacote
  [ericof]
