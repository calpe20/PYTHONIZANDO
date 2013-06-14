import os

from PyQt4.QtGui import QTreeWidget
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QCursor
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QBrush
from PyQt4.QtGui import QColor
from PyQt4.QtCore import QStringList
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QHeaderView
from PyQt4 import uic

import rope.base.project

import resources
from gui.generic.properties_panel import Project
from tools import runner
from tools import loader
from tools import manage_files
#from tools import introspection
from project_properties import ProjectProperties

class TreeProjectsWidget(QTreeWidget):

    images = {
        '.py':resources.images['tree-python'],
        '.java':resources.images['tree-java'],
        '.fn':resources.images['tree-code'],
        '.c':resources.images['tree-code'],
        '.cs':resources.images['tree-code'],
        '.jpg':resources.images['tree-image'],
        '.png':resources.images['tree-image'],
        '.html':resources.images['tree-html'],
        '.css':resources.images['tree-css'],
        '.ui':resources.images['designer']
        }

    def __init__(self, main):
        QTreeWidget.__init__(self)
        self.header().setHidden(True)
        self.setSelectionMode(self.SingleSelection)
        self.setAnimated(True)
        self._main = main
        self.extraMenus = {}
        self.actualProject = None
        self.projects = {}
        
        self.header().setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.header().setResizeMode(0, QHeaderView.ResizeToContents)
        self.header().setStretchLastSection(False)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self, SIGNAL("customContextMenuRequested(const QPoint &)"), self.menuContextTree)
        self.connect(self, SIGNAL("itemClicked(QTreeWidgetItem *, int)"), self._open_file)

    def menuContextTree(self, point):
        index = self.indexAt(point)
        if not index.isValid():
            return

        item = self.itemAt(point)
        name = item.text(0)

        menu=QMenu(self)
        if item.isFolder or item.parent() is None:
            action_add_file = menu.addAction(QIcon(resources.images['new']), 'Add New File')
            self.connect(action_add_file, SIGNAL("triggered()"), self._add_new_file)
            action_add_folder = menu.addAction(QIcon(resources.images['openProj']), 'Add New Folder')
            self.connect(action_add_folder, SIGNAL("triggered()"), self._add_new_folder)
            action_create_init = menu.addAction('Create "__init__" Complete')
            self.connect(action_create_init, SIGNAL("triggered()"), self._create_init)
        elif not item.isFolder:
            action_remove_file = menu.addAction(self.style().standardIcon(QStyle.SP_DialogCloseButton),
                'Delete File')
            self.connect(action_remove_file, SIGNAL("triggered()"), self._delete_file)
