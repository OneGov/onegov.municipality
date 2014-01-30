#
# Script to migrate existing onegov boxish sites.
#
import transaction

from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.component.hooks import setSite

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping


def get_plone_sites(root):

    sites = []
    for id, item in root.items():
        if not IPloneSiteRoot.providedBy(item):
            continue

        sites.append(item)
        sites.extend(get_plone_sites(item))

    return sites


def get_installed_products(site):
    installer = getToolByName(site, 'portal_quickinstaller')
    return [p['title'] for p in installer.listInstalledProducts()]


def get_portlet_mapping(site, column):
    column = getUtility(IPortletManager, name=column, context=site)
    return getMultiAdapter((site, column,), IPortletAssignmentMapping)


def remove_old_event_portlets(site):
    """ Sites with existing AT event portlets need to have them removed,
    unless plone.app.event is installed, in which case this is taken care of.

    """
    if 'plone.app.event' in get_installed_products(site):
        return

    for column in (u'plone.leftcolumn', u'plone.rightcolumn'):
        mapping = get_portlet_mapping(site, column)

        for id, assignment in mapping.items():
            if 'plone.app.portlets.portlets.events' in str(type(assignment)):

                'removing event portlet'
                del mapping[id]


def install_onegov_theme(site):
    if 'plonetheme.onegov' in get_installed_products(site):
        return

    print 'installing onegov theme'

    setup = getToolByName(site, 'portal_setup')
    setup.runAllImportStepsFromProfile(
        'profile-izug.basetheme:seantis_uninstall'
    )

    installer = getToolByName(site, 'portal_quickinstaller')
    installer.installProducts(['plonetheme.onegov'])


def uninstall_izug_basetheme(site):
    if 'izug.basetheme' not in get_installed_products(site):
        return

    print 'uninstalling izug.basetheme'

    installer = getToolByName(site, 'portal_quickinstaller')
    installer.uninstallProducts(['izug.basetheme'])


def disable_custom_css(site):
    skins = getToolByName(site, 'portal_skins')
    if not 'custom' in skins:
        return

    if not 'ploneCustom.css' in skins['custom']:
        return

    try:
        existing_data = skins['custom']['ploneCustom.css'].data
    except AttributeError:
        return

    if '@media DISABLED' in existing_data:
        return

    print 'removing custom css'

    disabled = '@media DISABLED {\n%s\n}' % existing_data
    skins['custom']['ploneCustom.css'].update_data(disabled)


def hide_directory_items_in_navigation(site):
    types_by_package = {
        'seantis.dir.contacts': ['seantis.dir.contacts.item'],
        'Seantis Dir Events': ['seantis.dir.events.item'],
        'seantis.dir.council': ['seantis.dir.council.item']
    }

    properties = getToolByName(site, 'portal_properties')
    blacklist = properties.navtree_properties.metaTypesNotToList

    installed = get_installed_products(site)

    for package, types in types_by_package.items():
        if package in installed:
            for t in types:
                if t not in blacklist:
                    print 'hiding {} in navigation'.format(t)
                    properties.navtree_properties._updateProperty(
                        'metaTypesNotToList', blacklist + (t, )
                    )


def main(app):
    steps = [
        remove_old_event_portlets,
        install_onegov_theme,
        uninstall_izug_basetheme,
        disable_custom_css,
        hide_directory_items_in_navigation,
    ]

    for site in get_plone_sites(root=app):
        print 'migrating {}'.format(site.id)
        setSite(site)
        for step in steps:
            step(site)

    transaction.commit()

# Ensures that grok won't execute the script
if 'app' in locals():
    if raw_input("""
        This migration script is meant for existing plone sites run by
        Seantis for the Canton of Zug. If you really want to continue,
        type 'i know': """) == 'i know':
        print ''
        main(locals()['app'])
