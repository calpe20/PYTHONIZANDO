from PyQt4.QtGui import QAction
from PyQt4.QtGui import QIcon
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject

import resources
from resources import OS_KEY


class MenuEdit(object):

    def __init__(self, menu, tool, main, status):
        self._main = main
        self._status = status

        undoAction = menu.addAction(QIcon(resources.images['undo']), 'Undo ('+OS_KEY+'+Z)')
        redoAction = menu.addAction(QIcon(resources.images['redo']), 'Redo ('+OS_KEY+'+Y)')
        cutAction = menu.addAction(QIcon(resources.images['cut']), '&Cut ('+OS_KEY+'+X)')
        copyAction = menu.addAction(QIcon(resources.images['copy']), '&Copy ('+OS_KEY+'+C)')
        pasteAction = menu.addAction(QIcon(resources.images['paste']), '&Paste ('+OS_KEY+'+V)')
        menu.addSeparator()
        indentMoreAction = menu.addAction(QIcon(resources.images['indent-more']), 'Indent More (Tab)')
        indentLessAction = menu.addAction(QIcon(resources.images['indent-less']), 'Indent Less (Shift+Tab)')
        menu.addSeparator()
        commentAction = menu.addAction(QIcon(resources.images['comment-code']),'Comment ('+OS_KEY+'+D)')
        unCommentAction = menu.addAction(QIcon(resources.images['uncomment-code']),'Uncomment ('+OS_KEY+'+D)')
        horizontalLineAction = menu.addAction('Insert Horizontal Line ('+OS_KEY+'+R)')
        menu.addSeparator()
        findAction = menu.addAction(QIcon(resources.images['find']), 'Find ('+OS_KEY+'+F)')
        findReplaceAction = menu.addAction(QIcon(resources.images['findReplace']), 'Find/Replace ('+OS_KEY+'+H)')
        menu.addSeparator()
        prefAction = menu.addAction(QIcon(resources.images['pref']), 'Preference&s')

        tool.addSeparator()
        tool.addAction(cutAction)
        tool.addAction(copyAction)
        tool.addAction(pasteAction)

        QObject.connect(cutAction, SIGNAL("triggered()"), lambda: self._main._central.actual_tab().obtain_editor().cut())
        QObject.connect(copyAction, SIGNAL("triggered()"), lambda: self._main._central.actual_tab().obtain_editor().copy())
        QObject.connect(pasteAction, SIGNAL("triggered()"), lambda: self._main._central.actual_tab().obtain_editor().paste())
        QObject.connect(redoAction, SIGNAL("triggered()"), lambda: self._main._central.actual_tab().obtain_editor().redo())
        QObject.connect(undoAction, SIGNAL("triggered()"), lambda: self._main._central.actual_tab().obtain_editor().undo())
        QObject.connect(indentMoreAction, SIGNAL("triggered()"), lambda: self._main._central.actual_tab().obtain_editor().indent_more())
        QObject.connect(indentLessAction, SIGNAL("triggered()"), lambda: self._main._central.actual_tab().obtain_editor().indent_less())
        QObject.connect(commentAction, SIGNAL("triggered()"), lambda: self._main._central.actual_tab().obtain_editor().comment())
        QObject.connect(unCommentAction, SIGNAL("triggered()"), lambda: self._main._central.actual_tab().obtain_editor().uncomment())
        QObject.connect(horizontalLineAction, SIGNAL("triggered()"), lambda: self._main._central.actual_tab().obtain_editor().insert_horizontal_line())
        QObject.connect(findAction, SIGNAL("triggered()"), lambda: self._main._open_find())
        QObject.connect(findReplaceAction, SIGNAL("triggered()"), lambda: self._main._open_find_replace())
        QObject.connect(prefAction, SIGNAL("triggered()"), main.show_preferences)