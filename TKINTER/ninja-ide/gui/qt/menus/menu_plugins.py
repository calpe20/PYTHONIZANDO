from PyQt4.QtGui import QAction
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL

from plugins_manager_widget import PluginsManagerWidget

class MenuPlugins(object):

    def __init__(self, menu, ide):
        self._ide = ide

        manageAction = menu.addAction('Manage Plugins')

        QObject.connect(manageAction, SIGNAL("triggered()"), self._show_manager)

    def _show_manager(self):
        manager = PluginsManagerWidget(self._ide)
        manager.show()