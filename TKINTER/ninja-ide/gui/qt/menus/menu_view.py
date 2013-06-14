from PyQt4.QtGui import QAction
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QWheelEvent
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QPoint

import resources
from resources import OS_KEY


class MenuView(object):

    def __init__(self, menu, parent, main):
        self._main = main
        self._parent = parent

        self.hideConsoleAction = menu.addAction('Show/Hide &Console (F4)')
        self.hideConsoleAction.setCheckable(True)
        self.hideEditorAction = menu.addAction('Show/Hide &Editor (F3)')
        self.hideEditorAction.setCheckable(True)
        self.hideAllAction = menu.addAction('Show/Hide &All (F11)')
        self.hideAllAction.setCheckable(True)
        self.hideExplorerAction = menu.addAction('Show/Hide &Explorer (F2)')
        self.hideExplorerAction.setCheckable(True)
        menu.addSeparator()
        splitTabHAction = menu.addAction(QIcon(resources.images['splitH']), 'Split Tabs Horizontally (F10)')
        splitTabVAction = menu.addAction(QIcon(resources.images['splitV']), 'Split Tabs Vertically (F9)')
        menu.addSeparator()
        #Panels Properties
        self.menuProperties = QMenu('Panels Properties')
        self.splitCentralOrientation = self.menuProperties.addAction('Change Central Splitter Orientation')
        self.splitMainOrientation = self.menuProperties.addAction('Change Main Splitter Orientation')
        self.menuProperties.addSeparator()
        self.splitCentralRotate = self.menuProperties.addAction(QIcon(resources.images['splitCRotate']), 'Rotate Central Panels')
        self.splitMainRotate = self.menuProperties.addAction(QIcon(resources.images['splitMRotate']), 'Rotate GUI Panels')
        menu.addMenu(self.menuProperties)
        menu.addSeparator()
        #Zoom
        zoomInAction = menu.addAction('Zoom &In ('+OS_KEY+'+Wheel-Up)')
        zoomOutAction = menu.addAction('Zoom &Out ('+OS_KEY+'+Wheel-Down)')
        menu.addSeparator()
        fadeInAction = menu.addAction('Fade In (Alt+Wheel-Up)')
        fadeOutAction = menu.addAction('Fade Out (Alt+Wheel-Down)')

        self._parent._toolbar.addSeparator()
        self._parent._toolbar.addAction(splitTabHAction)
        self._parent._toolbar.addAction(splitTabVAction)

        QObject.connect(self.hideConsoleAction, SIGNAL("triggered()"), self._main._hide_container)
        QObject.connect(self.hideEditorAction, SIGNAL("triggered()"), self._main._hide_editor)
        QObject.connect(self.hideExplorerAction, SIGNAL("triggered()"), self._main._hide_explorer)
        QObject.connect(self.hideAllAction, SIGNAL("triggered()"), self._main._hide_all)
        QObject.connect(splitTabHAction, SIGNAL("triggered()"), lambda: self._main.split_tab(True))
        QObject.connect(splitTabVAction, SIGNAL("triggered()"), lambda: self._main.split_tab(False))
        QObject.connect(zoomInAction, SIGNAL("triggered()"), lambda: self._main._central.actual_tab().obtain_editor().zoom_in())
        QObject.connect(zoomOutAction, SIGNAL("triggered()"), lambda: self._main._central.actual_tab().obtain_editor().zoom_out())
        QObject.connect(self.splitCentralOrientation, SIGNAL("triggered()"), self._main._splitter_central_orientation)
        QObject.connect(self.splitMainOrientation, SIGNAL("triggered()"), self._main._splitter_main_orientation)
        QObject.connect(self.splitCentralRotate, SIGNAL("triggered()"), self._main._splitter_central_rotate)
        QObject.connect(self.splitMainRotate, SIGNAL("triggered()"), self._main._splitter_main_rotate)
        QObject.connect(fadeInAction, SIGNAL("triggered()"), self._fade_in)
        QObject.connect(fadeOutAction, SIGNAL("triggered()"), self._fade_out)

    def _fade_in(self):
        event = QWheelEvent(QPoint(), 120, Qt.NoButton, Qt.AltModifier)
        self._parent.wheelEvent(event)

    def _fade_out(self):
        event = QWheelEvent(QPoint(), -120, Qt.NoButton, Qt.AltModifier)
        self._parent.wheelEvent(event)
