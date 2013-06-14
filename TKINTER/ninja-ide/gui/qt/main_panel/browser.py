import time

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView
from PyQt4.QtWebKit import QWebPage
from PyQt4.QtCore import QThread

from gui.generic import BaseCentralWidget
import resources

class Browser (QWidget, BaseCentralWidget):

    def __init__(self, URL, process=None):
        QWidget.__init__(self)
        BaseCentralWidget.__init__(self)
        self.path = URL
        self.process = process
        
        v_box = QVBoxLayout(self)
        #Web Frame
        self.webFrame = QWebView()
        self.webFrame.load(QUrl(URL))
        
        v_box.addWidget(self.webFrame)

        if process is not None:
            time.sleep(0.5)
            self.webFrame.reload()

    def shutdown_pydoc(self):
        if self.process is not None:
            self.process.kill()

    def find_match(self, word, back=False, sensitive=False, whole=False):
        b = QWebPage.FindBackward if back else None
        s = QWebPage.FindCaseSensitively if sensitive else None
        self.webFrame.page().findText(word)