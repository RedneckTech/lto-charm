import os
from textual.widgets import Tree

class FileOperations:

    def __init__(self, app):
        self.app = app

    def list_directory(self, path: str):
        try:
            tree_data = []
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        tree_data.append((entry.name, "directory"))
                    else:
                        tree_data.append((entry.name, "file"))
            return tree_data
        except Exception as e:
            self.app.log_widget.write(f"[red]Error: {e}[/red]")
            return []

    def populate_tree(self, tree: Tree, path: str):
        tree.clear()
        tree_data = self.list_directory(path)
        for name, entry_type in tree_data:
            if entry_type == "directory":
                tree.root.add(name, expanded=False)
            else:
                tree.root.add(name)
