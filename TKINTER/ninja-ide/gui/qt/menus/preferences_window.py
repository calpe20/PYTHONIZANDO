import sys

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QRadioButton
from PyQt4.QtGui import QFontDialog
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QSplitter
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import QSize

from gui.qt.central_widget import CentralWidget
import resources

class PreferencesWindow (QDialog):


    def __init__(self, parent):
        QDialog.__init__(self, parent, Qt.Dialog)
        self.setWindowTitle('NINJA - Preferences')
        self.setMaximumSize(QSize(0,0))
        self.setModal(True)
        main_box = QVBoxLayout(self)

        self.GeneralTab = TabGeneral()
        self.EditTab = TabEdit()
        self.ColorsTab = TabColors()
        self.InterfaceTab = TabInterface(parent)
        self.CSSTab = TabCSS()
        self.TemplatesTab = TabTemplates()
        self.Tabs = QTabWidget()
        self.Tabs.setTabPosition(2)
        self.Tabs.setMovable(False)
        #Tabs
        self.Tabs.addTab(self.GeneralTab, "General")
        #self.Tabs.addTab(self.EditTab, "Edit")
        #self.Tabs.addTab(self.ColorsTab, "Colors")
        self.Tabs.addTab(self.InterfaceTab, "Interface")
        #self.Tabs.addTab(self.CSSTab, "CSS")
        #self.Tabs.addTab(self.TemplatesTab, "Templates")

        #Footer Buttons
        self.btn_save = QPushButton('&Save')
        self.btn_cancel = QPushButton('&Cancel')

        h_footer = QHBoxLayout()
        h_footer.addWidget(self.btn_save)
        h_footer.addWidget(self.btn_cancel)

        g_footer = QGridLayout()
        g_footer.addLayout(h_footer, 0, 0, Qt.AlignRight)

        main_box.addWidget(self.Tabs)
        main_box.addLayout(g_footer)

        def save_changes():
            self.GeneralTab.save_state()
            self.InterfaceTab.save_state(parent)

            self.close()

        def cancel_changes():
            parent.reload_panels_position()
            self.close()

        #SIGNAL
        self.connect(self.btn_cancel, SIGNAL("clicked()"), cancel_changes)
        self.connect(self.btn_save, SIGNAL("clicked()"), save_changes)

