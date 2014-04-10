from plone import api
from ftw.upgrade import UpgradeStep


class UpdateWorkflow(UpgradeStep):

    def __call__(self):
        setup = api.portal.get_tool('portal_setup')
        setup.runImportStepFromProfile(
            'profile-onegov.municipality:default', 'typeinfo'
        )
