# Smarter Line Moves
A Sublime Text package that overrides Sublime's default line moving to work in a more predictable way.


## Overview
Sublime's default commands for moving lines – `Swap Line Up` and `Swap Line Down` – move files in a way that makes it difficult for the user to see where the text ends up once the selected text reaches the top or bottom of the window. This package fixes that by always keeping a few lines of space between the edges of the window and the moving text. This way, it is much easier to move the text into its dedicated position.

![Default swapping vs. smart swapping](https://user-images.githubusercontent.com/9803905/141032555-1bb01e54-7c68-43cd-86b1-ca0697b1f889.gif)

Additionally, Sublime's default swapping would stop at the top or bottom of the text buffer and not let the user move the text any further. This package fixes that by inserting new empty lines and therefore allowing the selected text to move above or below the original text. In case the text has been moved too far, the package allows to move the text back and will automatically delete any previously added empty lines.

![Default swapping vs. swapping below](https://user-images.githubusercontent.com/9803905/141029958-b9c9919a-7fea-4013-91a2-8027243fe9d8.gif)

The package offers the commands `Separate Text Up` and `Separate Text Down` to "separate" the selected text from the text above or below it. This is similar to Sublime Text's default `Insert Line After` and `Insert Line Before` commands, except that the selected text remains selected, so it appears like you move the selected text.

TODO Screencapture

To move text before *and* after the text selection simultaneously, the package adds the commands `Attract Text` and `Repel Text` that add or remove empty lines around the selected text respectively.

-------------------------------------------------------------------------------


## Installation ##

### Via Package Control ###

The best way to install the package is via Sublime's Package Control. This way the package will automatically keep up to date if there are new versions.

To install via Package Control, open the Command Palette and select the command `Package Control: Install Package` and search for `SmarterLineMoves`.

### Manually ###

You can install the package manually by [downloading the repo](https://api.github.com/repos/trych/SmarterLineMoves/zipball) and placing it in your Sublime Text `User` Package, which you can find by using `Preferences > Browse Packages...`. Just unzip the file and place it in the `User` folder. This installation method is not recommended, as the package will not automatically be updated.


-------------------------------------------------------------------------------


## Usage

### Smart Swapping

As the package overrides Sublime's default swapping commands, you can use the smarter swapping by simply using the regular shortcuts: <kbd>Shift+Ctrl+Up/Down</kbd> on Windows/Linux or <kbd>&#8984;+Ctrl+Up/Down</kbd> on macOS. The package will take care of the rest, keep the space between the selected text and the window edges or let the selected text move above or below the beginning and end of the text.

### Separate Text Up/Down

Use the <kbd>Shift+Ctrl+Alt+Up/Down</kbd> keys on Windows/Linux or <kbd>&#8984;+Ctrl+Alt+Up/Down</kbd> on macOS to separate the selected text up or down respectively.

### Attract/Repel Text

Use the <kbd>Shift+Ctrl+Alt+Right</kbd> keys on Windows/Linux or <kbd>&#8984;+Ctrl+Alt+Right</kbd> on macOS to to "repel" text from the current text selection and the <kbd>Shift+Ctrl+Alt+Left</kbd> keys on Windows/Linux or <kbd>&#8984;+Ctrl+Alt+Left</kbd> on macOS to "attract" text towards the current text selection.

-------------------------------------------------------------------------------


## Configuration

### Settings

The package's features can be changed and/or disabled by changing its settings.

You can open the settings file to see the default settings or change them to your custom settings under the `Preferences > Package Settings > SmarterLineSwaps` menu entry. The settings file has the following entries:

#### `smart_swap_up`: true/false (Default: true)

Turns the smart swapping in the up direction on or off. If it is turned off, Sublime's regular `Swap Line Up` command will be used again.

#### `smart_swap_down`: true/false (Default: true)

Turns the smart swapping in the down direction on or off. If it is turned off, Sublime's regular `Swap Line Down` command will be used again.

#### `swap_above`: true/false (Default: true)

Allows the text to move "above" the text buffer once the moving text reaches the top of the file by adding empty lines that the text can be swapped with, so it just keeps moving up when repeating the command.

#### `undo_swap_above`: true/false (Default: true)

If the selected text has been moved up "above" the text buffer too far, it can be moved back by using the `Swap Line Down` key binding. If this setting is set to true, the empty lines that have been previously added, will be automatically removed again.

#### `swap_below`: true/false (Default: true)

Allows the text to move "below" the text buffer once the moving text reaches the bottom of the file by adding empty lines that the text can be swapped with, so it just keeps moving down when repeating the command.

#### `undo_swap_below`: true/false (Default: true)

If the selected text has been moved down "below" the text buffer too far, it can be moved back by using the `Swap Line Up` key binding. If this setting is set to true, the empty lines that have been previously added, will be automatically removed again.

#### `squash_whitespace_only_lines`: true/false (Default: true)

If using the `Attract Text` command and this is set to true, lines that have only white space in them will be erased as well, as if they were empty lines. When this is set to false, those lines will be kept, just like regular lines with text content.

#### `move_up_clearance`: Number (Default: 5)

How many lines to keep visible between the moving text and the window top when using the package's text moving commands.

#### `move_down_clearance`: Number (Default: 5)

How many lines to keep visible between the moving text and the window bottom when using the package's text moving commands.

### Keyboard Shortcuts

You can change the package's default keyboard shortcuts for the `Separate Text Up/Down` and the `Attract/Repel Text` commands by changing their key bindings.

The key bindings for Windows/Linux are:

```json
  { "keys": ["ctrl+alt+shift+up"], "command": "separate_text_up" },
  { "keys": ["ctrl+alt+shift+down"], "command": "separate_text_down" },
  { "keys": ["ctrl+alt+shift+right"], "command": "repel_text" },
  { "keys": ["ctrl+alt+shift+left"], "command": "attract_text" },
```

The key bindings for macOS are:

```json
  { "keys": ["ctrl+alt+super+up"], "command": "separate_text_up" },
  { "keys": ["ctrl+alt+super+down"], "command": "separate_text_down" },
  { "keys": ["ctrl+alt+super+right"], "command": "repel_text" },
  { "keys": ["ctrl+alt+super+left"], "command": "attract_text" },
```

So if you want to change the keyboard shortcut for the `Attract Text` command to <kbd>Shift+Ctrl+A</kbd>, you can add the following line to your User keybinding map (which you can open via `Preferences > Key Bindings`):

```json
  { "keys": ["ctrl+shift+a"], "command": "attract_text" },
```

-------------------------------------------------------------------------------


## Issues and Feedback

If you run into any issues using SmarterLineSwaps or you have an idea for additional features, feel free to [open an issue in the package's issue tracker](https://github.com/trych/SmarterLineSwaps/issues).


-------------------------------------------------------------------------------


## License

SmarterLineSwaps is licensed under the [MIT License](LICENSE).
