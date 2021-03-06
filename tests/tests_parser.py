"""
SkCode tag parser test code.
"""

import string
import unittest

from skcode.parser import (
    WHITESPACE_CHARSET,
    IDENTIFIER_CHARSET,
    skip_whitespaces,
    get_identifier,
    parse_tag
)


class TagParserTestCase(unittest.TestCase):
    """ Tests case for the tag parser module. """

    def test_charsets_constants(self):
        """ Test if the charset constants are valid. """
        self.assertEqual(frozenset(string.whitespace), WHITESPACE_CHARSET)
        self.assertEqual(frozenset(string.ascii_letters + string.digits + '_*'), IDENTIFIER_CHARSET)

    def test_skip_whitespaces(self):
        """ Test the ``skip_whitespaces`` method with some whitespaces """
        offset = skip_whitespaces('   abcd   ', 0)
        self.assertEqual(offset, 3)

    def test_skip_whitespaces_without_spaces(self):
        """ Test the ``skip_whitespaces`` method without any whitespaces """
        offset = skip_whitespaces('abcd   ', 0)
        self.assertEqual(offset, 0)

    def test_skip_whitespaces_with_whitespaces_only(self):
        """
        Test if the ``skip_whitespaces`` method raise a ``IndexError`` if the string end with whitespaces.
        """
        with self.assertRaises(IndexError):
            skip_whitespaces("  ", 0)

    def test_get_identifier_with_valid_name(self):
        """
        Test if the ``get_identifier`` method with a valid identifier string.
        """
        identifier, offset = get_identifier('_abcdefghijklmnopqrstuvwxyz'
                                            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                                            '0123456789 ', 0)
        self.assertEqual('_abcdefghijklmnopqrstuvwxyz'
                         'abcdefghijklmnopqrstuvwxyz'
                         '0123456789', identifier)
        self.assertEqual(offset, 63)

    def test_get_identifier_with_whitespaces(self):
        """
        Test if the ``get_identifier`` method with some whitespaces.
        """
        identifier, offset = get_identifier('_abcdefghijklmnopqrstuvwxyz '
                                            'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
                                            '0123456789 ', 0)
        self.assertEqual('_abcdefghijklmnopqrstuvwxyz', identifier)
        self.assertEqual(offset, 27)

    def test_get_identifier_with_uppercase(self):
        """
        Test if the ``get_identifier`` method with some uppercase char.
        """
        identifier, offset = get_identifier('_ABCDEFGHIJKlmnopqrstuvwxyz ', 0)
        self.assertEqual('_abcdefghijklmnopqrstuvwxyz', identifier)
        self.assertEqual(offset, 27)

    def test_get_identifier_no_ending_whitespace(self):
        """
        Test if the ``get_identifier`` method with no ending whitespaces.
        """
        with self.assertRaises(IndexError):
            get_identifier('test', 0)

    # --- Functional tests
    PASS_TESTS = (
        # Test simple opening tag with extra whitespaces
        ('[test]', ('test', False, False, {}, 6)),
        ('[ test]', ('test', False, False, {}, 7)),
        ('[test ]', ('test', False, False, {}, 7)),
        ('[ test ]', ('test', False, False, {}, 8)),

        # Test tag name normalization
        ('[TesT]', ('test', False, False, {}, 6)),

        # Test attribute name normalization
        ('[test kEy=value]', ('test', False, False, {'key': 'value'}, 16)),

        # Test standalone attribute
        ('[test key]', ('test', False, False, {'key': ''}, 10)),

        # Test tag value escape sequence
        ('[test="val\\"ue"]', ('test', False, False, {'test': 'val"ue'}, 16)),
        ('[test=\'val\\\'ue\']', ('test', False, False, {'test': 'val\'ue'}, 16)),

        # Test tag value erroneous escape sequence
        ('[test="val\\\'ue"]', ('test', False, False, {'test': 'val\\\'ue'}, 16)),
        ('[test=\'val\\"ue\']', ('test', False, False, {'test': 'val\\"ue'}, 16)),
        ('[test="val\\nue"]', ('test', False, False, {'test': 'val\\nue'}, 16)),
        ('[test=\'val\\nue\']', ('test', False, False, {'test': 'val\\nue'}, 16)),

        # Test attribute escape sequence
        ('[test key="val\\"ue"]', ('test', False, False, {'key': 'val"ue'}, 20)),
        ('[test key=\'val\\\'ue\']', ('test', False, False, {'key': 'val\'ue'}, 20)),

        # Test attribute erroneous escape sequence
        ('[test key="val\\\'ue"]', ('test', False, False, {'key': 'val\\\'ue'}, 20)),
        ('[test key=\'val\\"ue\']', ('test', False, False, {'key': 'val\\"ue'}, 20)),
        ('[test key="val\\nue"]', ('test', False, False, {'key': 'val\\nue'}, 20)),
        ('[test key=\'val\\nue\']', ('test', False, False, {'key': 'val\\nue'}, 20)),

        # Test simple closing tag with extra whitespaces
        ('[/test]', ('test', True, False, {}, 7)),
        ('[ /test]', ('test', True, False, {}, 8)),
        ('[ / test]', ('test', True, False, {}, 9)),
        ('[/test ]', ('test', True, False, {}, 8)),
        ('[/ test ]', ('test', True, False, {}, 9)),
        ('[ / test ]', ('test', True, False, {}, 10)),

        # Test simple self closing tag with extra whitespaces
        ('[test/]', ('test', False, True, {}, 7)),
        ('[test /]', ('test', False, True, {}, 8)),
        ('[test / ]', ('test', False, True, {}, 9)),
        ('[ test/]', ('test', False, True, {}, 8)),
        ('[ test /]', ('test', False, True, {}, 9)),
        ('[ test / ]', ('test', False, True, {}, 10)),

        # Test simple opening tag with tag value (unquoted)
        ('[test=value]', ('test', False, False, {'test': 'value'}, 12)),
        ('[test =value]', ('test', False, False, {'test': 'value'}, 13)),
        ('[test= value]', ('test', False, False, {'test': 'value'}, 13)),
        ('[test = value]', ('test', False, False, {'test': 'value'}, 14)),

        # Test simple opening tag with tag value (double quoted)
        ('[test="value"]', ('test', False, False, {'test': 'value'}, 14)),
        ('[test ="value"]', ('test', False, False, {'test': 'value'}, 15)),
        ('[test= "value"]', ('test', False, False, {'test': 'value'}, 15)),
        ('[test = "value"]', ('test', False, False, {'test': 'value'}, 16)),

        # Test simple opening tag with tag value (single quoted)
        ('[test=\'value\']', ('test', False, False, {'test': 'value'}, 14)),
        ('[test =\'value\']', ('test', False, False, {'test': 'value'}, 15)),
        ('[test= \'value\']', ('test', False, False, {'test': 'value'}, 15)),
        ('[test = \'value\']', ('test', False, False, {'test': 'value'}, 16)),

        # Test simple self closing tag with tag value (unquoted)
        ('[test=value /]', ('test', False, True, {'test': 'value'}, 14)),
        ('[test =value /]', ('test', False, True, {'test': 'value'}, 15)),
        ('[test= value /]', ('test', False, True, {'test': 'value'}, 15)),
        ('[test = value /]', ('test', False, True, {'test': 'value'}, 16)),
        ('[test=value / ]', ('test', False, True, {'test': 'value'}, 15)),
        ('[test =value / ]', ('test', False, True, {'test': 'value'}, 16)),
        ('[test= value / ]', ('test', False, True, {'test': 'value'}, 16)),
        ('[test = value / ]', ('test', False, True, {'test': 'value'}, 17)),

        # Test simple self closing tag with tag value (double quoted)
        ('[test="value" /]', ('test', False, True, {'test': 'value'}, 16)),
        ('[test ="value" /]', ('test', False, True, {'test': 'value'}, 17)),
        ('[test= "value" /]', ('test', False, True, {'test': 'value'}, 17)),
        ('[test = "value" /]', ('test', False, True, {'test': 'value'}, 18)),
        ('[test="value" / ]', ('test', False, True, {'test': 'value'}, 17)),
        ('[test ="value" / ]', ('test', False, True, {'test': 'value'}, 18)),
        ('[test= "value" / ]', ('test', False, True, {'test': 'value'}, 18)),
        ('[test = "value" / ]', ('test', False, True, {'test': 'value'}, 19)),

        # Test simple self closing tag with tag value (single quoted)
        ('[test=\'value\' /]', ('test', False, True, {'test': 'value'}, 16)),
        ('[test =\'value\' /]', ('test', False, True, {'test': 'value'}, 17)),
        ('[test= \'value\' /]', ('test', False, True, {'test': 'value'}, 17)),
        ('[test = \'value\' /]', ('test', False, True, {'test': 'value'}, 18)),
        ('[test=\'value\' / ]', ('test', False, True, {'test': 'value'}, 17)),
        ('[test =\'value\' / ]', ('test', False, True, {'test': 'value'}, 18)),
        ('[test= \'value\' / ]', ('test', False, True, {'test': 'value'}, 18)),
        ('[test = \'value\' / ]', ('test', False, True, {'test': 'value'}, 19)),

        # Test simple opening tag with a single attribute (unquoted)
        ('[test key=value]', ('test', False, False, {'key': 'value'}, 16)),
        ('[test key =value]', ('test', False, False, {'key': 'value'}, 17)),
        ('[test key= value]', ('test', False, False, {'key': 'value'}, 17)),
        ('[test key = value]', ('test', False, False, {'key': 'value'}, 18)),

        # Test simple opening tag with a single attribute (double quoted)
        ('[test key="value"]', ('test', False, False, {'key': 'value'}, 18)),
        ('[test key ="value"]', ('test', False, False, {'key': 'value'}, 19)),
        ('[test key= "value"]', ('test', False, False, {'key': 'value'}, 19)),
        ('[test key = "value"]', ('test', False, False, {'key': 'value'}, 20)),

        # Test simple opening tag with a single attribute (single quoted)
        ('[test key=\'value\']', ('test', False, False, {'key': 'value'}, 18)),
        ('[test key =\'value\']', ('test', False, False, {'key': 'value'}, 19)),
        ('[test key= \'value\']', ('test', False, False, {'key': 'value'}, 19)),
        ('[test key = \'value\']', ('test', False, False, {'key': 'value'}, 20)),

        # Test empty attribute quoted value
        ('[test key=""]', ('test', False, False, {'key': ''}, 13)),
        ('[test key=\'\']', ('test', False, False, {'key': ''}, 13)),

        # Test empty tag value quoted value
        ('[test=""]', ('test', False, False, {'test': ''}, 9)),
        ('[test=\'\']', ('test', False, False, {'test': ''}, 9)),

        # Test last unquoted value empty (with error case)
        ('[test=]', ('test', False, False, {'test': ''}, 7)),
        ('[test key=]', ('test', False, False, {'key': ''}, 11)),
        ('[test= key=]', ('test', False, False, {'test': 'key='}, 12)),

        # Test whitespaces strip in attribute quoted values
        ('[test key=" value "]', ('test', False, False, {'key': 'value'}, 20)),
        ('[test key=\' value \']', ('test', False, False, {'key': 'value'}, 20)),
        ('[test key="\tvalue\t"]', ('test', False, False, {'key': 'value'}, 20)),
        ('[test key=\'\tvalue\t\']', ('test', False, False, {'key': 'value'}, 20)),

        # Test simple opening tag with tag value (unquoted) and a single attribute
        ('[test=value key=value]', ('test', False, False, {'test': 'value', 'key': 'value'}, 22)),
        ('[test=value key="value"]', ('test', False, False, {'test': 'value', 'key': 'value'}, 24)),
        ('[test=value key=\'value\']', ('test', False, False, {'test': 'value', 'key': 'value'}, 24)),

        # Test simple opening tag with tag value (double quoted) and a single attribute
        ('[test="value" key=value]', ('test', False, False, {'test': 'value', 'key': 'value'}, 24)),
        ('[test="value" key="value"]', ('test', False, False, {'test': 'value', 'key': 'value'}, 26)),
        ('[test="value" key=\'value\']', ('test', False, False, {'test': 'value', 'key': 'value'}, 26)),

        # Test simple opening tag with tag value (single quoted) and a single attribute
        ('[test=\'value\' key=value]', ('test', False, False, {'test': 'value', 'key': 'value'}, 24)),
        ('[test=\'value\' key="value"]', ('test', False, False, {'test': 'value', 'key': 'value'}, 26)),
        ('[test=\'value\' key=\'value\']', ('test', False, False, {'test': 'value', 'key': 'value'}, 26)),

        # Test simple opening tag with tag value (unquoted) and multiple attributes
        ('[test=value key=value key2=value2]', ('test', False, False,
                                                {'test': 'value', 'key': 'value', 'key2': 'value2'}, 34)),
        ('[test=value key="value" key2="value2"]', ('test', False, False,
                                                    {'test': 'value', 'key': 'value', 'key2': 'value2'}, 38)),
        ('[test=value key=\'value\' key2=\'value2\']', ('test', False, False,
                                                        {'test': 'value', 'key': 'value', 'key2': 'value2'}, 38)),

        # Test simple opening tag with tag value (double quoted) and multiple attributes
        ('[test="value" key=value key2=value2]', ('test', False, False,
                                                  {'test': 'value', 'key': 'value', 'key2': 'value2'}, 36)),
        ('[test="value" key="value" key2="value2"]', ('test', False, False,
                                                      {'test': 'value', 'key': 'value', 'key2': 'value2'}, 40)),
        ('[test="value" key=\'value\' key2=\'value2\']', ('test', False, False,
                                                          {'test': 'value', 'key': 'value', 'key2': 'value2'}, 40)),

        # Test simple opening tag with tag value (single quoted) and multiple attributes
        ('[test=\'value\' key=value key2=value2]', ('test', False, False,
                                                    {'test': 'value', 'key': 'value', 'key2': 'value2'}, 36)),
        ('[test=\'value\' key="value" key2="value2"]', ('test', False, False,
                                                        {'test': 'value', 'key': 'value', 'key2': 'value2'}, 40)),
        ('[test=\'value\' key=\'value\' key2=\'value2\']', ('test', False, False,
                                                            {'test': 'value', 'key': 'value', 'key2': 'value2'}, 40)),

        # Test simple opening tag with unquoted value ending with slash at end of the tag attrs
        ('[test=http://example.com/]', ('test', False, False, {'test': 'http://example.com/'}, 26)),
        ('[test url=http://example.com/]', ('test', False, False, {'url': 'http://example.com/'}, 30)),
    )

    # --- Error handling tests
    FAIL_TESTS = (
        # Opening tag without end
        ('[', IndexError),
        ('[ ', IndexError),
        ('[/', IndexError),
        ('[/ ', IndexError),
        ('[ /', IndexError),
        ('[ / ', IndexError),

        # Opening tag without name
        ('[[', ValueError),
        ('[]', ValueError),
        ('[/]', ValueError),
        ('[#', ValueError),
        ('["', ValueError),

        # Opening tag without end after tag name
        ('[test', IndexError),
        ('[test ', IndexError),

        # Closing tag with arguments
        ('[/test=value]', ValueError),
        ('[/test =value]', ValueError),
        ('[/test= value]', ValueError),
        ('[/test = value]', ValueError),
        ('[/test key=value]', ValueError),

        # Opening tag without end after attribute value
        ('[test=', IndexError),
        ('[test= ', IndexError),
        ('[test="', IndexError),
        ('[test="aaa', IndexError),
        ('[test="a\\', IndexError),
        ('[test=""', IndexError),

        # Opening tag without space between attribute names
        ('[test=""a', ValueError),
        ('[test=\'\'a', ValueError),

        # Opening tag without end after tag value
        ('[test=a', IndexError),
        ('[test=a ', IndexError),

        # Opening tag without end after attribute name or value
        ('[test key', IndexError),
        ('[test key ', IndexError),
        ('[test key=', IndexError),
        ('[test key= ', IndexError),
        ('[test key=a', IndexError),
        ('[test key=a ', IndexError),

        # Opening tag with erroneous attribute name
        ('[test key=value =value', ValueError),
        ('[test key=value #=value ', ValueError),

        # Opening tag without end after attribute value
        ('[test key=', IndexError),
        ('[test key= ', IndexError),
        ('[test key="', IndexError),
        ('[test key="aaa', IndexError),
        ('[test key="a\\', IndexError),
        ('[test key=""', IndexError),

        # Opening tag without space between attribute names
        ('[test key=""a', ValueError),
        ('[test key=\'\'a', ValueError),

        # Opening tag without end after final slash
        ('[test /', IndexError),
        ('[test / ', IndexError),
        ('[test />', ValueError),

        # Malformed self closing tag
        ('[/test /]', ValueError),

        # Malformed unquote value (real world mistake)
        ('[test=value[', ValueError),
        ('[test=value[foobar[/url]', ValueError),
        ('[test=value[ foobar[/url]', ValueError),
        ('[test key=value[', ValueError),
        ('[test key=value[foobar[/url]', ValueError),
        ('[test key=value[ foobar[/url]', ValueError),
    )

    def test_functional(self):
        """ Functional tests. """
        for text, excepted_result in self.PASS_TESTS:
            result = parse_tag(text, 0, opening_tag_ch='[', closing_tag_ch=']')
            self.assertEqual(result, excepted_result, msg=text)

    def test_error(self):
        """ Error handling tests. """
        for text, excepted_exception in self.FAIL_TESTS:
            with self.assertRaises(excepted_exception, msg=text):
                parse_tag(text, 0, opening_tag_ch='[', closing_tag_ch=']')

    def test_html_compatibility_mode(self):
        """ Test if the HTML retro-compatibility mode work as expected. """
        with self.assertRaises(ValueError):
            parse_tag('[tagname=tagvalue]', 0, opening_tag_ch='[', closing_tag_ch=']', allow_tagvalue_attr=False)

    def test_html_compatibility_mode_no_xhtml(self):
        """ Test if the HTML retro-compatibility mode work as expected (without allowing XHTML-like tags). """
        with self.assertRaises(ValueError):
            parse_tag('[tagname/]', 0, opening_tag_ch='[', closing_tag_ch=']', allow_self_closing_tags=False)
