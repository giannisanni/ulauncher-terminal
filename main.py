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
            # Try to find existing terminal window
            result = subprocess.run(['xdotool', 'search', '--class', 'gnome-terminal'], capture_output=True, text=True)
            window_ids = result.stdout.strip().split('\n')
            
            if not window_ids or window_ids == ['']:
                # No terminal found, open new one
                subprocess.Popen(['gnome-terminal', '--window'])
                time.sleep(0.5)  # Wait for terminal to open
                
                # Get the new terminal window
                result = subprocess.run(['xdotool', 'search', '--class', 'gnome-terminal'], capture_output=True, text=True)
                window_ids = result.stdout.strip().split('\n')
            
            if window_ids and window_ids != ['']:
                # Focus the last terminal window
                window_id = window_ids[-1]
                subprocess.run(['xdotool', 'windowactivate', window_id])
                time.sleep(0.1)  # Wait for window focus
                
                # Type and execute command
                subprocess.run(['xdotool', 'type', command])
                time.sleep(0.1)  # Small delay before Enter
                subprocess.run(['xdotool', 'key', 'Return'])
                return True
                
            return False
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
