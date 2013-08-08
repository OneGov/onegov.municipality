from ftw.subsite.portlets import teaserportlet
from plone.namedfile.file import NamedImage
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from zope.component import getMultiAdapter
from zope.component import getUtility
import os
from plone.uuid.interfaces import IUUID

SUBSITE_PORTLETS = [
    {'ftw.subsite.front1':
        [
            {'assignment': teaserportlet.Assignment,
             'id': 'privatpersonen',
             'teasertitle': u'Privatpersonen',
             'internal_target': 'private',
             'teaserdesc': u'Lorem ipsum Incididunt laboris est cupidatat eli',
             'imagename': 'municipal.jpeg'}
        ]},

    {'ftw.subsite.front2':
        [
            {'assignment': teaserportlet.Assignment,
             'id': 'unternehmen',
             'teasertitle': u'Unternehmen',
             'internal_target': 'unternehmen',
             'teaserdesc': u'Lorem ipsum Incididunt laboris est cupidatat eli',
             'imagename': 'municipal.jpeg'}
        ]},

    {'ftw.subsite.front3':
        [
            {'assignment': teaserportlet.Assignment,
             'id': 'gemeinde',
             'teasertitle': u'Gemeinde',
             'internal_target': 'gemeinde',
             'teaserdesc': u'Lorem ipsum Incididunt laboris est cupidatat eli',
             'imagename': 'municipal.jpeg'}
        ]},

    {'ftw.subsite.front4':
        [
            {'assignment': teaserportlet.Assignment,
             'id': 'politik',
             'teasertitle': u'Politik',
             'internal_target': 'politik',
             'teaserdesc': u'Lorem ipsum Incididunt laboris est cupidatat eli',
             'imagename': 'municipal.jpeg'}
        ]}
]


def setup_startpage(portal):

    for managers in SUBSITE_PORTLETS:
        for managername, portlets in managers.items():

            manager = getUtility(IPortletManager,
                                 name=managername, context=portal)
            assignments = getMultiAdapter((portal, manager),
                                          IPortletAssignmentMapping,
                                          context=portal)

            for portlet in portlets:
                id_ = portlet['id']

                relative_path = 'profiles/init-content/content_creation/images'
                image = open('%s/%s/%s' % (
                    os.path.split(__file__)[0],
                    relative_path,
                    portlet['imagename']), 'r')

                target = portal.unrestrictedTraverse(
                    portlet['internal_target'])
                target_uid = IUUID(target)

                if id_ not in assignments:
                    assignments[id_] = portlet['assignment'](
                        assignment_context_path='++contextportlets++%s' % (
                            managername),
                        teasertitle=portlet['teasertitle'],
                        internal_target=target_uid,
                        teaserdesc=portlet['teaserdesc'],
                        image=NamedImage(image,
                                         contentType='image/jpg',
                                         filename=u'teaser.jpg'))


def import_various(context):
    """Miscellanous steps import handle
    """
    portal = context.getSite()
    if context.readDataFile('onegov.municipality-init.txt') is not None:
        setup_startpage(portal)
