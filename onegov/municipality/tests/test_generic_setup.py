from Products.CMFCore.utils import getToolByName
from onegov.municipality.testing import MUNICIPALITY_INTEGRATION_TESTING
from unittest2 import TestCase


class TestIntranetInstallation(TestCase):

    layer = MUNICIPALITY_INTEGRATION_TESTING

    def test_intranet_profile_installed(self):
        portal = self.layer['portal']
        portal_setup = getToolByName(portal, 'portal_setup')

        version = portal_setup.getLastVersionForProfile(
            'onegov.municipality:default')
        self.assertNotEqual(version, None)
        self.assertNotEqual(version, 'unknown')
