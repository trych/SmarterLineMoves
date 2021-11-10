# Smarter Line Swaps
A Sublime Text package that overrides Sublime's default line swapping to work in a more predictable way.


## Overview
Sublime's default commands for moving lines – `Swap Line Up` and `Swap Line Down` – move files in a way that makes it difficult for the user to see where the text ends up once the selected text reaches the top or bottom of the window. This package fixes that by always keeping a few lines of space between the edges of the window and the moving text. This way, it is much easier to move the text into its dedicated position.

![Default swapping vs. smart swapping](https://user-images.githubusercontent.com/9803905/141032555-1bb01e54-7c68-43cd-86b1-ca0697b1f889.gif)

Additionally Sublime's default swapping would stop at the top or bottom of the text buffer and not let the user move the text any further. This package fixes that by inserting new empty lines and therefore allowing the selected text to move above or below the original text. In case the text has been moved too far, the package allows to move the text back and will automatically delete any previously added empty lines.

![Default swapping vs. swapping below](https://user-images.githubusercontent.com/9803905/141029958-b9c9919a-7fea-4013-91a2-8027243fe9d8.gif)


-------------------------------------------------------------------------------


## Installation ##

### Package Control ###

The best way to install the package is via Sublime's Package Control. This way the package will automatically keep up to date if there are new versions.

To install via Package Control, open the Command Palette and select the command `Package Control: Install Package` and search for `SmarterLineSwaps`.


-------------------------------------------------------------------------------


## Usage

As the package overrides Sublime's default swapping commands, you can use the smarter swapping by simply using the regular shortcuts: <kbd>Shift+Ctrl+Up/Down</kbd> on Windows/Linux or <kbd>&#8984;+Ctrl+Up/Down</kbd> on macOS. The package will take care of the rest, keep the space between the selected text and the window edges or let the selected text move above or below the beginning and end of the text.


-------------------------------------------------------------------------------


## Configuration

You can change and selectively disable the package's features by changing its settings.

You can open the settings file to see the default settings or change them to your custom settings under the `Preferences > Package Settings > SmarterLineSwaps` menu entry. The settings file has the following entries:

### `allow_smart_swap_up`: true/false (Default: true)

Turns the smart swapping in the up direction on or off. If it is turned off, Sublime's regular `Swap Line Up` command will be used again.

### `swap_up_clearance`: Number (Default: 5)

How many lines to keep visible between the moving text and the window top when smart swapping up is enabled.

### `allow_smart_swap_down`: true/false (Default: true)

Turns the smart swapping in the down direction on or off. If it is turned off, Sublime's regular `Swap Line Down` command will be used again.

### `swap_down_clearance`: Number (Default: 5)

How many lines to keep visible between the moving text and the window bottom when smart swapping down is enabled.

### `allow_swap_lines_above`: true/false (Default: true)

Allows the text to move "above" the text buffer once the moving text reaches the top of the file by adding empty lines that the text can be swapped with, so it just keeps moving up when repeating the command.

### `undo_swap_above`: true/false (Default: true)

If the selected text has been moved up "above" the text buffer too far, it can be moved back by using the `Swap Line Down` key binding. If this setting is set to true, the empty lines that have been previously added, will be automatically removed again.

### `allow_swap_lines_below`: true/false (Default: true)

Allows the text to move "below" the text buffer once the moving text reaches the bottom of the file by adding empty lines that the text can be swapped with, so it just keeps moving down when repeating the command.

### `undo_swap_below`: true/false (Default: true)

If the selected text has been moved down "below" the text buffer too far, it can be moved back by using the `Swap Line Up` key binding. If this setting is set to true, the empty lines that have been previously added, will be automatically removed again.


-------------------------------------------------------------------------------


## License

SmarterLineSwaps is licensed under the [MIT License](LICENSE).
