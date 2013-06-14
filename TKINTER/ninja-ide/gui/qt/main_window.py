import sys

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QShortcut
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QSettings

from main_panel import Browser
from main_panel import factory_editor
from main_panel import ImageViewer
from display_panel import DisplayContainer
from properties_panel import PropertiesWidget
from gui.generic import MainWindowGeneric
from menus import WizardNewProject
from menus import PreferencesWindow
from tab_central_widget import TabCentralWidget
from central_widget import CentralWidget
import resources
from tools import runner
from tools import manage_files

class MainWindow(QWidget, MainWindowGeneric):

    def __init__(self, parent):
        QWidget.__init__(self)
        MainWindowGeneric.__init__(self)
        self._parent = parent
        self.settings = QSettings('NINJA-IDE','Kunai')

        self.settings.beginGroup('Preferences')
        self.settings.beginGroup('Interface')

        self._vbox = QVBoxLayout(self)
        #Splitters
        self.splitterMain = QSplitter()
        self.splitterCentral = QSplitter(Qt.Vertical)
        #Properties Panel
        self._properties = PropertiesWidget(self)
        #Central
        self._central = CentralWidget(self)
        self.show_start_page()
        self.splitterCentral.insertWidget(self.settings.value('central_tab_position', 0).toInt()[0], self._central)
        #Display Container
        self.container = DisplayContainer(self)
        self._hide_container()
        self.splitterCentral.insertWidget(self.settings.value('container_tab_position', 1).toInt()[0], self.container)
        height = [(self.height() / 3)*2,self.height() / 3]
        self.splitterCentral.setSizes([height[self.settings.value('central_tab_position', 0).toInt()[0]], height[self\
        .settings.value('container_tab_position', 1).toInt()[0]]])
        #Size Central Splitter
        self.splitterMain.insertWidget(self.settings.value('main_tab_position', 0).toInt()[0], self.splitterCentral)
        self.splitterMain.insertWidget(self.settings.value('properties_tab_position', 1).toInt()[0], self._properties)
        width = [(self.width() / 6)*5, self.width() / 6]
        self.splitterMain.setSizes([width[self.settings.value('main_tab_position', 0).toInt()[0]],\
         width[self.settings.value('properties_tab_position', 1).toInt()[0]]])
        self._vbox.addWidget(self.splitterMain)

        self.settings.endGroup()#End General Preferences
        self.settings.endGroup()

        #flag for reload_file
        self._reloading = False

        #Shortcuts
        shortCloseTab = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_W), self)
        shortNew = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_N), self)
        shortNewProject = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_J), self)
        shortOpen = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_O), self)
        shortOpenProject = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_P), self)
        shortSave = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_S), self)
        shortSaveAll = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_S), self)
        shortRedo = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Y), self)
        shortComment = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_D), self)
        shortHorizontalLine = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_R), self)
        shortIndentLess = QShortcut(QKeySequence(Qt.SHIFT + Qt.Key_Tab), self)
        shortHideContainer = QShortcut(QKeySequence(Qt.Key_F4), self)
        shortHideEditor = QShortcut(QKeySequence(Qt.Key_F3), self)
        shortHideExplorer = QShortcut(QKeySequence(Qt.Key_F2), self)
        shortRunFile = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F6), self)
        shortRunProgram = QShortcut(QKeySequence(Qt.Key_F6), self)
        shortHideAll = QShortcut(QKeySequence(Qt.Key_F11), self)
        shortFind = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F), self)
        shortFindReplace = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_H), self)
        shortHelp = QShortcut(QKeySequence(Qt.Key_F1), self)
        shortSplitHorizontal = QShortcut(QKeySequence(Qt.Key_F10), self)
        shortSplitVertical = QShortcut(QKeySequence(Qt.Key_F9), self)
        shortReloadFile = QShortcut(QKeySequence(Qt.Key_F5), self)
        #Signal -> Slot
        self.connect(shortCloseTab, SIGNAL("activated()"), self.close_actual_tab)
        self.connect(shortNew, SIGNAL("activated()"), self.new_editor)
        self.connect(shortNewProject, SIGNAL("activated()"), self.new_project)
        self.connect(shortOpen, SIGNAL("activated()"), self.open_file)
        self.connect(shortOpenProject, SIGNAL("activated()"), self.open_project_folder)
        self.connect(shortSave, SIGNAL("activated()"), self.save)
        self.connect(shortSaveAll, SIGNAL("activated()"), self.save_project)
        self.connect(shortComment, SIGNAL("activated()"), lambda: self._central.obtain_editor().comment())
        self.connect(shortIndentLess, SIGNAL("activated()"), lambda: self._central.obtain_editor().indent_less())
        self.connect(shortHorizontalLine, SIGNAL("activated()"), lambda: self._central.obtain_editor().insert_horizontal_line())
        self.connect(shortRedo, SIGNAL("activated()"), lambda: self._central.obtain_editor().redo())
        self.connect(shortHideContainer, SIGNAL("activated()"), self._hide_container)
        self.connect(shortHideEditor, SIGNAL("activated()"), self._hide_editor)
        self.connect(shortHideExplorer, SIGNAL("activated()"), self._hide_explorer)
        self.connect(shortRunFile, SIGNAL("activated()"), self._run_code)
        self.connect(shortRunProgram, SIGNAL("activated()"), self._run_program)
        self.connect(shortHideAll, SIGNAL("activated()"), self._hide_all)
        self.connect(shortFind, SIGNAL("activated()"), self._open_find)
        self.connect(shortFindReplace, SIGNAL("activated()"), self._open_find_replace)
        self.connect(shortHelp, SIGNAL("activated()"), self._show_python_doc)
        self.connect(shortSplitHorizontal, SIGNAL("activated()"), lambda: self.split_tab(True))
        self.connect(shortSplitVertical, SIGNAL("activated()"), lambda: self.split_tab(False))
        self.connect(shortReloadFile, SIGNAL("activated()"), lambda: self.reload_file())

    def change_window_title(self, title):
        self._parent.setWindowTitle('NINJA-IDE - ' + title)

    def _open_find(self):
        if not self._parent._status.isVisible():
            self._parent._status.show()
        self._parent._status.focus_find(self._central.obtain_editor())

    def _open_find_replace(self):
        if not self._parent._status.isVisible():
            self._parent._status.show()
        self._parent._status.replace_visibility(True)
        self._parent._status.focus_find(self._central.obtain_editor())

    def _hide_container(self):
        if self.containerIsVisible:
            self.container.hide()
            self.containerIsVisible = False
            self._central.obtain_editor().setFocus()
        else:
            self.container.show()
            self.containerIsVisible = True
            self.container.gain_focus()

    def _hide_editor(self):
        if self._central.isVisible():
            self._central.hide()
        else:
            self._central.show()

    def _hide_explorer(self):
        if self._properties.isVisible():
            self._properties.hide()
        else:
            self._properties.show()

    def _splitter_central_orientation(self):
        if self.splitterCentral.orientation() == Qt.Horizontal:
            self.splitterCentral.setOrientation(Qt.Vertical)
        else:
            self.splitterCentral.setOrientation(Qt.Horizontal)

    def get_splitter_central_orientation(self):
        return self.splitterCentral.orientation()

    def _splitter_main_orientation(self):
        if self.splitterMain.orientation() == Qt.Horizontal:
            self.splitterMain.setOrientation(Qt.Vertical)
        else:
            self.splitterMain.setOrientation(Qt.Horizontal)

    def get_splitter_main_orientation(self):
        return self.splitterMain.orientation()

    def _splitter_main_rotate(self):
        w = self.splitterMain.widget(0)
        w1 = self.splitterMain.widget(1)
        self.splitterMain.insertWidget(0, w1)
        self.splitterMain.insertWidget(1, w)

    def get_splitter_main_position(self):
        w = self.splitterMain.widget(0)
        return w.__class__

    def _splitter_central_rotate(self):
        w = self.splitterCentral.widget(0)
        w1 = self.splitterCentral.widget(1)
        self.splitterCentral.insertWidget(0, w1)
        self.splitterCentral.insertWidget(1, w)

    def get_splitter_central_position(self):
        w = self.splitterCentral.widget(0)
        return w.__class__

    def get_splitter_position_0(self):
        return type(self.splitterCentral.widget(0))

    def get_splitter_main_position_0(self):
        return type(self.splitterMain.widget(0))
    
    def reload_panels_position(self):
        self.settings = QSettings('NINJA-IDE','Kunai')

        self.settings.beginGroup('Preferences')
        self.settings.beginGroup('Interface')
        
        #first with the splitterCentral
        c = self.splitterCentral.widget(0)
        c1 = self.splitterCentral.widget(1)
        if (type(c) == CentralWidget):
            self.splitterCentral.insertWidget(self.settings.value('central_tab_position', 0).toInt()[0], c)
            self.splitterCentral.insertWidget(self.settings.value('container_tab_position', 1).toInt()[0], c1)
        else:
            self.splitterCentral.insertWidget(self.settings.value('central_tab_position', 0).toInt()[0], c1)
            self.splitterCentral.insertWidget(self.settings.value('container_tab_position', 1).toInt()[0], c)
        #now with the splitterMain
        m = self.splitterMain.widget(0)
        m1 = self.splitterMain.widget(1)
        if (type(m) == QSplitter):
            self.splitterMain.insertWidget(self.settings.value('central_tab_position', 0).toInt()[0], m)
            self.splitterMain.insertWidget(self.settings.value('container_tab_position', 1).toInt()[0], m1)
        else:
            self.splitterMain.insertWidget(self.settings.value('central_tab_position', 0).toInt()[0], m1)
            self.splitterMain.insertWidget(self.settings.value('container_tab_position', 1).toInt()[0], m)

    def get_open_projects(self):
        return self._properties._treeProjects.get_open_projects()

    def _run_code(self):
        if self.save():
            self.container.show()
            self.containerIsVisible = True
            editor = self._central.obtain_editor()
            ext = self.get_file_extension(editor.path)
            if ext == 'html':
                height = self.height() / 3
                self.splitterCentral.setSizes([height, height * 2])
                self.container.render_web_page(editor.path)
            elif ext == 'py':
                height = self.height() / 3
                self.splitterCentral.setSizes([height * 2, height])
                self.container.run_application(editor.path)
            else:
                self.execute_file(editor.path, ext)

    def _run_program(self, actual=None):
        self.container.show()
        self.containerIsVisible = True
        if actual is None:
            actual = self._properties._treeProjects.actualProject
        if actual is None:
            return
        mainFile = actual.mainFile
        if mainFile == '':
            self._properties._treeProjects.open_project_properties()
            self.containerIsVisible = False
            self.container.hide()
            return
        path = manage_files.create_abs_path(actual.path, mainFile)
        self._central.save_project_files(actual.path)
        lang = actual.lang()
        type_ = actual.projectType
        if lang == 'html':
            height = self.height() / 3
            self.splitterCentral.setSizes([height, height * 2])
            self.container.render_web_page(path)
        elif lang == 'py':
            height = self.height() / 3
            self.splitterCentral.setSizes([height * 2, height])
            self.container.run_application(path)
        else:
            self.execute_program(path, lang, type_)

    def _stop_program(self):
        self.container.kill_application()

    def _hide_all(self):
        if self._properties.isVisible():
            self._properties.hide()
            self.container.hide()
            self._parent._toolbar.hide()
        else:
            if self.containerIsVisible:
                self.container.show()
            self._properties.show()
            self._parent._toolbar.show()

    def show_start_page(self):
        startPage = Browser(resources.start_page_url)
        self.add_tab(startPage, 'Start Page')

    def show_report_bugs(self):
        bugsPage = Browser(resources.bugs_page)
        self.add_tab(bugsPage, 'Report Bugs!')

    def _show_python_doc(self):
        process = runner.start_pydoc()
        docPage = Browser(process[1], process[0])
        self.add_tab(docPage, 'Python Documentation')

    def new_editor(self, lang='py'):
        if not self._reloading:
            editor = factory_editor(lang, self._central.actual_tab())
            self.add_tab(editor, 'New Document')

    def add_tab(self, component, title):
        self._central.actual_tab().add_tab(component, title)

    def split_tab(self, option):
        if option:
            self._central.show_split(Qt.Horizontal)
        else:
            self._central.show_split(Qt.Vertical)

    def new_project(self):
        project = WizardNewProject(self)
        project.show()

    def show_preferences(self):
        prefs = PreferencesWindow(self)
        prefs.show()

    def open_document(self, fileName, project=None):
        try:
            if not self._central.actual_tab().is_open(fileName):
                self._central.actual_tab().notOpening = False
                editor = factory_editor(fileName, self._central.actual_tab(), project)
                content = self.read_file_content(fileName)
                editor.setPlainText(content)
                editor.path = fileName
                editor.ask_if_externally_modified = True
                #self.add_tab(editor, self.get_file_name(fileName))
                if not editor.has_write_permission():
                    fileName += ' (Read-Only)'
                self.add_tab(editor, self.get_file_name(fileName))
                self.change_window_title(fileName)
            else:
                self._central.actual_tab().move_to_open(fileName)
        except Exception, reason:
            print reason
            QMessageBox.information(self, 'Incorrect File', 'The file couldn\'t be open')
        self._central.actual_tab().notOpening = True

    def open_image(self, fileName):
        try:
            viewer = ImageViewer(fileName)
            self.add_tab(viewer, self.get_file_name(fileName))
        except Exception, reason:
            print reason
            QMessageBox.information(self, 'Incorrect File', 'The image couldn\'t be open')

    def open_file(self):
        fileName = str(QFileDialog.getOpenFileName(self, 'Open File', '', '(*.py);;(*.*)'))
        if not fileName:
            return
        try:
            self._central.actual_tab().notOpening = False
            content = self.read_file_content(fileName)
            editor = factory_editor(fileName, self._central.actual_tab())
            editor.setPlainText(content)
            editor.path = fileName
            #self.add_tab(editor, self.get_file_name(fileName))
            if not editor.has_write_permission():
                fileName += ' (Read-Only)'
            self.add_tab(editor, self.get_file_name(fileName))
            self.change_window_title(fileName)
        except Exception, reason:
            print reason
            QMessageBox.information(self, 'Incorrect File', 'The file does not exist!')
        self._central.actual_tab().notOpening = True

    def open_project_folder(self, folderName =''):
        if folderName =='':
            folderName = str(QFileDialog.getExistingDirectory(self, 'Open Project Directory'))
        try:
            self._properties._treeProjects.load_project(self.open_project(folderName), folderName)
        except Exception, reason:
            print reason
            QMessageBox.information(self, 'Incorrect File', 'The file does not exist!')

    def open_project_type(self, extensions):
        folderName = str(QFileDialog.getExistingDirectory(self, 'Open Project Directory'))
        try:
            self._properties._treeProjects.load_project(
                    self.open_project_with_extensions(folderName, extensions), folderName)
        except Exception, reason:
            print reason
            QMessageBox.information(self, 'Incorrect File', 'The file does not exist!')

    def close_actual_tab(self):
        self._central.actual_tab().removeTab(self._central.actual_tab().currentIndex())

    def reload_file(self):
        editor = self._central.obtain_editor()
        if not editor.newDocument:
            fileName = editor.path
            #Hey IGNORE SIGNAL("allTabsClosed()") this time!
            self._reloading = True
            self.close_actual_tab()
            self.open_document(fileName)
            self._reloading = False

    def save(self):
        editor = self._central.obtain_editor()
        try:
            if editor.newDocument or not editor.has_write_permission():
                return self.save_as()
            
            fileName = editor.path
            fileName = self.store_file_content(fileName, editor.get_text())
            self._central.actual_tab().setTabText(self._central.actual_tab().currentIndex(), 
                self.get_file_name(fileName))
            editor.register_syntax(fileName)
            self.change_window_title(fileName)
            editor.path = fileName
            self._central.actual_tab().mark_as_saved()
            editor.ask_if_externally_modified = True
            self.emit(SIGNAL("fileSaved(QString)"), 'File Saved: ' + fileName)
            return True
        except Exception, reason:
            print reason
            QMessageBox.information(self, 'Save Error', "The file couldn't be saved!")
            return False

    def save_project(self):
        actual = self._properties._treeProjects.actualProject
        if actual is None:
            return
        self._central.save_project_files(actual.path)

    def save_as(self):
        editor = self._central.obtain_editor()
        try:
            fileName = str(QFileDialog.getSaveFileName(self, 'Save File', '', '(*.py);;(*.*)'))
            if not fileName:
                return
            
            fileName = self.store_file_content(fileName, editor.get_text())
            self._central.actual_tab().setTabText(self._central.actual_tab().currentIndex(), 
                                                        self.get_file_name(fileName))
            editor.register_syntax(fileName)
            editor.path = fileName
            self.change_window_title(fileName)
            self._central.actual_tab().mark_as_saved()
            self.emit(SIGNAL("fileSaved(QString)"), 'File Saved: ' + fileName)
            return fileName
        except Exception, reason:
            print reason
            QMessageBox.information(self, 'Save Error', "The file couldn't be saved!")
            self._central.actual_tab().setTabText(self._central.actual_tab().currentIndex(), 'New Document')
        return None

    def _update_window_name(self):
        editor = self._central.obtain_editor()
        if editor is not None:
            self.change_window_title(editor.path)
