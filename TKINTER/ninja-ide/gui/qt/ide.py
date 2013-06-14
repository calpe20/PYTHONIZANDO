import sys
import os

from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QToolBar
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QSplashScreen
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QSettings

from main_window import MainWindow
from menus import MenuFile
from menus import MenuEdit
from menus import MenuProject
from menus import MenuPlugins
from menus import MenuView
from menus import MenuAbout

import core
import resources
from status_bar import StatusBar
from tools import loader
from gui.qt.qtcss import styles
from gui.generic import IDEGeneric

class IDE(QMainWindow, IDEGeneric):

    max_opacity = 1
    min_opacity = 0.3

    def __init__(self):
        QWidget.__init__(self)
        IDEGeneric.__init__(self)
        self.setWindowTitle('NINJA-IDE {Ninja Is Not Just Another IDE}')
        self.setWindowIcon(QIcon(resources.images['icon']))
        self.setWindowState(Qt.WindowMaximized)
        self.setMinimumSize(700, 500)

        #Opactity
        self.opacity = 1

        #ToolBar
        self._toolbar = QToolBar()
        self._toolbar.setToolTip('Press and Drag to Move')
        styles.set_style(self._toolbar, 'toolbar-default')
        self.addToolBar(Qt.LeftToolBarArea, self._toolbar)
        self._toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        #StatusBar
        self._status = StatusBar()
        self._status.hide()
        self.setStatusBar(self._status)

        #Main Widgets
        self.main = MainWindow(self)
        self.setCentralWidget(self.main)

        #Menu
        menubar = self.menuBar()
        styles.apply(menubar, 'menu')
        file_ = menubar.addMenu('&File')
        edit = menubar.addMenu('&Edit')
        view = menubar.addMenu('&View')
        project = menubar.addMenu('&Project')
        self.pluginsMenu = menubar.addMenu('P&lugins')
        about = menubar.addMenu('&About')

        #The order of the icons in the toolbar is defined by this calls
        self._menuFile = MenuFile(file_, self._toolbar, self.main)
        self._menuView = MenuView(view, self, self.main)
        self._menuEdit = MenuEdit(edit, self._toolbar, self.main, self._status)
        self._menuProject = MenuProject(project, self._toolbar, self.main)
        self._menuPlugins = MenuPlugins(self.pluginsMenu, self)
        self._menuAbout = MenuAbout(about, self.main)

        self.main.container.load_toolbar(self._toolbar)
        self.main._central.actual_tab().obtain_editor().setFocus()

        filenames, projects_path = core.cliparser.parse()

        for filename in filenames:
            self.main.open_document(filename)

        for project_path in projects_path:
            self.main.open_project_folder(project_path)

        self.connect(self.main, SIGNAL("fileSaved(QString)"), self.show_status_message)

    def show_status_message(self, message):
        self._status.showMessage(message, 2000)

    def add_toolbar_item(self, plugin, name, icon):
        self._toolbar.addSeparator()
        action = self._toolbar.addAction(QIcon(icon), name)
        self.connect(action, SIGNAL("triggered()"), lambda: plugin.toolbarAction())

    def closeEvent(self, event):
        settings = QSettings('NINJA-IDE','Kunai')
        if settings.value('Preferences/General/load_files', 2).toInt()[0]==2:
            settings.setValue('Open_Files/projects',self.main.get_open_projects())
            settings.setValue('Open_Files/tab1', self.main._central._tabs.get_open_files())
            settings.setValue('Open_Files/tab2', self.main._central._tabs2.get_open_files())
        else:
            settings.setValue('Open_Files/projects',[])

        if self.main._central.check_for_unsaved():
            val = QMessageBox.question(self, 'Some changes were not saved',
                        'Do you want to exit anyway?', QMessageBox.Yes, QMessageBox.No)
            if val == QMessageBox.No:
                event.ignore()
            else:
                self.main._properties._treeProjects.close_open_projects()
        else:
            self.main._properties._treeProjects.close_open_projects()

    def wheelEvent(self, event):
        if event.modifiers() == Qt.AltModifier:
            if event.delta() == 120 and self.opacity < self.max_opacity:
                self.opacity += 0.1
            elif event.delta() == -120 and self.opacity > self.min_opacity:
                self.opacity -= 0.1
            self.setWindowOpacity(self.opacity)
            event.ignore()
        else:
            super(IDE, self).wheelEvent(event)


def set_plugin_access(ide):
    core.register_plugin_access(ide.main._central.obtain_editor,
        ide.main._central.obtain_editor().get_text,
        ide.main._central.obtain_editor().get_path,
        ide.main.new_editor,
        ide.main.add_tab,
        ide.main.save,
        ide.main.open_document,
        ide.main.open_image,
        ide.main._properties._treeProjects.get_selected_project_path
        )

def start():
    app = QApplication(sys.argv)

    # Create and display the splash screen
    splash_pix = QPixmap(resources.images['splash'])
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    loader.load_syntax()

    ide = IDE()
    #Settings
    settings = QSettings('NINJA-IDE','Kunai')
    if (settings.value('Preferences/General/activate_plugins', 2)==2):
        set_plugin_access(ide)
        core.load_plugins(ide)

    ide.show()
    for projectFolder in settings.value('Open_Files/projects',[]).toStringList():
        ide.main.open_project_folder(str(projectFolder))

    for openFile in settings.value('Open_Files/tab1', []).toStringList():
        ide.main.open_document(str(openFile))

    for openFile2 in settings.value('Open_Files/tab2', []).toStringList():
        ide.main.split_tab(True)
        ide.main.open_document(str(openFile2))

    splash.finish(ide)
    sys.exit(app.exec_())

def load_settings(self, ide):
    settings = QSettings('NINJA-IDE','Kunai')
    settings.beginGroup('Preferences')
    #General Settings
    settings.beginGroup('General')
    settings.value('load_files', 2)
    settings.value('activate_plugins', 2)
    if (settings.value('save_position_geometry', 0)):
        ide.setMinimumSize(settings.value('ide_width', 700), settings.value('ide_height', 500))
    settings.value('confirm_exit', 2)
    settings.value('start_route','')
    settings.value('project_route','')
    settings.value('extra_plugins_route', '')
    settings.endGroup    #End General Settings

    #Interference Settings
    settings.beginGroup('Interface')
    settings.value('show_simbol_list', 2)
    settings.value('show_files_list',2)
    settings.value('editor_font',QFont("Sans Serif", 8.5))
    settings.value('simbol_list_font',QFont("Sans Serif", 8.5))
    settings.value('window_message_font',QFont("Sans Serif", 8.5))
    settings.value('show_editor_tabs', 2)
    settings.value('show_close_tabs', 2)
    settings.value('next_tabs_location',1)
    settings.value('hide_show_panels', 2)
    settings.value('editor_tab_position', 0)
    settings.value('lateral_bar_position', 0)
    settings.value('message_window_position', 0)
    settings.endGroup()#End Interface Settings
    settings.endGroup()

