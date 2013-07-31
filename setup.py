from setuptools import setup, find_packages

version = '1.0.dev0'

tests_require = [
    'plone.app.testing',
    ]


setup(name='onegov.municipality',
      version=version,
      long_description=open("README.rst").read() + "\n" + \
          open("docs/HISTORY.txt").read(),

      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],

      keywords='plone onegov municipality',
      author='Verein OneGov',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/OneGov/onegov.municipality',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['onegov'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'Plone',
        'ftw.contentpage',
        'ftw.inflator',
        'ftw.upgrade',
        'plonetheme.onegov',
        'setuptools',
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
