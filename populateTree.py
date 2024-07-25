# populateTree.py
import tkinter as tk
from tkinter import ttk
from readLA import read_la_file  # Importe a função read_la_file

def populate_tree(tree, blocks):
    for idx, block in enumerate(blocks):
        tree.insert("", "end", iid=idx, text=f"Block {idx}", values=(block['type'], block['size']))

def main():
    # Leitura do arquivo
    blocks = read_la_file(r'D:\GamingLibrary\The Curse of Monkey Island\COMI.LA2')

    # Configuração da janela principal
    root = tk.Tk()
    root.title("SCUMM File Viewer")

    tree = ttk.Treeview(root, columns=('Type', 'Size'), show='headings')
    tree.heading('Type', text='Block Type')
    tree.heading('Size', text='Block Size')

    tree.pack(fill=tk.BOTH, expand=True)

    # Popula o TreeView com os blocos do arquivo
    populate_tree(tree, blocks)

    # Loop da interface
    root.mainloop()

if __name__ == "__main__":
    main()