#            action_load_symbols = menu.addAction(self.style().standardIcon(QStyle.SP_DialogCloseButton),
#                'Load Symbols')
#            self.connect(action_load_symbols, SIGNAL("triggered()"), self._load_file_symbols)
        if item.parent() is None:
            menu.addSeparator()
            actionRunProject = menu.addAction(QIcon(resources.images['play']), 'Run Project')
            self.connect(actionRunProject, SIGNAL("triggered()"), self.run_project)
            actionMainProject = menu.addAction('Set as Main Project')
            self.connect(actionMainProject, SIGNAL("triggered()"), lambda: self.set_default_project(item))
            actionProperties = menu.addAction(QIcon(resources.images['pref']), 'Project Properties')
            self.connect(actionProperties, SIGNAL("triggered()"), self.open_project_properties)
            if self.extraMenus.get(item.projectType, False):
                menus = self.extraMenus[item.projectType]
                for m in menus:
                    menu.addSeparator()
                    menu.addMenu(m)
            if self.extraMenus.get(item.lang(), False):
                menus = self.extraMenus[item.lang()]
                for m in menus:
                    menu.addSeparator()
                    menu.addMenu(m)
            menu.addSeparator()
            action_refresh = menu.addAction(self.style().standardIcon(QStyle.SP_BrowserReload), 
                'Refresh Project')
            self.connect(action_refresh, SIGNAL("triggered()"), self._refresh_project)
            action_close = menu.addAction(self.style().standardIcon(QStyle.SP_DialogCloseButton), 
                'Close Project')
            self.connect(action_close, SIGNAL("triggered()"), self._close_project)
        menu.exec_(QCursor.pos())

    def run_project(self):
        item = self.currentItem()
        self._main._run_program(item)

    def set_default_project(self, item):
        item.setForeground(0, QBrush(QColor(0, 204, 82)))
        self.actualProject = item
        for i in self.projects:
            if i is not item:
                i.setForeground(0, QBrush(Qt.darkGray))

    def open_project_properties(self):
        item = self.currentItem()
        while item.parent() is not None:
            item = item.parent()
        proj = ProjectProperties(self, item)
        proj.show()

    def _refresh_project(self, item=None):
        if item is None:
            item = self.currentItem()
        while item.parent() is not None:
            item = item.parent()
        item.takeChildren()
        if item.extensions != manage_files.supported_extensions:
            folderInfo = self._main.open_project_with_extensions(item.path, item.extensions)
        else:
            folderInfo = self._main.open_project(item.path)
        self.dicFolder = folderInfo
        if self.dicFolder[item.path][1] is not None: self.dicFolder[item.path][1].sort()
        self.load_folder(item, item.path)

    def _close_project(self):
        item = self.currentItem()
        index = self.indexOfTopLevelItem(item)
        myproject = self.projects.pop(item)
        myproject.close()
        self.takeTopLevelItem(index)

    def _create_init(self):
        item = self.currentItem()
        if item.parent() is None:
            pathFolder = item.path
        else:
            pathFolder = os.path.join(item.path, str(item.text(0)))
        manage_files.create_init_file_complete(pathFolder)
        self._refresh_project()

    def _add_new_file(self):
        item = self.currentItem()
        if item.parent() is None:
            pathForFile = item.path
        else:
            pathForFile = os.path.join(item.path, str(item.text(0)))
        result = QInputDialog.getText(self, 'New File', 'Enter the File Name:')
        fileName = str(result[0])

        if result[1] and fileName.strip() != '':
            fileName = os.path.join(pathForFile, fileName)
            fileName = self._main.store_file_content(fileName, '')
            name = os.path.basename(fileName)
            subitem = ItemTree(item, QStringList(name), pathForFile)
            subitem.setToolTip(0, name)
            subitem.setIcon(0, self.obtain_icon(name))
            item.sortChildren(0, Qt.AscendingOrder)
            self._main.open_document(fileName)

    def _add_new_folder(self):
        item = self.currentItem()
        if item.parent() is None:
            pathForFolder = item.path
        else:
            pathForFolder = os.path.join(item.path, str(item.text(0)))
        result = QInputDialog.getText(self, 'New Folder', 'Enter the Folder Name:')
        folderName = str(result[0])

        if result[1] and folderName.strip() != '':
            folderName = os.path.join(pathForFolder, folderName)
            manage_files.create_folder(folderName)
            item.setSelected(False)
            while item.parent() is not None:
                item = item.parent()
            item.setSelected(True)
            self._refresh_project()

    def _delete_file(self):
        item = self.currentItem()
        val = QMessageBox.question(self, 'Delete File',
                'Do you want to delete the following file: '\
                + item.path, QMessageBox.Yes, QMessageBox.No)
        if val == QMessageBox.Yes:
            manage_files.delete_file(item.path, str(item.text(0)))
            self.removeItemWidget(item, 0)

    def _load_file_symbols(self):
        item = self.currentItem()
        module = introspection.load_module(item.path, str(item.text(0)[:-3]))
        for class_info in introspection.get_classes_and_methods(module):
            class_item = ItemTree(item, QStringList(class_info['name']), item.path)
            class_item.setToolTip(0, class_info['name'])
            for method_info in class_info['methods']:
                method_item =  ItemTree(class_item, QStringList(method_info['name']), item.path)
                method_item.setToolTip(0, method_info['name'])

    def load_project(self, folderInfo, folder):
        self.dicFolder = folderInfo
        if folder == '': return

        name = os.path.basename(folder)
        item = ItemProjectTree(self, QStringList(name), folder)
        item.isFolder = True
        item.setToolTip(0, name)
        item.setIcon(0, QIcon(resources.images['tree-app']))
        myproject = rope.base.project.Project(folder, None, '.ninjaproject')
        self.projects[item] = myproject
        if self.dicFolder[folder][1] is not None: self.dicFolder[folder][1].sort()
        if item.extensions != manage_files.supported_extensions:
            self.dicFolder = self._main.open_project_with_extensions(item.path, item.extensions)
        self.load_folder(item, folder)
        item.setExpanded(True)
        if len(self.projects) == 1:
            self.set_default_project(item)
        if self.currentItem() is None:
            item.setSelected(True)
            self.setCurrentItem(item)

    def load_folder(self, parent, folder):
        items = self.dicFolder[folder]
        
        if items[0] is not None: items[0].sort()
        for i in items[0]:
            subitem = ItemTree(parent, QStringList(i), folder)
            subitem.setToolTip(0, i)
            subitem.setIcon(0, self.obtain_icon(i))
        if items[1] is not None: items[1].sort()
        for f in items[1]:
            if f.startswith('.'): continue
            subfolder = ItemTree(parent, QStringList(f), folder)
            subfolder.isFolder = True
            subfolder.setToolTip(0, f)
            subfolder.setIcon(0, QIcon(resources.images['tree-folder']))
            self.load_folder(subfolder, os.path.join(folder, f))

    def obtain_icon(self, fileName):
        return QIcon(self.images.get(manage_files.get_file_extension(fileName), resources.images['tree-generic']))

    def _open_file(self, item, val):
        if item.childCount() == 0 and not item.isFolder:
            fileName = os.path.join(item.path, str(item.text(val)))
            if (manage_files.get_file_extension(fileName)) in ('.jpg', '.png'):
                self._main.open_image(fileName)
            elif (manage_files.get_file_extension(fileName)).endswith('.ui'):
                self.w = uic.loadUi(fileName)
                self.w.show()
            else:
                while item.parent() is not None:
                    item = item.parent()
                self._main.open_document(fileName, self.projects[item])

    def get_selected_project_path(self):
        return self.currentItem().path

    def get_selected_project_lang(self):
        return self.currentItem().lang()

    def get_open_projects(self):
        return [p.path for p in self.projects]

    def close_open_projects(self):
        for p in self.projects:
            proj = self.projects[p]
            proj.close()

    def keyPressEvent(self, event):
        item = self.currentItem()
        self._open_file(item, 0)
        super(TreeProjectsWidget, self).keyPressEvent(event)


class ItemTree(QTreeWidgetItem):

    def __init__(self, parent, name, path):
        QTreeWidgetItem.__init__(self, parent, name)
        self.path = path
        self.isFolder = False


class ItemProjectTree(QTreeWidgetItem, Project):

    def __init__(self, parent, name, path):
        QTreeWidgetItem.__init__(self, parent, name)
        Project.__init__(self)
        self._parent = parent
        self.path = path
        self.isFolder = False
        self.setForeground(0, QBrush(Qt.darkGray))
        project = loader.read_ninja_project(path)
        self.name = project.get('name', '')
        if self.name != '':
            self.setText(0, self.name)
        self.projectType = project.get('project-type', '')
        self.description = project.get('description', '')
        self.url = project.get('url', '')
        self.license = project.get('license', '')
        self.mainFile = project.get('mainFile', '')
        self.extensions = project.get('supported-extensions', manage_files.supported_extensions)

    def lang(self):
        if self.mainFile != '':
            return manage_files.get_file_extension(self.mainFile)[1:]
