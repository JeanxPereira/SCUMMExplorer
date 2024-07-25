from PyQt5.QtWidgets import QAction, QMenu
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

def create_menus(parent, menubar):
    file_menu = menubar.addMenu('File')
    
    open_file_action = QAction('Open File', parent)
    open_file_action.setShortcut('Ctrl+O')
    open_file_action.triggered.connect(parent.open_file)
    file_menu.addAction(open_file_action)
    
    exit_action = QAction('Exit', parent)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.triggered.connect(parent.close)
    file_menu.addAction(exit_action)
    
    recent_files_menu = QMenu('Recent Imported Files', parent)
    file_menu.addMenu(recent_files_menu)
    
    for recent_file in parent.settings.get('recent_files', []):
        recent_file_action = QAction(recent_file, parent)
        recent_file_action.triggered.connect(lambda checked, file=recent_file: parent.populate_tree(file))
        recent_files_menu.addAction(recent_file_action)

    # Edit Menu
    editMenu = menubar.addMenu('Edit')
    editMenu.addAction(create_action(parent, 'Undo', 'Ctrl+Z'))
    editMenu.addAction(create_action(parent, 'Redo', 'Ctrl+Y'))
    editMenu.addSeparator()
    editMenu.addAction(create_action(parent, 'Cut', 'Ctrl+X'))
    editMenu.addAction(create_action(parent, 'Copy', 'Ctrl+C'))
    editMenu.addAction(create_action(parent, 'Paste', 'Ctrl+V'))
    editMenu.addAction(create_action(parent, 'Delete'))
    editMenu.addAction(create_action(parent, 'Select All', 'Ctrl+A'))

    # Search Menu
    searchMenu = menubar.addMenu('Search')
    searchMenu.addAction(create_action(parent, 'Find', 'Ctrl+F'))
    searchMenu.addAction(create_action(parent, 'Replace', 'Ctrl+H'))
    searchMenu.addAction(create_action(parent, 'Search Again', 'F3'))
    searchMenu.addSeparator()
    searchMenu.addAction(create_action(parent, 'Go to...', 'Ctrl+G'))

    # View Menu
    viewMenu = menubar.addMenu('View')
    viewMenu.addAction(create_action(parent, 'Explorer'))
    viewMenu.addAction(create_action(parent, 'Informer'))
    viewMenu.addAction(create_action(parent, 'Log'))

    viewersMenu = QMenu('Viewers', parent)
    viewersMenu.addAction(create_checkable_action(parent, 'Hex Viewer'))
    viewersMenu.addAction(create_checkable_action(parent, 'Text Viewer'))
    viewersMenu.addAction(create_checkable_action(parent, 'Image Viewer'))
    viewersMenu.addAction(create_checkable_action(parent, 'Box Viewer'))
    viewersMenu.addAction(create_checkable_action(parent, 'Room Viewer'))
    viewersMenu.addAction(create_checkable_action(parent, 'Costume Viewer'))
    viewersMenu.addAction(create_checkable_action(parent, 'Pallete Viewer'))
    viewMenu.addMenu(viewersMenu)

    viewMenu.addSeparator()
    viewMenu.addAction(create_action(parent, 'Zoom In'))
    viewMenu.addAction(create_action(parent, 'Zoom Out'))
    viewMenu.addSeparator()
    viewMenu.addAction(create_action(parent, 'Divisions'))
    viewMenu.addAction(create_action(parent, 'Offset Display'))
    viewMenu.addAction(create_action(parent, 'Charset'))
    viewMenu.addAction(create_action(parent, 'Conversions'))

    # Tools Menu
    toolsMenu = menubar.addMenu('Tools')
    toolsMenu.addAction(create_action(parent, 'Hex Viewer', icon='icons/menu/HexViewer.png'))
    toolsMenu.addAction(create_action(parent, 'File Dump', icon='icons/menu/Save.png'))
    toolsMenu.addAction(create_action(parent, 'Specification Script Editor'))
    toolsMenu.addSeparator()
    toolsMenu.addAction(create_action(parent, 'Options', icon='icons/menu/Options.png'))
    toolsMenu.addAction(create_action(parent, 'Crash SCUMMRev', 'Shift+Ctrl+Backspace'))

    # Bookmarks Menu
    bookmarksMenu = menubar.addMenu('Bookmarks')
    bookmarksMenu.addAction(create_action(parent, 'Add..'))
    bookmarksMenu.addAction(create_action(parent, 'Manage Bookmarks...'))

    # Window Menu
    windowMenu = menubar.addMenu('Window')
    windowMenu.addAction(create_action(parent, 'Explorer - '))
    windowMenu.addAction(create_action(parent, 'Informer'))

    # Help Menu
    helpMenu = menubar.addMenu('Help')
    helpMenu.addAction(create_action(parent, 'SCUMM Revival Github', icon='icons/menu/GoToWeb.png'))
    helpMenu.addAction(create_action(parent, 'Tip of the day...', icon='icons/menu/Tip.png'))
    helpMenu.addSeparator()
    helpMenu.addAction(create_action(parent, 'About SCUMM Revival', icon='icons/menu/About.png'))

def create_action(parent, name, shortcut=None, icon=None, callback=None):
    if icon:
        action = QAction(QIcon(create_pixmap(icon)), name, parent)
    else:
        action = QAction(name, parent)
    
    if shortcut:
        action.setShortcut(shortcut)
    if callback:
        action.triggered.connect(callback)
    return action

def create_checkable_action(parent, name):
    action = QAction(name, parent)
    action.setCheckable(True)
    return action

def create_pixmap(icon_path):
    pixmap = QPixmap(icon_path)
    pixmap.setDevicePixelRatio(1)  # Desabilita a suavização
    pixmap = pixmap.scaled(pixmap.size(), Qt.IgnoreAspectRatio, Qt.FastTransformation)  # Usa Qt.FastTransformation para evitar suavização
    return pixmap
