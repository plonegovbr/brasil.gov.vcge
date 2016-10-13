***************************************************************
.gov.br: Vocabulário Controlado do Governo Eletrônico
***************************************************************

.. contents:: Conteúdo
   :depth: 2

Introdução
-----------

Este pacote provê a integração do Vocabulário Controlado do Governo Eletrônico
 (VCGE) para uso em sites Plone do Governo da República Federativa do Brasil.

Este pacote adiciona ao editor de conteúdos do Plone a opção de classificá-los
em categorias de assuntos predefinidos, conhecidos como like `vocabulários
controlados <http://en.wikipedia.org/wiki/Controlled_vocabulary>`_. O produto
cria, para cada assunto, uma tag `RDFa <http://pt.wikipedia.org/wiki/RDFa>`_
no HTML renderizado pelo Plone. Além disso, o produto possibilita buscar por
todos os conteúdos classificados em um assunto específico do vocabulário. O
funcionamento é semelhante ao sistema de etiquetas(tags), e ambos se
complementam em um sistema mais poderoso de classificação e recuperação de
informação.

Os conteúdos classificados com este produto, e publicados na web, se juntam a
outras iniciativas semelhantes e constituem um enorme repositório enriquecido
com metadados, criando possibilidades diversas para construção de motores de
indexação e recuperação de informações.

Para visualizar a estrutura `poli-hierárquica
<http://eurovoc.europa.eu/drupal/?q=pt/node/924>`_ de assuntos do VCGE acesse
o `repositório do e-VoG <http://vocab.e.gov.br/2011/03/vcge>`_.

Para saber mais acesse `Vocabulário Controlado do Governo Eletrônico (VCGE)
<http://www.governoeletronico.gov.br/acoes-e-projetos/e-ping-padroes-de-
interoperabilidade/vcge>`_.

Este produto utiliza um arquivo `SKOS
<http://en.wikipedia.org/wiki/Simple_Knowledge_Organization_System>`_, padrão
W3C para representar vocabulários controlados, dentre outras estruturas de
classificação.

Versionamento
---------------------

As versões 1.x deste pacote se referem ao VCGE 1.0

As versões 2.x deste pacote se referem ao VCGE 2.0.

Ainda não existe um caminho de migração de termos do VCGE 1.0 para o VCGE 2.0, portanto utilize o VCGE 2.0 apenas em **novos** projetos.

Estado deste pacote
---------------------

O **brasil.gov.vcge** tem testes automatizados e, a cada alteração em seu
código os testes são executados pelo serviço Travis. 

O estado atual dos testes pode ser visto na imagem a seguir:

.. image:: https://secure.travis-ci.org/plonegovbr/brasil.gov.vcge.png?branch=master
    :target: http://travis-ci.org/plonegovbr/brasil.gov.vcge

.. image:: https://coveralls.io/repos/plonegovbr/brasil.gov.vcge/badge.png?branch=master
    :target: https://coveralls.io/r/plonegovbr/brasil.gov.vcge

Instalação
------------

Para habilitar a instalação deste produto em um ambiente que utilize o
buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e
   adicionar o pacote ``brasil.gov.vcge`` à lista de eggs da instalação::

        [buildout]
        ...
        eggs =
            brasil.gov.vcge

2. Após alterar o arquivo de configuração é necessário executar
   ''bin/buildout'', que atualizará sua instalação.

3. Reinicie o Plone

4. Acesse o painel de controle e instale o produto
**.gov.br: Vocabulário Controlado do Governo Eletrônico**.

Rodando o buildout de uma tag antiga do pacote
----------------------------------------------

Para atender ao relato de ter vários jobs de integração contínua em pacotes brasil.gov.* (ver https://github.com/plonegovbr/portalpadrao.release/issues/11), no fim da seção extends do buildout.cfg de todos os pacotes brasil.gov.* temos a seguinte linha:

.. code-block:: cfg

    https://raw.githubusercontent.com/plonegovbr/portal.buildout/master/buildout.d/versions.cfg

Hoje, esse arquivo contém sempre as versões pinadas de um release a ser lançado. Por esse motivo, quando é feito o checkout de uma tag mais antiga provavelmente você não conseguirá rodar o buildout. Dessa forma, após fazer o checkout de uma tag antiga, recomendamos que adicione, na última linha do extends, o arquivo de versões do IDG compatível com aquela tag, presente no repositório https://github.com/plonegovbr/portalpadrao.release/.

Exemplo: você clonou o repositório do brasil.gov.portal na sua máquina, e deu checkout na tag 1.0.5. Ao editar o buildout.cfg, ficaria dessa forma, já com a última linha adicionada:

.. code-block:: cfg

    extends =
        https://raw.github.com/collective/buildout.plonetest/master/test-4.3.x.cfg
        https://raw.github.com/collective/buildout.plonetest/master/qa.cfg
        http://downloads.plone.org.br/release/1.0.4/versions.cfg
        https://raw.githubusercontent.com/plonegovbr/portal.buildout/master/buildout.d/versions.cfg
        https://raw.githubusercontent.com/plone/plone.app.robotframework/master/versions.cfg
        https://raw.githubusercontent.com/plonegovbr/portalpadrao.release/master/1.0.5/versions.cfg
        
Para saber qual arquivo de versões é compatível, no caso do brasil.gov.portal, é simples pois é a mesma versão (no máximo um bug fix, por exemplo, brasil.gov.portal é 1.1.3 e o arquivo de versão é 1.1.3.1). Para os demais pacotes, recomendamos comparar a data da tag do pacote e a data nos changelog entre uma versão e outra para adivinhar a versão compatível.
