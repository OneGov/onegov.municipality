from ftw.lawgiver.tests.base import WorkflowTest
from onegov.municipality.testing import MUNICIPALITY_INTEGRATION_TESTING


class TestOneGovSimpleWorkflow(WorkflowTest):

    workflow_path = '../profiles/default/workflows/onegov-simple-workflow'
    layer = MUNICIPALITY_INTEGRATION_TESTING
