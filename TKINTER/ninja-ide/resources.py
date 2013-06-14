#-*-coding:utf-8-*-

import os, sys


OS_VERSION = sys.version
OS_KEY =  'Cmd' if 'Apple' in OS_VERSION else 'Ctrl'

PRJ_PATH = os.path.abspath(os.path.dirname(__file__))

createpath = os.path.join

images = {
    'splash': os.path.join(PRJ_PATH, 'img', 'splash.png'),
    'icon': os.path.join(PRJ_PATH, 'img', 'icon.png'),
    'new': os.path.join(PRJ_PATH, 'img', 'document-new.png'),
    'newProj': os.path.join(PRJ_PATH, 'img', 'project-new.png'),
    'open': os.path.join(PRJ_PATH, 'img', 'document-open.png'),
    'openProj': os.path.join(PRJ_PATH, 'img', 'project-open.png'),
    'openFolder': os.path.join(PRJ_PATH, 'img', 'folder-open.png'),
    'save': os.path.join(PRJ_PATH, 'img', 'document-save.png'),
    'saveAs': os.path.join(PRJ_PATH, 'img', 'document-save-as.png'),
    'saveAll': os.path.join(PRJ_PATH, 'img', 'document-save-all.png'),
    'copy': os.path.join(PRJ_PATH, 'img', 'edit-copy.png'),
    'cut': os.path.join(PRJ_PATH, 'img', 'edit-cut.png'),
    'paste': os.path.join(PRJ_PATH, 'img', 'edit-paste.png'),
    'redo': os.path.join(PRJ_PATH, 'img', 'edit-redo.png'),
    'undo': os.path.join(PRJ_PATH, 'img', 'edit-undo.png'),
    'find': os.path.join(PRJ_PATH, 'img', 'find.png'),
    'findReplace': os.path.join(PRJ_PATH, 'img', 'find-replace.png'),
    'play': os.path.join(PRJ_PATH, 'img', 'play.png'),
    'stop': os.path.join(PRJ_PATH, 'img', 'stop.png'),
    'file-run': os.path.join(PRJ_PATH, 'img', 'file-run.png'),
    'debug': os.path.join(PRJ_PATH, 'img', 'debug.png'),
    'designer': os.path.join(PRJ_PATH, 'img', 'qtdesigner.png'),
    'bug': os.path.join(PRJ_PATH, 'img', 'bug.png'),
    'function': os.path.join(PRJ_PATH, 'img', 'function.png'),
    'module': os.path.join(PRJ_PATH, 'img', 'module.png'),
    'class': os.path.join(PRJ_PATH, 'img', 'class.png'),
    'attribute': os.path.join(PRJ_PATH, 'img', 'attribute.png'),
    'web': os.path.join(PRJ_PATH, 'img', 'web.png'),
    'splitH': os.path.join(PRJ_PATH, 'img', 'split-horizontal.png'),
    'splitV': os.path.join(PRJ_PATH, 'img', 'split-vertical.png'),
    'splitCRotate': os.path.join(PRJ_PATH, 'img', 'panels-change-position.png'),
    'splitMRotate': os.path.join(PRJ_PATH, 'img', 'panels-change-vertical-position.png'),
    'indent-less': os.path.join(PRJ_PATH, 'img', 'indent-less.png'),
    'indent-more': os.path.join(PRJ_PATH, 'img', 'indent-more.png'),
    'console': os.path.join(PRJ_PATH, 'img', 'console.png'),
    'pref': os.path.join(PRJ_PATH, 'img', 'preferences-system.png'),
    'tree-app': os.path.join(PRJ_PATH, 'img', 'tree', 'project', 'tree-app.png'),
    'tree-code': os.path.join(PRJ_PATH, 'img', 'tree', 'project', 'tree-code.png'),
    'tree-folder': os.path.join(PRJ_PATH, 'img', 'tree', 'project', 'tree-folder.png'),
    'tree-html': os.path.join(PRJ_PATH, 'img', 'tree', 'project', 'tree-html.png'),
    'tree-generic': os.path.join(PRJ_PATH, 'img', 'tree', 'project', 'tree-generic.png'),
    'tree-css': os.path.join(PRJ_PATH, 'img', 'tree', 'project', 'tree-CSS.png'),
    'tree-java': os.path.join(PRJ_PATH, 'img', 'tree', 'project', 'tree-java.png'),
    'tree-python': os.path.join(PRJ_PATH, 'img', 'tree', 'project', 'tree-python.png'),
    'tree-image': os.path.join(PRJ_PATH, 'img', 'tree', 'project', 'tree-image.png'),
    'comment-code': os.path.join(PRJ_PATH, 'img', 'comment-code.png'),
    'uncomment-code': os.path.join(PRJ_PATH, 'img', 'uncomment-code.png'),
    'reload-file': os.path.join(PRJ_PATH, 'img', 'reload-file.png'),
}

syntax_files = os.path.join(PRJ_PATH, 'plugins', 'syntax')

plugins = os.path.join(PRJ_PATH, 'plugins')

start_page_url = os.path.join(PRJ_PATH, 'doc', 'startPage.html')

descriptor = os.path.join(PRJ_PATH, 'plugins', 'descriptor.json')

twits = os.path.join(PRJ_PATH, 'doc','twit_posts.txt')

bugs_page = 'http://code.google.com/p/ninja-ide/issues/list'
