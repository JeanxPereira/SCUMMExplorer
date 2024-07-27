import os
from pathlib import Path

from nutcracker.kernel2.fileio import ResourceFile
from nutcracker.sputm.preset import sputm

from PyQt6.QtWidgets import QTreeWidgetItem
from PyQt6.QtCore import Qt

def open_game_resource(filename: str | os.PathLike[str]):
    with ResourceFile.load(filename, key=0x00) as resource:
        schema = sputm.generate_schema(resource)
        root = sputm(schema=schema).map_chunks(resource)
        for element in root:
            yield element

def read_la_files(file_path):
    base_path = Path(file_path)
    base_name = base_path.stem
    base_dir = base_path.parent

    la_files = [base_path]
    for ext in ['LA1', 'LA2']:
        additional_file = base_dir / f"{base_name[:-1]}{ext[-1]}"
        if additional_file.exists():
            la_files.append(additional_file)

    data_dict = {}
    for la_file in la_files:
        try:
            elements = open_game_resource(la_file)
            for element in elements:
                block_name = element.tag
                block_size = len(element.data) if hasattr(element, 'data') else 0
                if block_name not in data_dict:
                    data_dict[block_name] = []
                data_dict[block_name].append((element, block_size))
        except Exception as e:
            print(f"Error reading {la_file}: {e}")
    
    return data_dict

def populate_tree_item(parent_item, element, block_size, set_icon_callback):
    item = QTreeWidgetItem(parent_item)
    item.setText(0, element.tag)
    item.setText(1, str(block_size))
    item_data = (element.tag, element.offset, block_size, 'Standard') if hasattr(element, 'offset') else (element.tag, 0, block_size, 'Standard')
    item.setData(0, Qt.ItemDataRole.UserRole, item_data)

    # Store palette data in the item for relevant blocks
    if element.tag in ['APAL', 'RGBS']:
        item.setData(1, Qt.ItemDataRole.UserRole, element.data)

    set_icon_callback(item, element.tag)

    for child in element.children():
        child_size = len(child.data) if hasattr(child, 'data') else 0
        populate_tree_item(item, child, child_size, set_icon_callback)
    
    # Map WRAP content within IMAG and ROOM
    if element.tag in ['IMAG', 'ROOM']:
        wrap = next((child for child in element.children() if child.tag == 'WRAP'), None)
        if wrap:
            wrap_item = QTreeWidgetItem(item)
            wrap_item.setText(0, 'WRAP')
            wrap_item.setText(1, str(len(wrap.data) if hasattr(wrap, 'data') else 0))
            for wrap_child in wrap.children():
                wrap_child_size = len(wrap_child.data) if hasattr(wrap_child, 'data') else 0
                populate_tree_item(wrap_item, wrap_child, wrap_child_size, set_icon_callback)