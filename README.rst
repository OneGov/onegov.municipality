onegov.municipality
===================

This is a Plone policy package, setting up a `OneGov Box`_ based
website for municipalities.


Development installation
------------------------

You can install onegov.municipality with buildout:

.. code:: bash

  git clone https://github.com/OneGov/onegov.municipality.git
  cd onegov.municipality
  python2.7 bootstrap.py
  bin/buildout -c development.cfg


Running Plone
-------------

.. code:: bash

  bin/instance fg


Tests
-----------------

.. image:: https://secure.travis-ci.org/OneGov/onegov.municipality.png
   :target: http://travis-ci.org/OneGov/onegov.municipality

Run tests with:

.. code:: bash

    bin/test


Links
-----

- Source: https://github.com/OneGov/onegov.municipality
- Issue tracker: https://github.com/OneGov/onegov.municipality/issues


Copyright
---------

This package is copyright by `Verein OneGov <http://www.onegov.ch/>`_.

``onegov.policy`` is licensed under GNU General Public License, version 2.


.. _OneGov Box: http://www.onegov.ch/