class TabGeneral(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        v_box = QVBoxLayout(self)
        self.setFixedWidth(500)
        self.settings = QSettings('NINJA-IDE','Kunai')

        
        #Groups
        self.gbox_Home = QGroupBox('On Start:')
        self.gbox_Close = QGroupBox("On Close:")
        self.gbox_Routes = QGroupBox('Routes:')

        v_box.addWidget(self.gbox_Home)
        v_box.addWidget(self.gbox_Close)
        v_box.addWidget(self.gbox_Routes)

        self.settings.beginGroup('Preferences')
        self.settings.beginGroup('General')
        #Home
        #Layout
        v_home = QVBoxLayout()
        ##CheckBox
        self.ch_lastSesionFiles = QCheckBox('Load files from last session.')
        self.ch_lastSesionFiles.setCheckState(self.settings.value('load_files', 2).toInt()[0])
        self.ch_activatePlugins = QCheckBox('Activate Plugins.')
        self.ch_activatePlugins.setCheckState(self.settings.value('activate_plugins', 2).toInt()[0])
        self.ch_notifyUpdates = QCheckBox('Nofity me for new available updates.')
        self.ch_notifyUpdates.setCheckState(self.settings.value('notify_updates', 0).toInt()[0])
        v_home.addWidget(self.ch_lastSesionFiles)
        v_home.addWidget(self.ch_activatePlugins)
        v_home.addWidget(self.ch_notifyUpdates)
        self.gbox_Home.setLayout(v_home)

        #Close
        #Layout
        v_close = QVBoxLayout()
        ##CheckBox
        self.ch_saveState = QCheckBox('Save the window position and geometry.')
        self.ch_saveState.setCheckState(self.settings.value('save_position_geometry', 0).toInt()[0])
        self.ch_confirmExit = QCheckBox('Confirm Exit.')
        self.ch_confirmExit.setCheckState(self.settings.value('confirm_exit', 2).toInt()[0])
        v_close.addWidget(self.ch_saveState)
        v_close.addWidget(self.ch_confirmExit)
        self.gbox_Close.setLayout(v_close)

        #Routes
        #Layout
        g_routes = QGridLayout()
        ##TextBox
        self.txt_startRoute = QLineEdit()
        self.txt_startRoute.setText(self.settings.value('start_route','').toString())
        self.txt_projectRoute = QLineEdit()
        self.txt_projectRoute.setText(self.settings.value('project_route','').toString())
        self.txt_xtraPlugins = QLineEdit()
        self.txt_xtraPlugins.setText(self.settings.value('extra_plugins_route','').toString())
        ##Button
        self.btn_startRoute = QPushButton(QIcon(resources.images['openFolder']),'')
        self.btn_projectRoute = QPushButton(QIcon(resources.images['openFolder']),'')
        self.btn_xtraPlugins = QPushButton(QIcon(resources.images['openFolder']),'')

        

        def load_start_route():
            self.txt_startRoute.setText(load_directory(self, 'Start Route'))
        def load_project_route():
            self.txt_projectRoute.setText(load_directory(self, 'Project Route'))
        def load_xtra_plugins_route():
            self.txt_xtraPlugins.setText(load_directory(self, 'Extra Plugins Route'))
        
        
        self.settings.endGroup()#End General Preferences
        self.settings.endGroup()
        
        #Signal
        self.connect(self.btn_startRoute, SIGNAL('clicked()'), load_start_route)
        self.connect(self.btn_projectRoute, SIGNAL('clicked()'), load_project_route)
        self.connect(self.btn_xtraPlugins, SIGNAL('clicked()'), load_xtra_plugins_route)

        g_routes.addWidget(QLabel('Start Route:'), 0, 0, Qt.AlignRight)
        g_routes.addWidget(QLabel('Project Files:'), 1, 0, Qt.AlignRight)
        #g_routes.addWidget(QLabel('Extra Plugins Route:'), 2, 0, Qt.AlignRight)
        g_routes.addWidget(self.txt_startRoute, 0, 1)
        g_routes.addWidget(self.txt_projectRoute, 1, 1)
        #g_routes.addWidget(self.txt_xtraPlugins, 2 ,1)
        g_routes.addWidget(self.btn_startRoute, 0,2)
        g_routes.addWidget(self.btn_projectRoute, 1,2)
        #g_routes.addWidget(self.btn_xtraPlugins, 2, 2)

        self.gbox_Routes.setLayout(g_routes)
        
    def save_state(self):
            self.settings.beginGroup('Preferences')
            self.settings.beginGroup('General')

            #CheckBox
            self.settings.setValue('load_files', self.ch_lastSesionFiles.checkState())
            self.settings.setValue('activate_plugins', self.ch_activatePlugins.checkState())
            self.settings.setValue('save_position_geometry', self.ch_saveState.checkState())
            self.settings.setValue('confirm_exit', self.ch_confirmExit.checkState())
            self.settings.setValue('notify_updates', self.ch_notifyUpdates.checkState())

            #TextBox
            self.settings.setValue('start_route', self.txt_startRoute.text())
            self.settings.setValue('project_route', self.txt_projectRoute.text())
            self.settings.setValue('extra_plugins_route', self.txt_xtraPlugins.text())
            
            self.settings.endGroup()#End General Preferences
            self.settings.endGroup()

class TabEdit(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        v_box = QVBoxLayout(self)
        self.setFixedWidth(500)

class TabColors(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        v_box = QVBoxLayout(self)
        self.setFixedWidth(500)

class TabCSS(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        v_box = QVBoxLayout(self)
        self.setFixedWidth(500)

class TabInterface(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        v_box = QVBoxLayout(self)
        self.setFixedWidth(500)
        self.settings = QSettings('NINJA-IDE','Kunai')

        #groups
        self.gbox_bars = QGroupBox('Lateral Bars:')
        self.gbox_fonts = QGroupBox('Fonts:')
        self.gbox_tabs = QGroupBox('Editor Tabs:')
        self.gbox_tabsPosition = QGroupBox('Tabs Position:')
        
        v_box.addWidget(self.gbox_bars)
        v_box.addWidget(self.gbox_fonts)
        v_box.addWidget(self.gbox_tabs)
        v_box.addWidget(self.gbox_tabsPosition)

        self.settings.beginGroup('Preferences')
        self.settings.beginGroup('Interface')
        
        #Lateral Bars
        ##Checks
        self.ch_simbols = QCheckBox('Show Simbols List.')
        self.ch_simbols.setCheckState(self.settings.value('show_simbol_list', 2).toInt()[0])
        self.ch_files = QCheckBox('Show Files List.')
        self.ch_files.setCheckState(self.settings.value('show_files_list', 2).toInt()[0])

        v_bars = QVBoxLayout()
        v_bars.addWidget(self.ch_simbols)
        v_bars.addWidget(self.ch_files)

        self.gbox_bars.setLayout(v_bars)

        
        #Buttons
        self.btn_editor_font = QPushButton(self.settings.value('editor_font','Monospace, 10').toString())
        #self.btn_simbol_font = QPushButton(self.settings.value('simbol_list_font','Monospace, 10').toString())
        #self.btn_message_font = QPushButton(self.settings.value('window_message_font','Monospace, 10').toString())

        def load_editor_font():
            self.btn_editor_font.setText(load_font(self, self.get_font_from_string(self.btn_editor_font.text())))

        def load_simbol_font():
            self.btn_simbol_font.setText(load_font())

        def load_message_font():
            self.btn_message_font.setText(load_font())

        
        #SIGNALS
        self.connect(self.btn_editor_font, SIGNAL("clicked()"), load_editor_font)
        #self.connect(self.btn_simbol_font, SIGNAL ("clicked()"), load_simbol_font)
        #self.connect(self.btn_message_font, SIGNAL("clicked()"), load_message_font)

        g_font = QGridLayout()
        g_font.addWidget(QLabel('Editor Font:'), 0,0,Qt.AlignRight)
        #g_font.addWidget(QLabel('Simbol List:'),1, 0, Qt.AlignRight)
        #g_font.addWidget(QLabel('Messages Window:'),2,0,Qt.AlignRight)
        g_font.addWidget(self.btn_editor_font, 0,1)
        #g_font.addWidget(self.btn_simbol_font, 1, 1)
        #g_font.addWidget(self.btn_message_font, 2, 1)

        self.gbox_fonts.setLayout(g_font)

        #Edition Tabs
        #Checks
        self.ch_showEditTabs = QCheckBox('Show Editor Tabs')
        self.ch_showEditTabs.setCheckState(self.settings.value('show_editor_tabs', 2).toInt()[0])
        self.ch_showClose = QCheckBox('Show Close Button on Tabs')
        self.ch_showClose.setCheckState(self.settings.value('show_close_tabs', 2).toInt()[0])
        self.ch_hidePanel = QCheckBox('F11 hide/show side Panels')
        self.ch_hidePanel.setCheckState(self.settings.value('hide_show_panels', 2).toInt()[0])
        
        #Option
        self.opt_left = QRadioButton('Left')
        self.opt_right =QRadioButton('Right')
        if (self.settings.value('next_tabs_location', 1).toInt()[0] == 1):
            self.opt_right.setChecked(True)
        else:
            self.opt_left.setChecked(True)
        h_optionNewFiles = QHBoxLayout()
        h_optionNewFiles.addWidget(QLabel('Location for New Files Tabs'))
        h_optionNewFiles.addWidget(self.opt_left)
        h_optionNewFiles.addWidget(self.opt_right)

        v_tabs = QVBoxLayout()
        v_tabs.addWidget(self.ch_showEditTabs)
        v_tabs.addWidget(self.ch_showClose)
        v_tabs.addLayout(h_optionNewFiles)
        #v_tabs.addWidget(self.ch_hidePanel)

        self.gbox_tabs.setLayout(v_tabs)

        #Tabs Position
        #Buttons
        #self.btn_orientation_change = QPushButton
        self.btn_hchange = QPushButton(QIcon(resources.images['splitCRotate']),'')
        self.btn_hchange.setIconSize(QSize(64,64))
        self.btn_right_vchange = QPushButton(QIcon(resources.images['splitMRotate']),'')
        self.btn_right_vchange.setIconSize(QSize(64,64))

        #SIGNAL
        self.connect(self.btn_hchange, SIGNAL('clicked()'), parent._splitter_central_rotate)
        self.connect(self.btn_right_vchange, SIGNAL('clicked()'), parent._splitter_main_rotate)
        
        self.settings.endGroup()#End General Preferences
        self.settings.endGroup()
        
        g_tabPosition = QGridLayout()
        g_tabPosition.addWidget(self.btn_hchange, 0,0)
        g_tabPosition.addWidget(self.btn_right_vchange, 0, 1)
        g_tabPosition.addWidget(QLabel('Vertical Change'),1,0, Qt.AlignCenter)
        g_tabPosition.addWidget(QLabel('Horizontal Change'),1,1, Qt.AlignCenter)
        

        self.gbox_tabsPosition.setLayout(g_tabPosition)

#Fonts
    def get_font_from_string(self, font):
        if (font.isEmpty()):
            return QFont("Monospace", 10)
        
        listFont = font.remove(' ').split(',')
        ret = QFont(listFont[0], listFont[1].toInt()[0])
        return ret

        
    def save_state(self, parent):
        
        self.settings.beginGroup('Preferences')
        self.settings.beginGroup('Interface')
        #CheckBox
        self.settings.setValue('show_simbol_list', self.ch_simbols.checkState())
        self.settings.setValue('show_files_list', self.ch_files.checkState())
        self.settings.setValue('show_editor_tabs', self.ch_showEditTabs.checkState())
        self.settings.setValue('show_close_tabs', self.ch_showClose.checkState())
        self.settings.setValue('hide_show_panels', self.ch_hidePanel.checkState())
        #OptionButton
        if (self.opt_right.isChecked()):
            self.settings.setValue('next_tabs_location', 1)
        else:
            self.settings.setValue('next_tabs_location', 0)
        #Fonts
        self.settings.setValue('editor_font', self.btn_editor_font.text())
        #self.settings.setValue('simbol_list_font', self.btn_simbol_font.text())
        #self.settings.setValue('window_message_font', self.btn_message_font.text())

        #Panels Positions
        if (parent.get_splitter_position_0() == CentralWidget):
            self.settings.setValue('central_tab_position', 0)
            self.settings.setValue('container_tab_position', 1)
        else:
            self.settings.setValue('central_tab_position', 1)
            self.settings.setValue('container_tab_position', 0)

        if (parent.get_splitter_main_position_0() == QSplitter):
            self.settings.setValue('main_tab_position', 0)
            self.settings.setValue('properties_tab_position', 1)
        else:
            self.settings.setValue('main_tab_position', 1)
            self.settings.setValue('properties_tab_position', 0)
        
        self.settings.endGroup()#End Interface Preferences
        self.settings.endGroup()


class TabTemplates(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        v_box = QVBoxLayout(self)
        self.setFixedWidth(500)

def load_font(self, initialFont):
    print initialFont.key()
    font, ok = QFontDialog(initialFont).getFont()
    if ok:
        newFont = font.toString().split(',')
        return newFont[0]+', '+newFont[1]
    else:
        return initialFont



def load_directory(self, Title):
    return str(QFileDialog.getExistingDirectory(self, Title))