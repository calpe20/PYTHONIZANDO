from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QLabel
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize

import resources

class AboutNinja(QDialog):
    
    def __init__(self):
        QDialog.__init__(self, None, Qt.Dialog)
        self.setModal(True)
        self.setWindowTitle('About NINJA-IDE')
        self.setMaximumSize(QSize(0,0))
        v_box = QVBoxLayout(self)
        
        pixmap = QPixmap(resources.images['icon'])
        labIcon = QLabel('')
        labIcon.setPixmap(pixmap)
        hbox = QHBoxLayout()
        hbox.addWidget(labIcon)
        lblTitle = QLabel('<h1>NINJA-IDE</h1>\n<i>Ninja Is Not Just Another IDE<i>')
        lblTitle.setTextFormat(Qt.RichText)
        lblTitle.setAlignment(Qt.AlignLeft)
        hbox.addWidget(lblTitle)
        v_box.addLayout(hbox)
        v_box.addWidget(QLabel("""NINJA is an IDE specialy Designed for Python applications development.
In the Version 1.0, also called Kunai, will be included the next features:
    Autocompleting Code, Code Checking, Projects Management,
    Wizard Interfaces for creating new files and also new projects,
    an interactive Python console,
    an easter egg (essencial in any application),
    and much more!."""))
        v_box.addWidget(QLabel('Version: UNDER DEVELOPMENT'))
        v_box.addWidget(QLabel('Website: http://ninja-ide.googlecode.com'))