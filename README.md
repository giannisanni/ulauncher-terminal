# Ulauncher Terminal Command Executor

A Ulauncher extension that allows you to execute terminal commands directly from Ulauncher.

## Features
- Quick terminal command execution
- Opens a new terminal window
- Automatically executes the command
- Terminal stays open after execution

## Requirements
- Ulauncher
- xdotool
- gnome-terminal (or another terminal emulator)

## Installation

### 1. Install Required Packages

For Ubuntu/Debian:
```bash
sudo apt install xdotool gnome-terminal
```

For Fedora:
```bash
sudo dnf install xdotool gnome-terminal
```

For Arch Linux:
```bash
sudo pacman -S xdotool gnome-terminal
```

For macOS:
```bash
brew install xdotool
# Note: You'll need to use iTerm2 or Terminal.app instead of gnome-terminal
```

2. Clone the repository to the Ulauncher extensions folder:
```bash
git clone https://github.com/giannisanni/ulauncher-terminal.git ~/.local/share/ulauncher/extensions/com.github.giannisan.ulauncher-terminal
```

3. Restart Ulauncher

## Usage
1. Open Ulauncher
2. Type `t` followed by your command (e.g., `t ls -la`)
3. Press Enter to execute

The extension will:
- Open a new terminal window
- Type and execute your command
- Keep the terminal window open for output

## Examples
- `t ls -la` - List files with details
- `t htop` - Open system monitor
- `t python3` - Start Python interpreter
- `t git status` - Check git status

## Contributing
Feel free to open issues or submit pull requests.

## License
MIT License
