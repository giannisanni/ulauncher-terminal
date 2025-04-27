import subprocess
import time
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

class TerminalExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

    def execute_command(self, command):
        try:
            # Open new terminal window
            subprocess.Popen(['gnome-terminal', '--window'])
            time.sleep(0.5)  # Wait for terminal to open

            # Type command using xdotool
            subprocess.run(['xdotool', 'type', command])
            time.sleep(0.1)  # Small delay before Enter
            subprocess.run(['xdotool', 'key', 'Return'])
            
            return True
        except Exception as e:
            print(f"Error executing command: {e}")
            return False

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        command = event.get_argument()
        
        if not command:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='Enter a command...',
                    description='Type a command to execute in terminal',
                    on_enter=ExtensionCustomAction('')
                )
            ])

        # Return item that will execute the command when selected
        return RenderResultListAction([
            ExtensionResultItem(
                icon='images/icon.png',
                name=f'Execute: {command}',
                description='Press enter to execute in terminal',
                on_enter=ExtensionCustomAction({
                    'command': command
                }, keep_app_open=False)
            )
        ])

class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        if isinstance(data, dict) and 'command' in data:
            extension.execute_command(data['command'])
        return HideWindowAction()

if __name__ == '__main__':
    TerminalExtension().run()
