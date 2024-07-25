from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QSplitter

def create_main_widget(parent):
    main_widget = QWidget()
    layout = QVBoxLayout(main_widget)
    
    file_view = QTreeWidget()
    file_view.setHeaderLabels(["Type", "Size"])
    
    layout.addWidget(file_view)
    
    return main_widget, file_view
