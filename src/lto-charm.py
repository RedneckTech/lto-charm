import os
import toml
from textual.app import App
from textual.widgets import Header, Footer, Input, Log, Tree
from textual.containers import Horizontal, Vertical
from file_operations import FileOperations

# Define the configuration directory
config_dir = "."

def load_config():
    """
    Load the configuration from config.toml file.

    Returns:
        dict: The configuration dictionary.
    """
    config_path = os.path.join(config_dir, 'config.toml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            return toml.load(config_file)
    else:
        return {}

class LtoCharm(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = load_config()
        self.default_directory = self.config.get('settings', {}).get('default_directory', '.')
        self.file_ops = FileOperations(self)

    def create_styles(self):
        #Create a styles dictionary based on the config.toml settings.
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
        #Define the layout of the application.
        yield Header()
        yield Horizontal(
            Vertical(
                Input(placeholder="Enter directory", id="dir_input_left"),
                Tree("Left Panel", id="tree_left"),  # Provide a label for the tree
            ),
            Vertical(
                Input(placeholder="Enter directory", id="dir_input_right"),
                Tree("Right Panel", id="tree_right"),  # Provide a label for the tree
            ),
        )
        yield Footer()

    async def on_mount(self):
        #Mount the components and apply the stylesheet when the application starts.
        self.dir_input_left = self.query_one("#dir_input_left", Input)
        self.dir_input_right = self.query_one("#dir_input_right", Input)
        self.tree_left = self.query_one("#tree_left", Tree)
        self.tree_right = self.query_one("#tree_right", Tree)

        self.dir_input_left.on_submit = self.update_tree_left
        self.dir_input_right.on_submit = self.update_tree_right

        styles = self.create_styles()
        input_styles = styles['input']
        log_styles = styles['log']

        self.dir_input_left.styles.height = input_styles['height']
        self.dir_input_left.styles.border_color = input_styles['border_color']
        self.dir_input_right.styles.height = input_styles['height']
        self.dir_input_right.styles.border_color = input_styles['border_color']

    async def update_tree_left(self, value):
        #Update the left tree with the contents of the directory entered by the user.
        path = value.strip()
        self.file_ops.populate_tree(self.tree_left, path)

    async def update_tree_right(self, value):
        #Update the right tree with the contents of the directory entered by the user.
        path = value.strip()
        self.file_ops.populate_tree(self.tree_right, path)

if __name__ == "__main__":
    LtoCharm().run()
