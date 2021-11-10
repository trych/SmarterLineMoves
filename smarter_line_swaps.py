import sublime
import sublime_plugin


sls_settings = {}


def plugin_loaded():
  global sls_settings
  sls_settings = sublime.load_settings('SmarterLineSwaps.sublime-settings')


class SmartSwapLineUpCommand(sublime_plugin.TextCommand):
  """
  Swaps lines up while keeping a set amount of lines visible between
  the uppermost moving selected line and the text window's top.
  """
  def run(self, edit):
    self.view.run_command('swap_line_up')

    sel_begin = self.view.sel()[0].begin()
    target_line = max(self.view.rowcol(sel_begin)[0] - sls_settings.get('swap_up_clearance'), 0)
    target_point = self.view.text_point(target_line, 0)

    self.view.show(target_point, False, False, False)


class SmartSwapLineDownCommand(sublime_plugin.TextCommand):
  """
  Swaps lines down while keeping a set amount of lines visible between
  the bottommost moving selected line and the text window's bottom.
  """
  def run(self, edit):
    self.view.run_command('swap_line_down')

    sel_end = self.view.sel()[-1].end()
    target_line = min(self.view.rowcol(sel_end)[0] + sls_settings.get('swap_down_clearance'), self.view.rowcol(len(self.view))[0])
    target_point = self.view.text_point(target_line, 0)

    self.view.show(target_point, False, False, False)


class SwapLineAboveCommand(sublime_plugin.TextCommand):
  """
  Extends the Swap Line Up Command so that it keeps moving the
  selection even after hitting the top of the text buffer by adding
  an extra empty line on top that gets swapped.
  """
  def run(self, edit):
    self.view.insert(edit, 0, '\n')
    self.view.run_command('swap_line_up')


class SwapLineBelowCommand(sublime_plugin.TextCommand):
  """
  Extends the Swap Line Down Command so that it keeps moving the
  selection even after hitting the bottom of the text buffer by adding
  an extra empty line on the bottom that gets swapped.
  """
  def run(self, edit):
    self.view.insert(edit, len(self.view), '\n')
    self.view.run_command('swap_line_down')


class UnswapLineAbove(sublime_plugin.TextCommand):
  """
  Undoes the swap line above command by moving the line back down
  and deleting the previously added empty lines.
  """
  def run(self, edit):
    self.view.run_command('swap_line_down')

    if self.view.line(0).empty():
      self.view.erase(edit, sublime.Region(0, 1))


class UnswapLineBelowCommand(sublime_plugin.TextCommand):
  """
  Undoes the swap line below command by moving the line back up
  and deleting the previously added empty lines.
  """
  def run(self, edit):
    self.view.run_command('swap_line_up')

    if self.view.line(len(self.view)).empty():
      self.view.erase(edit, sublime.Region(len(self.view) - 1, len(self.view)))


class SelectedLinesContextEventListener(sublime_plugin.EventListener):
    """
    Creates a custom context to allow key bindings to check if either the
    first or the last line is part of the current selection.
    """
    def on_query_context(self, view, key, operator, operand, match_all):

        if key == 'selection_in_first_line':
          key_condition = view.line(view.sel()[0].begin()) == view.line(0)
        elif key == 'selection_in_last_line':
          key_condition = view.line(view.sel()[-1].end()) == view.line(len(view))
        else:
          return None

        if operator == sublime.OP_EQUAL:
            return key_condition == operand
        elif operator == sublime.OP_NOT_EQUAL:
            return key_condition != operand

        return False


class SmarterLineSwapsSettingsEventListener(sublime_plugin.EventListener):
    """
    Called to handle the custom sls_settings key in the package's keymap.
    """
    def on_query_context(self, view, key, operator, operand, match_all):
        if not key.startswith('sls_settings.'):
            return None

        setting = key[len('sls_settings.'):]
        lhs = sls_settings.get(setting)

        if operator == sublime.OP_EQUAL:
            return lhs == operand
        elif operator == sublime.OP_NOT_EQUAL:
            return lhs != operand

        return False


class SwapLineCommandEventListener(sublime_plugin.EventListener):
    """
    An event listener that overwrites the default line swap commands
    when they are called via the menu entries Edit > Line > Swap Line Up/Down.
    """
    def on_text_command(self, view, command_name, args):

        if command_name == 'swap_line_up' and sls_settings.get('allow_smart_swap_up'):
            return ('smart_swap_line_up', {})

        if command_name == 'swap_line_down' and sls_settings.get('allow_smart_swap_down'):
            return ('smart_swap_line_down', {})
