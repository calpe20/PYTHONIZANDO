from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QToolTip
from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QTextOption
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextDocument
from PyQt4.QtGui import QFontMetrics
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QTextFormat
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QBrush
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QCursor
from PyQt4.QtGui import QFont
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from PyQt4 import QtCore

from highlighter import Highlighter
from highlighter_pygments import HighlighterPygments
from gui.generic.main_panel import EditorGeneric
from gui.generic import BaseCentralWidget
from gui.qt.qtcss import styles
from tools import loader
from tools import manage_files

from completer import Completer

class Editor(QPlainTextEdit, EditorGeneric, BaseCentralWidget):

    def __init__(self, parent, project=None):
        QPlainTextEdit.__init__(self)
        EditorGeneric.__init__(self)
        BaseCentralWidget.__init__(self)
        self.parent = parent
        self.completer = Completer(self, project)
        self.setWordWrapMode(QTextOption.NoWrap)
        doc = self.document()
        option = QTextOption()
        option.setFlags(QTextOption.ShowTabsAndSpaces)
        doc.setDefaultTextOption(option)
        self.setDocument(doc)
        self.set_default_font()

        #file modification time POSIX
        self._mtime = None
        #Flag to dont bug the user when answer 'dont show the modification dialog'
        self.ask_if_externally_modified = True

        self.lineNumberArea = self.LineNumberArea(self)
        self.viewport().installEventFilter(self)

        self.highlighter = None
        styles.set_style(self, 'editor')

        self.connect(self, SIGNAL("cursorPositionChanged()"), self.highlight_current_line)
        self.connect(self, SIGNAL("modificationChanged(bool)"), self.modif_changed)
        self.highlight_current_line()

    def set_path(self, fileName):
        super(Editor, self).set_path(fileName)
        self.newDocument = False
        self._mtime = manage_files.get_last_modification(fileName)

    def check_external_modification(self):
        if self.newDocument:
            return False
        #Saved document we can ask for modification!
        return manage_files.check_for_external_modification(self.path, self._mtime)

    def has_write_permission(self):
        if self.newDocument:
            return True
        return manage_files.has_write_prmission(self.path)

    def register_syntax(self, fileName):
        ext = manage_files.get_file_extension(fileName)[1:]
        if self.highlighter is not None and \
            not self.path.endswith(ext):
            self.highlighter.deleteLater()
        if not self.path.endswith(ext):
            if ext in loader.extensions:
                self.highlighter = Highlighter(self.document(),
                    loader.extensions.get(ext, 'py'))
            else:
                try:
                    self.highlighter = HighlighterPygments(self.document(), fileName)
                except:
                    print 'There is no lexer for this file'
            #for apply rehighlighting (rehighlighting form highlighter not responding)
            self.firstVisibleBlock().document().find('\n').insertText('')

    def set_font(self, font):
        self.document().setDefaultFont(font)
        self.font_family = str(font.family())
        self.font_size = font.pointSize()
        self.parent.notify_font_change()

    def set_default_font(self):
        #Set Font and FontSize
        font = QFont(self.font_family, self.font_size)
        self.document().setDefaultFont(font)

    def get_font(self):
        return self.document().defaultFont()

    def get_text(self):
        return self.toPlainText()

    def modif_changed(self, val):
        if self.parent is not None:
            self.parent.mark_as_changed(val)

    def zoom_in(self):
        font = self.font()
        size = font.pointSize()
        if size < self.font_max_size:
            size += 2
            font.setPointSize(size)
        self.setFont(font)

    def zoom_out(self):
        font = self.font()
        size = font.pointSize()
        if size > self.font_min_size:
            size -= 2
            font.setPointSize(size)
        self.setFont(font)

    def comment(self):
        lang = manage_files.get_file_extension(self.get_path())[1:]
        key = loader.extensions.get(lang, 'python')
        comment_wildcard = loader.syntax[key]['comment'][0]
        
        #cursor is a COPY all changes do not affect the QPlainTextEdit's cursor!!!
        cursor = self.textCursor()
        start = self.document().findBlock(cursor.selectionStart()).firstLineNumber()
        end = self.document().findBlock(cursor.selectionEnd()).firstLineNumber()
        startPosition = self.document().findBlockByLineNumber(start).position()
        
        #Start a undo block
        cursor.beginEditBlock()
        
        #Move the COPY cursor
        cursor.setPosition(startPosition)
        #Move the QPlainTextEdit Cursor where the COPY cursor IS!
        self.setTextCursor(cursor)
        self.moveCursor(QTextCursor.StartOfLine)
        self.moveCursor(QTextCursor.Right, QTextCursor.KeepAnchor)
        text = self.textCursor().selectedText()
        if text == comment_wildcard:
            cursor.endEditBlock()
            self.uncomment(start, end, startPosition)
            return
        else:
            self.moveCursor(QTextCursor.StartOfLine)
        for i in xrange(start, end+1):
            self.textCursor().insertText(comment_wildcard)
            self.moveCursor(QTextCursor.Down)
            self.moveCursor(QTextCursor.StartOfLine)
        
        #End a undo block
        cursor.endEditBlock()

    def uncomment(self, start=-1, end=-1, startPosition=-1):
        lang = manage_files.get_file_extension(self.get_path())[1:]
        key = loader.extensions.get(lang, 'python')
        comment_wildcard = loader.syntax[key]['comment'][0]

        #cursor is a COPY all changes do not affect the QPlainTextEdit's cursor!!!
        cursor = self.textCursor()
        if start == -1 and end == -1 and startPosition == -1:
            start = self.document().findBlock(cursor.selectionStart()).firstLineNumber()
            end = self.document().findBlock(cursor.selectionEnd()).firstLineNumber()
            startPosition = self.document().findBlockByLineNumber(start).position()
        
        #Start a undo block
        cursor.beginEditBlock()
        
        #Move the COPY cursor
        cursor.setPosition(startPosition)
        #Move the QPlainTextEdit Cursor where the COPY cursor IS!
        self.setTextCursor(cursor)
        self.moveCursor(QTextCursor.StartOfLine)
        for i in xrange(start, end+1):
            self.moveCursor(QTextCursor.Right, QTextCursor.KeepAnchor)
            text = self.textCursor().selectedText()
            if text == comment_wildcard:
                self.textCursor().removeSelectedText()
            elif u'\u2029' in text:
                #\u2029 is the unicode char for \n
                #if there is a newline, rollback the selection made above.
                self.moveCursor(QTextCursor.Left, QTextCursor.KeepAnchor)
            
            self.moveCursor(QTextCursor.Down)
            self.moveCursor(QTextCursor.StartOfLine)
        
        #End a undo block
        cursor.endEditBlock()

    def insert_horizontal_line(self):
        self.moveCursor(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        text = unicode(self.textCursor().selection().toPlainText())
        self.moveCursor(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
        comment = '#' * (80 - len(text))
        self.textCursor().insertText(comment)

    def indent_more(self):
        #cursor is a COPY all changes do not affect the QPlainTextEdit's cursor!!!
        cursor = self.textCursor()
        selectionStart =  cursor.selectionStart()
        selectionEnd = cursor.selectionEnd()
        #line where indent_more should start and end
        start = self.document().findBlock(cursor.selectionStart()).firstLineNumber()
        end = self.document().findBlock(cursor.selectionEnd()).firstLineNumber()
        startPosition = self.document().findBlockByLineNumber(start).position()
        
        #Start a undo block
        cursor.beginEditBlock()
        
        #Decide which lines will be indented
        cursor.setPosition(selectionEnd)
        self.setTextCursor(cursor)
        #Select one char at left
        #If there is a newline \u2029 (\n) then skip it
        self.moveCursor(QTextCursor.Left, QTextCursor.KeepAnchor)
        if u'\u2029' in self.textCursor().selectedText():
            end -= 1
        
        cursor.setPosition(selectionStart)
        self.setTextCursor(cursor)
        self.moveCursor(QTextCursor.StartOfLine)
        #Indent loop; line by line 
        for i in xrange(start, end+1):
            self.textCursor().insertText(' '*Editor.indent)
            self.moveCursor(QTextCursor.Down, QTextCursor.MoveAnchor)

        #Restore the user selection
        cursor.setPosition(startPosition)
        selectionEnd = selectionEnd + (EditorGeneric.indent*(end-start+1))
        cursor.setPosition(selectionEnd, QTextCursor.KeepAnchor)
        self.setTextCursor(cursor)
        #End a undo block
        cursor.endEditBlock()

    def indent_less(self):
        #save the total of movements made after indent_less
        totalIndent = 0
        #cursor is a COPY all changes do not affect the QPlainTextEdit's cursor!!!
        cursor = self.textCursor()
        selectionEnd = cursor.selectionEnd()
        #line where indent_less should start and end
        start = self.document().findBlock(cursor.selectionStart()).firstLineNumber()
        end = self.document().findBlock(cursor.selectionEnd()).firstLineNumber()
        startPosition = self.document().findBlockByLineNumber(start).position()
        
        #Start a undo block
        cursor.beginEditBlock()
        
        #Decide which lines will be indented_less
        cursor.setPosition(selectionEnd)
        self.setTextCursor(cursor)
        #Select one char at left
        self.moveCursor(QTextCursor.Left, QTextCursor.KeepAnchor)
        #If there is a newline \u2029 (\n) then dont indent this line; skip it!
        if u'\u2029' in self.textCursor().selectedText():
            end -= 1

        cursor.setPosition(startPosition)
        self.setTextCursor(cursor)
        self.moveCursor(QTextCursor.StartOfLine)
        #Indent_less loop; line by line 
        for i in xrange(start, end+1):
            #Select EditorGeneric.indent chars from the current line
            for j in xrange(EditorGeneric.indent):
                self.moveCursor(QTextCursor.Right, QTextCursor.KeepAnchor)
            
            text = self.textCursor().selectedText()
            if text == ' '*EditorGeneric.indent:
                self.textCursor().removeSelectedText()
                totalIndent += EditorGeneric.indent
            elif u'\u2029' in text:
                #\u2029 is the unicode char for \n
                #if there is a newline, rollback the selection made above.
                for j in xrange(EditorGeneric.indent):
                    self.moveCursor(QTextCursor.Left, QTextCursor.KeepAnchor)
            
            #Go Down to the next line!
            self.moveCursor(QTextCursor.Down)
        #Restore the user selection
        cursor.setPosition(startPosition)
        cursor.setPosition(selectionEnd-totalIndent, QTextCursor.KeepAnchor)
        self.setTextCursor(cursor)
        #End a undo block
        cursor.endEditBlock()

    def find_match(self, word, back=False, sensitive=False, whole=False):
        b = QTextDocument.FindBackward if back else None
        s = QTextDocument.FindCaseSensitively if sensitive else None
        w = QTextDocument.FindWholeWords if whole else None
        self.moveCursor(QTextCursor.NoMove, QTextCursor.KeepAnchor)
        if back or sensitive or whole:
            self.find(word, b or s or w)
        else:
            self.find(word)

    def replace_match(self, wordOld, wordNew, sensitive=False, whole=False, all=False):
        s = QTextDocument.FindCaseSensitively if sensitive else None
        w = QTextDocument.FindWholeWords if whole else None
        self.moveCursor(QTextCursor.NoMove, QTextCursor.KeepAnchor)

        cursor = self.textCursor()
        cursor.beginEditBlock()

        self.moveCursor(QTextCursor.Start)
        replace = True
        while (replace or all):
            result = False
            if back or sensitive or whole:
                result = self.find(wordOld, s or w)
            else:
                result = self.find(wordOld)

            if result:
                tc = self.textCursor()
                if tc.hasSelection():
                    tc.insertText(wordNew)
            else:
                break
            replace = False

        cursor.endEditBlock()

    def highlight_current_line(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.darkCyan)
            lineColor.setAlpha(20)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def resizeEvent(self,e):
        self.lineNumberArea.setFixedHeight(self.height())
        QPlainTextEdit.resizeEvent(self,e)

    def eventFilter(self, object, event):
        if object is self.viewport():
            self.lineNumberArea.update()
            return False
        return QPlainTextEdit.eventFilter(object, event)

    def keyPressEvent(self, event):
        if self.completer is not None and self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab,
              Qt.Key_Escape, Qt.Key_Backtab):
                event.ignore()
                self.completer.popup().hide()
                return
            elif event.key == Qt.Key_Space:
                self.completer.popup().hide()

        if event.key() == Qt.Key_Tab:
            if self.textCursor().hasSelection():
                self.indent_more()
                return
            else:
                self.textCursor().insertText(' '*EditorGeneric.indent)
                return
        elif event.key() == Qt.Key_Backspace:
            if self.textCursor().hasSelection():
                super(Editor, self).keyPressEvent(event)
                return
            for i in xrange(EditorGeneric.indent):
                self.moveCursor(QTextCursor.Left, QTextCursor.KeepAnchor)
            text = self.textCursor().selection()
            if unicode(text.toPlainText()) == ' '*EditorGeneric.indent:
                self.textCursor().removeSelectedText()
                return
            else:
                for i in xrange(EditorGeneric.indent):
                    self.moveCursor(QTextCursor.Right)
        elif event.key() == Qt.Key_Home:
            if event.modifiers() == Qt.ShiftModifier:
                move = QTextCursor.KeepAnchor
            else:
                move = QTextCursor.MoveAnchor
            if self.textCursor().atBlockStart():
                self.moveCursor(QTextCursor.WordRight, move)
                return

        super(Editor, self).keyPressEvent(event)
        
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            text = unicode(self.document().findBlock(self.textCursor().position()-1).text())
            spaces = self.get_indentation(text)
            self.textCursor().insertText(spaces)
            if text != '' and text == ' '*len(text):
                previousLine = self.document().findBlock(self.textCursor().position()-1)
                self.moveCursor(QTextCursor.Up)
                self.moveCursor(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
                self.textCursor().removeSelectedText()
                self.moveCursor(QTextCursor.Down)
            self.eventKeyReturn()
        elif unicode(event.text()) in self.braces_strings:
            self.textCursor().insertText(self.braces_strings[str(event.text())])
            self.moveCursor(QTextCursor.Left)
        completionPrefix = self.text_under_cursor()
        if event.key() == Qt.Key_Period or \
          (event.key() == Qt.Key_Space and event.modifiers() == Qt.ControlModifier):
            self.completer.setCompletionPrefix('')
            cr = self.cursorRect()
            self.completer.complete(cr)
        if self.completer is not None and self.completer.popup().isVisible():
            if completionPrefix != self.completer.completionPrefix():
                self.completer.setCompletionPrefix(completionPrefix)
                self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))
                self.completer.setCurrentRow(0)
                cr = self.cursorRect()
                self.completer.complete(cr)
        self.eventKeyAny()

    def text_under_cursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            if event.delta() == 120:
                self.zoom_in()
            elif event.delta() == -120:
                self.zoom_out()
            event.ignore()
        else:
            super(Editor, self).wheelEvent(event)

    def focusInEvent(self, event):
        super(Editor, self).focusInEvent(event)
        self.parent.editor_focus()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            fileName = str(event.mimeData().text())[7:].rstrip()
            content = manage_files.read_file_content(fileName)
            self.setPlainText(content)

    def contextMenuEvent(self, event):
        popup_menu = self.createStandardContextMenu()

        lang = manage_files.get_file_extension(self.get_path())[1:]
        if EditorGeneric.extraMenus.get(lang, False):
            popup_menu.insertSeparator(popup_menu.actions()[0])
            popup_menu.insertMenu(popup_menu.actions()[0], EditorGeneric.extraMenus[lang])

        popup_menu.exec_(event.globalPos())


    #based on: http://john.nachtimwald.com/2009/08/15/qtextedit-with-line-numbers/ (MIT license)
    class LineNumberArea(QWidget):

        def __init__(self, editor):
            QWidget.__init__(self, editor)
            self.edit = editor
            self.highest_line = 0
            css = '''
            QWidget {
              font-family: monospace;
              font-size: 10;
              color: black;
            }'''
            self.setStyleSheet(css)
 
        def update(self, *args):
            width = QFontMetrics(self.edit.document().defaultFont()).width(str(self.highest_line)) + 10
            if self.width() != width:
                self.setFixedWidth(width)
                self.edit.setViewportMargins(width,0,0,0)
            QWidget.update(self, *args)
 
        def paintEvent(self, event):
            contents_y = 0
            page_bottom = self.edit.viewport().height()
            font_metrics = QFontMetrics(self.edit.document().defaultFont())
            current_block = self.edit.document().findBlock(self.edit.textCursor().position())
 
            painter = QPainter(self)
            painter.fillRect(self.rect(), Qt.lightGray)
            
            block = self.edit.firstVisibleBlock()
            viewport_offset = self.edit.contentOffset()
            line_count = block.blockNumber()
            painter.setFont(self.edit.document().defaultFont())
            while block.isValid():
                line_count += 1
                # The top left position of the block in the document
                position = self.edit.blockBoundingGeometry(block).topLeft() + viewport_offset
                # Check if the position of the block is out side of the visible area
                if position.y() > page_bottom:
                    break
 
                # We want the line number for the selected line to be bold.
                bold = False
                if block == current_block:
                    bold = True
                    font = painter.font()
                    font.setBold(True)
                    painter.setFont(font)
 
                # Draw the line number right justified at the y position of the
                # line. 3 is a magic padding number. drawText(x, y, text).
                painter.drawText(self.width() - font_metrics.width(str(line_count)) - 3,
                    round(position.y()) + font_metrics.ascent()+font_metrics.descent()-1,
                    str(line_count))
 
                # Remove the bold style if it was set previously.
                if bold:
                    font = painter.font()
                    font.setBold(False)
                    painter.setFont(font)
 
                block = block.next()
 
            self.highest_line = line_count
            painter.end()
 
            QWidget.paintEvent(self, event)


def factory_editor(fileName, parent, project=None):
    editor = Editor(parent, project)
    editor.register_syntax('lang.' + fileName)
    return editor
