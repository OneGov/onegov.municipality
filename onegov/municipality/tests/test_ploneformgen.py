from Products.PloneFormGen.content.form import FormFolder
from ftw.contentpage.interfaces import ICategorizable
from onegov.municipality.testing import MUNICIPALITY_INTEGRATION_TESTING
from unittest2 import TestCase


class TestPloneFormGen(TestCase):

    layer = MUNICIPALITY_INTEGRATION_TESTING

    def test_formfolder_is_categorizable(self):
        self.assertTrue(
            ICategorizable.implementedBy(FormFolder),
            'PloneFormGen forms should support content page categorization.')
