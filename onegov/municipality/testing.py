from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2
from zope.configuration import xmlconfig


class OneGovMunicipalityLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        z2.installProduct(app, 'ftw.contentpage')
        z2.installProduct(app, 'ftw.file')
        z2.installProduct(app, 'simplelayout.types.common')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'onegov.municipality:default')


MUNICIPALITY_FIXTURE = OneGovMunicipalityLayer()

MUNICIPALITY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MUNICIPALITY_FIXTURE, ),
    name="onegov.municipality:Integration")
