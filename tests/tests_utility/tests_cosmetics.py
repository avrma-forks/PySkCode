"""
SkCode cosmetics replacement utility test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import TextTreeNode
from skcode.utility.cosmetics import (
    setup_cosmetics_replacement,
    do_cosmetics_replacement,
    DEFAULT_COSMETICS_MAP,
    COSMETICS_MAP_ATTR_NAME
)


class CosmeticsUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the cosmetics utility module. """

    def test_setup_cosmetics_replacement(self):
        """ Test the ``setup_cosmetics_replacement`` helper. """
        document_tree = RootTreeNode()
        self.assertNotIn(COSMETICS_MAP_ATTR_NAME, document_tree.attrs)
        setup_cosmetics_replacement(document_tree, DEFAULT_COSMETICS_MAP)
        self.assertIn(COSMETICS_MAP_ATTR_NAME, document_tree.attrs)
        self.assertEqual(DEFAULT_COSMETICS_MAP, document_tree.attrs[COSMETICS_MAP_ATTR_NAME])

    def test_do_cosmetics_replacement_no_input(self):
        """ Test the ``do_cosmetics_replacement`` function. """
        root_tree_node = RootTreeNode()
        output = do_cosmetics_replacement(root_tree_node, '')
        self.assertEqual('', output)

    def test_do_cosmetics_replacement_no_setup(self):
        """ Test the ``do_cosmetics_replacement`` function. """
        root_tree_node = RootTreeNode()
        output = do_cosmetics_replacement(root_tree_node, 'Test ...')
        self.assertEqual('Test ...', output)

    def test_do_cosmetics_replacement(self):
        """ Test the ``do_cosmetics_replacement`` function. """
        root_tree_node = RootTreeNode()
        setup_cosmetics_replacement(root_tree_node, DEFAULT_COSMETICS_MAP)
        output = do_cosmetics_replacement(root_tree_node, 'Foo --- bar')
        self.assertEqual('Foo — bar', output)
        output = do_cosmetics_replacement(root_tree_node, 'Foo -- bar')
        self.assertEqual('Foo — bar', output)
        output = do_cosmetics_replacement(root_tree_node, 'Test ...')
        self.assertEqual('Test …', output)
        output = do_cosmetics_replacement(root_tree_node, 'FooBar(tm)')
        self.assertEqual('FooBar™', output)

    def test_do_cosmetics_replacement_text(self):
        """ Test the ``do_cosmetics_replacement`` function. """
        root_tree_node = RootTreeNode()
        setup_cosmetics_replacement(root_tree_node, DEFAULT_COSMETICS_MAP)
        tree_node = root_tree_node.new_child(None, TextTreeNode, content='Test ...')
        output = tree_node.render_html('')
        self.assertEqual('Test …', output)
        output = tree_node.render_text('')
        self.assertEqual('Test …', output)
