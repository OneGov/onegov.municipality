from Products.CMFCore.utils import getToolByName
from onegov.municipality.testing import MUNICIPALITY_INTEGRATION_TESTING
from unittest2 import TestCase
import re
import tinycss


class TestFTIIcons(TestCase):

    layer = MUNICIPALITY_INTEGRATION_TESTING

    def test_ftis_with_webfonts_do_have_an_empty_icon_expression(self):
        webfont_types = self.get_portal_types_with_webfonts()
        wrong_types = {}

        for type_name, icon_expr in self.get_icon_expressions_foreach_fti().items():
            if not icon_expr:
                continue
            normalized_name = type_name.lower().replace(' ', '-')
            if normalized_name in webfont_types:
                wrong_types[type_name] = icon_expr

        self.assertEquals({}, wrong_types,
                          'FTIs, which have a webfont / sprite based styling in the '
                          'theme, should not have an "icon_expr".')

    def get_icon_expressions_foreach_fti(self):
        types_tool = getToolByName(self.layer['portal'], 'portal_types')
        result = {}
        for fti in types_tool.objectValues():
            result[fti.getId()] = fti.icon_expr
        return result

    def get_portal_types_with_webfonts(self):
        css = self.get_css()
        xpr = re.compile('\.contenttype-([A-Za-z_-]*):before')

        types = []
        for rule in css.rules:
            for selector in rule.selector.as_css().split(','):
                match = xpr.match(selector.strip())
                if match:
                    types.append(match.groups()[0])

        return types

    def get_css(self):
        parser = tinycss.make_parser()
        css_file = self.layer['portal'].restrictedTraverse(
            '++theme++plonetheme.onegov/sass/components/icons.scss').path
        return parser.parse_stylesheet_file(css_file)
