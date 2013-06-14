from PyQt4.QtGui import QAction
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL

from about_ninja import AboutNinja

class MenuAbout(object):

    def __init__(self, menu, main):
        self._main = main

        startPageAction = menu.addAction('Show Start Page')
        helpAction = menu.addAction('Python Help (F1)')
        reportBugAction = menu.addAction('Report Bugs!')
        menu.addSeparator()
        aboutNinjaAction = menu.addAction('About NINJA-IDE')
        aboutQtAction = menu.addAction('About Qt')

        QObject.connect(startPageAction, SIGNAL("triggered()"), self._main.show_start_page)
        QObject.connect(reportBugAction, SIGNAL("triggered()"), self._main.show_report_bugs)
        QObject.connect(aboutQtAction, SIGNAL("triggered()"), self._show_about_qt)
        QObject.connect(helpAction, SIGNAL("triggered()"), self._main._show_python_doc)
        QObject.connect(aboutNinjaAction, SIGNAL("triggered()"), self._show_about_ninja)

    def _show_about_qt(self):
        QMessageBox.aboutQt(self._main, 'About Qt')

    def _show_about_ninja(self):
        self.about = AboutNinja()
        self.about.show()