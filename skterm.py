#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test terminal for the SkCode project.
"""

from skcode.etree import debug_print_ast
from skcode import (
    parse_skcode,
    render_to_html,
    render_to_text
)


# Terminal code
if __name__ == '__main__':
    print('-- SkCode testing terminal --')

    # Get user input
    print('Use CTRL+C, CTRL+D or simply type "EOF" on a single line to stop text input')
    text = []
    try:
        while True:
            line = input('skcode> ')
            if line == 'EOF':
                break
            text.append(line)
    except (KeyboardInterrupt, EOFError):
        pass
    text = '\n'.join(text)

    # Parse text
    ast = parse_skcode(text)

    # Dump parsing info
    print('----- Input text -----')
    print(text)
    print('----- Document tree -----')
    debug_print_ast(ast)
    print('----- HTML output -----')
    print(render_to_html(ast))
    print('----- TEXT output -----')
    print(render_to_text(ast))

    # End of script
    input('Press enter to exit.')
