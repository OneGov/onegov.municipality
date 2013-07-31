from Products.CMFCore.utils import getToolByName
from ftw.upgrade.exceptions import CyclicDependencies
from ftw.upgrade.utils import topological_sort
from onegov.municipality.testing import MUNICIPALITY_INTEGRATION_TESTING
from unittest2 import TestCase
from xml.dom.minidom import parse
import os.path


MIXIN_DEPENDENCIES = {}


def get_sorted_profile_ids(portal_setup, mixin_dependencies):
    """Returns a sorted list of profile ids (without profile- prefix).
    The sorting is done by resolving the dependencies and performing
    a topological graph sort.
    If there are circular dependencies a CyclicDependencies exception
    is thrown.
    """
    profile_ids = []
    dependencies = []

    for profile in portal_setup.listProfileInfo():
        profile_ids.append(profile['id'])

    for profile in portal_setup.listProfileInfo():
        if not profile.get('dependencies'):
            continue

        profile_dependencies = list(profile.get('dependencies') or [])
        if profile.get('id') in mixin_dependencies:
            profile_dependencies.extend(mixin_dependencies[profile['id']])

        for dependency in profile_dependencies:
            if dependency.startswith('profile-'):
                dependency = dependency.split('profile-', 1)[1]
            else:
                continue

            if dependency not in profile_ids:
                continue
            dependencies.append((profile['id'], dependency))

    order = topological_sort(profile_ids, dependencies)

    if order is None:
        raise CyclicDependencies(dependencies)
    else:
        return list(reversed(order))


class TestDependencyOrder(TestCase):
    """It is important that the dependency order of the generic setup
    ``default`` profile is correct.
    """

    layer = MUNICIPALITY_INTEGRATION_TESTING

    def test_default_profile_dependencies_are_ordered_correctly(self):
        self.assert_profile_dependencies_are_ordered_correctly('default')

    def test_init_content_profile_dependencies_are_ordered_correctly(self):
        self.assert_profile_dependencies_are_ordered_correctly('init-content')

    def get_sorted_profile_ids(self):
        portal = self.layer['portal']
        setup_tool = getToolByName(portal, 'portal_setup')
        return get_sorted_profile_ids(setup_tool, MIXIN_DEPENDENCIES)

    def get_default_profile_dependencies(self, dirname):
        path = os.path.join(os.path.dirname(__file__),
                            '..', 'profiles', dirname, 'metadata.xml')
        doc = parse(path)
        profiles = []

        for node in doc.getElementsByTagName('dependency'):
            profile = ''.join([item.data for item in node.childNodes
                               if item.nodeType == item.TEXT_NODE])
            assert profile.startswith('profile-'), \
                'unexpected dependency %s' % profile
            profile = profile[len('profile-'):]
            profiles.append(profile)

        return profiles

    def assert_profile_dependencies_are_ordered_correctly(self, profilename):
        self.maxDiff = None

        all_profileids_topological = self.get_sorted_profile_ids()
        needed_profile_ids = self.get_default_profile_dependencies(profilename)

        needed_sorted = sorted(
            needed_profile_ids[:],
            key=lambda name: all_profileids_topological.index(name))

        try:
            self.assertEquals(
                needed_profile_ids, needed_sorted,
                ('Generic setup "%s" profile dependencies are not in'
                 ' topological order') % profilename)

        except AssertionError:
            print ''
            print '-' * 7, 'expected order', '-' * 7
            print '    <dependencies>'

            for name in needed_sorted:
                print '        <dependency>profile-%s</dependency>' % name

            print '    </dependencies>'
            print '-' * 30
            raise
