"""
based on Python Syntax highlighting from:
http://diotavelli.net/PyQtWiki/Python%20syntax%20highlighting
"""
import sys

from PyQt4.QtCore import QRegExp
from PyQt4.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter, QPen

from tools import loader

def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setFontFamily('monospace')
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages
STYLES = {
    'keyword': format('darkMagenta', 'bold'),
    'operator': format('darkRed'),
    'brace': format('#858585'),
    'definition': format('black', 'bold'),
    'string': format('green'),
    'string2': format('darkGreen'),
    'comment': format('gray', 'italic'),
    'properObject': format('darkBlue', 'italic'),
    'numbers': format('brown'),
    'spaces': format('#BFBFBF'),
}


class Highlighter (QSyntaxHighlighter):
    keywords = []

    # operators
    operators = []

    # braces
    braces = []
    def __init__(self, document, lang):
        QSyntaxHighlighter.__init__(self, document)
        langSyntax = loader.syntax[lang]
        Highlighter.keywords = langSyntax.get('keywords', [])
        Highlighter.braces = langSyntax.get('brace', [])
        Highlighter.operators = langSyntax.get('operators', [])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
            for w in Highlighter.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
            for o in Highlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
            for b in Highlighter.braces]

        # All other rules
        proper = langSyntax.get('properObject', None)
        if proper is not None:
            proper = '\\b' + str(proper[0]) + '\\b'
            rules += [
                # 'self'
                (proper, 0, STYLES['properObject'])]

        rules.append((r'__\w+__', 0, STYLES['properObject']))
            
        definition = langSyntax.get('definition', [])
        for de in definition:
            expr = '\\b' + de + '\\b\\s*(\\w+)'
            rules.append((expr, 1, STYLES['definition']))

        rules += [
            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        stringChar = langSyntax.get('string', [])
        for sc in stringChar:
            expr = r'"[^"\\]*(\\.[^"\\]*)*"' if sc == '"' else r"'[^'\\]*(\\.[^'\\]*)*'"
            rules.append((expr, 0, STYLES['string']))

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])    #'''
        self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])    #"""

        comments = langSyntax.get('comment', [])
        for co in comments:
            expr = co + '[^\\n]*'
            rules.append((expr, 0, STYLES['comment']))

        rules.append(('\s+', 0, STYLES['spaces']))

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
            for (pat, index, fmt) in rules]


    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = expression.cap(nth).length()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)


    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = text.length() - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False
