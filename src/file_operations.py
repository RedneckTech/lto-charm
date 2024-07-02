import os

class FileOperations:
    def __init__(self, app):
        self.app = app

    def list_directory(self, path: str):
        try:
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        self.app.print(f"[blue]{entry.name}[/blue]")
                    else:
                        self.app.print(f"[green]{entry.name}[/green]")
        except Exception as e:
            self.app.print(f"[red]Error: {e}[/red]")

    def create_file(self, path: str, filename: str):
        full_path = os.path.join(path, filename)
        try:
            with open(full_path, 'w') as file:
                file.write('')
            self.app.print(f"[green]File created: {full_path}[/green]")
        except Exception as e:
            self.app.print(f"[red]Error: {e}[/red]")

    def delete_file(self, path: str):
        try:
            os.remove(path)
            self.app.print(f"[green]File deleted: {path}[/green]")
        except Exception as e:
            self.app.print(f"[red]Error: {e}[/red]")

    # Add more file operations as needed
