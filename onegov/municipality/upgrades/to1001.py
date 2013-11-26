from ftw.upgrade import UpgradeStep


class UpdateWorkflow(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-onegov.municipality.upgrades:1001')

        self.update_workflow_security(['izug_workflow', 'izug_zupo_workflow'],
                                      reindex_security=False)
