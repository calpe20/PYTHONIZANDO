from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QIcon

from tree_symbols_widget import TreeSymbolsWidget
from tree_projects_widget import TreeProjectsWidget
from gui.generic.properties_panel import PropertiesGeneric

class PropertiesWidget(QTabWidget, PropertiesGeneric):

    def __init__(self, main):
        QTabWidget.__init__(self)
        PropertiesGeneric.__init__(self)
        self.setTabPosition(QTabWidget.East)

        self._treeProjects = TreeProjectsWidget(main)
        self._treeSymbols = TreeSymbolsWidget()
        self.addTab(self._treeProjects, 'Projects')
        self.addTab(self._treeSymbols, 'Symbols')

    def add_tab(self, widget, name, icon):
        self.addTab(widget, QIcon(icon), name)

    def install_project_menu(self, menu, lang):
        if lang not in self._treeProjects.extraMenus:
            self._treeProjects.extraMenus[lang] = [menu]
        else:
            self._treeProjects.extraMenus[lang] += [menu]