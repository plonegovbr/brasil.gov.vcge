# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.0.1.dev0'
description = u'Brasil.gov.br: Vocabulário Controlado do Governo Eletrônico'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(name='brasil.gov.vcge',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Plone',
          'Framework :: Plone :: 4.0',
          'Framework :: Plone :: 4.1',
          'Framework :: Plone :: 4.2',
          'Framework :: Plone :: 4.3',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='brasil.gov.br vcge plone plonegovbr vocabularios',
      author='PloneGov.Br',
      author_email='gov@plone.org.br',
      url='http://www.plone.org.br/gov/',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['brasil', 'brasil.gov'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Plone >=4.0',
          'raptus.autocompletewidget',
          'rdflib',
          'setuptools',
          'zope.component',
          'z3c.form',
          'zope.interface',
      ],
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
              'Products.CMFPlone',
          ],
          'develop': [
              'Sphinx',
              'manuel',
              'pep8',
              'setuptools-flakes',
          ],
          'test': [
              'interlude',
              'plone.app.testing',
              'unittest2',
          ]},
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
