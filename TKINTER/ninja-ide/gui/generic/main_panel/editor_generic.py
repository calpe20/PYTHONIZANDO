import re

class EditorGeneric(object):

    anyKeyEvent = []
    returnKeyEvent = []
    extraMenus = {}

    indent = 4
    patIndent = re.compile('^\s+')
    braces_strings = {"'":"'", '"':'"', '{':'}', '(':')', '[':']'}
    font_max_size = 28
    font_min_size = 6
    font_family = "Monospace"
    font_size = 10

    def __init__(self):
        pass

    def get_indentation(self, line):
        indentation = ''
        if len(line) > 0 and line[-1] in [':', '{', '(', '[']:
            indentation = ' '*4
        space = self.patIndent.match(line)
        if space is not None:
            return space.group() + indentation
        return indentation

    def eventKeyReturn(self):
        for plug in EditorGeneric.returnKeyEvent:
            plug.eventKeyReturn()

    def eventKeyAny(self):
        for plug in EditorGeneric.anyKeyEvent:
            plug.eventKeyAny()
