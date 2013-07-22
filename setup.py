# -*- coding:utf-8 -*-

import os
from setuptools import setup, find_packages

version = '1.0a1'
long_description = (open("README.txt").read() + "\n" +
                    open(os.path.join("docs", "INSTALL.txt")).read() + "\n" +
                    open(os.path.join("docs", "CREDITS.txt")).read() + "\n" +
                    open(os.path.join("docs", "HISTORY.txt")).read())


description = u'Brasil.gov.br: Vocabulário Controlado do Governo Eletrônico'

setup(name='brasil.gov.vcge',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
          "Topic :: Software Development :: Libraries :: Python Modules"],
      keywords='brasil.gov.br vcge plone plonegovbr vocabularios',
      author='PloneGov.Br',
      author_email='gov@plone.org.br',
      url='http://www.plone.org.br/gov/',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['brasil', 'brasil.gov'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'raptus.autocompletewidget',
                        'rdflib'],
      extras_require={
          'archetypes': [
              'archetypes.schemaextender',
              'Products.ATContentTypes',
              'Products.Archetypes',
          ],
          'dexterity': [
              'collective.z3cform.widgets',
              'plone.app.dexterity [grok]',
              'plone.autoform',
              'plone.behavior',
              'plone.indexer',
          ],
          'develop': [
              'Sphinx',
              'manuel',
              'pep8',
              'setuptools-flakes',
          ],
          'test': [
              'interlude',
              'plone.app.testing'
          ]},
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
