import os
import toml
from textual.app import App
from textual.widgets import Header, Footer, Input, Log
from textual.containers import Vertical
from file_operations import FileOperations

def load_config():
    """
    Load the configuration from config.toml file.

    Returns:
        dict: The configuration dictionary.
    """
    if os.path.exists('config.toml'):
        with open('config.toml', 'r') as config_file:
            return toml.load(config_file)
    else:
        return {}

class LtoCharm(App):
    """
    The main application class for the lto-charm file manager.
    """

    def __init__(self, **kwargs):
        """
        Initialize the LtoCharm application.

        Args:
            **kwargs: Additional keyword arguments for the App base class.
        """
        super().__init__(**kwargs)
        self.config = load_config()
        self.default_directory = self.config.get('settings', {}).get('default_directory', '.')
        self.file_ops = FileOperations(self)

    def create_styles(self):
        """
        Create a styles dictionary based on the config.toml settings.

        Returns:
            dict: The styles dictionary.
        """
        styles = self.config.get('styles', {})
        input_height = styles.get('input_height', 3)
        input_border_color = styles.get('input_border_color', 'gray')
        log_border_color = styles.get('log_border_color', 'gray')

        return {
            'input': {
                'height': input_height,
                'border_color': input_border_color
            },
            'log': {
                'border_color': log_border_color
            }
        }

    def compose(self):
        """
        Define the layout of the application.
        """
        yield Header()
        yield Vertical(
            Input(placeholder="Command", id="command_input"),
            Log(id="log_widget")
        )
        yield Footer()

    async def on_mount(self):
        """
        Mount the components and apply the stylesheet when the application starts.
        """
        self.command_input = self.query_one("#command_input", Input)
        self.command_input.on_submit = self.handle_command
        self.log_widget = self.query_one("#log_widget", Log)

        styles = self.create_styles()
        input_styles = styles['input']
        log_styles = styles['log']

        self.command_input.styles.height = input_styles['height']
        self.command_input.styles.border_color = input_styles['border_color']
        self.log_widget.styles.border_color = log_styles['border_color']

    async def handle_command(self, value):
        """
        Handle the command input by the user.

        Args:
            value (str): The command entered by the user.
        """
        command = value.strip()
        self.log_widget.write(f"[bold]lto-charm>[/bold] {command}")

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
            self.log_widget.write("[red]Unknown command[/red]")

if __name__ == "__main__":
    LtoCharm().run()
