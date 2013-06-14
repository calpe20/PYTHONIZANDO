css_styles = {
    'editor':'''
        QPlainTextEdit {
          font-family: monospace;
          font-size: 10;
          color: black;
          background-color: white;
          selection-color: white;
          selection-background-color: #437DCD;
        }''',

    'menu':"""
        QMenuBar {
         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
             stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
             stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
         border-style: solid;
         border-width: 1px;
         color: darkgray;
         }
        QMenu {
         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
             stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
             stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
         color: #6E6E6E;
         }
        """,

    'toolbar':"""
        QToolBar {
         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
             stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
             stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
         border-radius: 10px;
         border-style: solid;
         border-width: 1px;
         color: darkgray;
         }
        """,

    'toolbar-default':"""
        QToolBar::separator {
         border-radius: 10px;
         background: gray;
         width: 2px; /* when vertical */
         height: 2px; /* when horizontal */
         }
        """,

    'ide':"""
        IDE {
         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
             stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
             stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
         }
        """,

    'tree':"""
        QTreeWidget {
         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
             stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
             stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
         border-radius: 10px;
         border-style: solid;
         border-width: 1px;
         color: black;
         }
        """
}

enable_css = False

def apply(widget, sty):
    css = css_styles.get(sty, '')
    if enable_css and css != '':
        widget.setStyleSheet(css)

def set_style(widget, sty):
    css = css_styles.get(sty, '')
    widget.setStyleSheet(css)