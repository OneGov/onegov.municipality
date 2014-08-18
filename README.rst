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


Minimal Buildout
----------------

The following is the minimal buildout with which you'll get
onegov.municipality to run. Essentially, it's the minimal buildout from
http://bluedynamics.com/articles/jens/plone-4.3-latest-minimal-buildout,
with two lines added (as noted in the code's comments).

.. code:: bash

    [buildout]

    # the second extends line is onegov.municipality specific
    extends =
        http://dist.plone.org/release/4.3-latest/versions.cfg
        https://raw.githubusercontent.com/OneGov/onegov.municipality/master/release/latest.cfg

    find-links +=
        http://effbot.org/downloads/

    parts = instance

    [versions]
    zc.buildout >= 2.2.1
    setuptools >= 2.2

    [instance]
    recipe = plone.recipe.zope2instance
    http-address = 8080
    user = admin:admin

    # the third eggs line is onegov.municipality specific
    eggs =
        Plone
        Pillow
        onegov.municipality

Using this minimal buildout you can install onegov.municipality thusly:

1. Save the buildout above in buildout.cfg

2. Get bootstrap:

.. code:: bash

    curl https://raw.githubusercontent.com/OneGov/onegov.municipality/master/bootstrap.py > bootstrap.py
    curl 

3. Run bootstrap:

.. code:: bash

    python boostrap.py

4. Run buildout

.. code:: bash

    bin/buildout

5. Run the server

.. code:: bash

    bin/instance fg

6. Install onegov municipality on http://localhost:8080 using the user *admin*
with the password *admin*


Tests
-----

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
