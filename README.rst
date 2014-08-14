onegov.municipality
===================

This is a Plone policy package, setting up a `OneGov Box`_ based
website for municipalities.


Releases
--------

The `OneGov Box`_ comes with a Known Good Set of packages which can be found
in the release folder of this repo. There's currently no stable release.

Stable releseas are versions without appendage like rc1 or dev. 1.0 or 1.0.1
for example.

Once a Known Good Set is released, it will not be changed anymore, so it is
safe to use that set for production.

The latest.cfg in the releases folder always contains the latest pinned
packages.


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

Heroku
------

This assumes that you signed up for a Heroku account and installed the Heroku Toolbelt:

.. code:: bash

  heroku create --buildpack git://github.com/niteoweb/heroku-buildpack-plone.git
  heroku config:add BUILDOUT_CFG=heroku.cfg
  git push heroku heroku:master


Links
-----

- Source: https://github.com/OneGov/onegov.municipality
- Issue tracker: https://github.com/OneGov/onegov.municipality/issues


Copyright
---------

This package is copyright by `Verein OneGov <http://www.onegov.ch/>`_.

``onegov.policy`` is licensed under GNU General Public License, version 2.


.. _OneGov Box: http://www.onegov.ch/
