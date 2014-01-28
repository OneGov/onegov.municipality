from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2


class OneGovMunicipalityLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import onegov.municipality
        self.loadZCML(package=onegov.municipality)

        import collective.deletepermission
        self.loadZCML(package=collective.deletepermission)

        import plone.app.iterate
        self.loadZCML(package=plone.app.iterate)

        z2.installProduct(app, 'Products.DateRecurringIndex')
        z2.installProduct(app, 'ftw.contentpage')
        z2.installProduct(app, 'ftw.file')
        z2.installProduct(app, 'ftw.subsite')
        z2.installProduct(app, 'simplelayout.types.common')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'onegov.municipality:default')


MUNICIPALITY_FIXTURE = OneGovMunicipalityLayer()

MUNICIPALITY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MUNICIPALITY_FIXTURE, ),
    name="onegov.municipality:Integration")
