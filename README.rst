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
  ln -s development.cfg buildout.cfg
  python2.7 bootstrap.py
  bin/buildout


Running Plone
-------------

.. code:: bash

  bin/instance fg


Running the tests
-----------------

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
