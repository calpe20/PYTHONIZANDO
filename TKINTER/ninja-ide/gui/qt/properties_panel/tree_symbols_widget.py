from PyQt4.QtGui import QTreeWidget

from gui.qt.qtcss import styles

class TreeSymbolsWidget(QTreeWidget):

    def __init__(self):
        QTreeWidget.__init__(self)
        styles.apply(self, 'tree')
