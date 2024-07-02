import os
import toml
from textual.app import App
from textual.widgets import Header, Footer, Input, TextLog
from textual.containers import Vertical
from file_operations import FileOperations

def load_config():
    if os.path.exists('config.toml'):
        with open('config.toml', 'r') as config_file:
            return toml.load(config_file)
    else:
        return {}

class LtoCharm(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = load_config()
        self.default_directory = self.config.get('settings', {}).get('default_directory', '.')
        self.file_ops = FileOperations(self)
        self.stylesheet = self.create_stylesheet()

    def create_stylesheet(self):
        styles = self.config.get('styles', {})
        input_height = styles.get('input_height', 3)
        input_border_color = styles.get('input_border_color', 'gray')
        textlog_border_color = styles.get('textlog_border_color', 'gray')

        return f"""
        Input {{
            height: {input_height};
            border: solid {input_border_color};
        }}
        TextLog {{
            overflow: auto;
            border: solid {textlog_border_color};
        }}
        """

    def compose(self):
        yield Header()
        yield Vertical(
            Input(placeholder="Command"),
            TextLog()
        )
        yield Footer()

    async def on_mount(self):
        self.command_input = self.query_one(Input)
        self.command_input.on_submit = self.handle_command
        self.text_log = self.query_one(TextLog)
        self.stylesheet.apply(self)

    async def handle_command(self, value):
        command = value.strip()
        self.text_log.write(f"[bold]lto-charm>[/bold] {command}")

        if command.startswith('ls'):
            path = command.split(' ')[1] if len(command.split(' ')) > 1 else self.default_directory
            self.file_ops.list_directory(path)
        elif command.startswith('touch'):
            _, path, filename = command.split(' ')
            self.file_ops.create_file(path, filename)
        elif command.startswith('rm'):
            _, path = command.split(' ')
            self.file_ops.delete_file(path)
        elif command in ['exit', 'quit']:
            await self.action_quit()
        else:
            self.text_log.write("[red]Unknown command[/red]")

if __name__ == "__main__":
    LtoCharm().run()
