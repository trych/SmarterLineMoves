import sublime
import sublime_plugin


slm_settings = {}


def plugin_loaded():
  global slm_settings
  slm_settings = sublime.load_settings('SmarterLineMoves.sublime-settings')


class SmartSwapLineUpCommand(sublime_plugin.TextCommand):
  """
  Swaps lines up while keeping a set amount of lines visible between
  the uppermost moving selected line and the text window's top.
  """
  def run(self, edit):
    self.view.run_command('swap_line_up')
    clear_top(self.view)
    if slm_settings.get('auto_reindent'):
      self.view.run_command('reindent')


class SmartSwapLineDownCommand(sublime_plugin.TextCommand):
  """
  Swaps lines down while keeping a set amount of lines visible between
  the bottommost moving selected line and the text window's bottom.
  """
  def run(self, edit):
    self.view.run_command('swap_line_down')
    clear_bottom(self.view)
    if slm_settings.get('auto_reindent'):
      self.view.run_command('reindent')


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
    clear_bottom(self.view)


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

    if self.view.line(self.view.size()).empty():
      self.view.erase(edit, sublime.Region(len(self.view) - 1, len(self.view)))


class SeparateTextUp(sublime_plugin.TextCommand):
  """
  Separates selected text from the text below it by inserting
  empty lines below the text, thus moving the selected text up.
  """
  def run(self, edit):
    view = self.view

    sel_end = view.sel()[-1].end()
    sel_last_line = view.rowcol(sel_end)[0]
    insertPoint = view.text_point(sel_last_line + 1, 0)

    view.insert(edit, insertPoint, '\n')

    clear_top(view, True)


class SeparateTextDown(sublime_plugin.TextCommand):
  """
  Separates selected text from the text above it by inserting
  empty lines above the text, thus moving the selected text down.
  """
  def run(self, edit):
    view = self.view
    lh = view.line_height()

    sel_begin = view.sel()[0].begin()
    sel_first_line = view.rowcol(sel_begin)[0]
    insertPoint = view.text_point(sel_first_line, 0)

    view.insert(edit, insertPoint, '\n')

    clear_bottom(view)


class RepelText(sublime_plugin.TextCommand):
  """
  Moves neighboring text away from the text selection by inserting
  empty lines around the text selection.
  """
  def run(self, edit):
    view = self.view

    sel_begin = view.sel()[0].begin()
    begin_insert_point = view.text_point(view.rowcol(sel_begin)[0], 0)

    sel_end = view.sel()[-1].end()
    end_insert_point = view.text_point(view.rowcol(sel_end)[0] + 1, 0)

    view.insert(edit, begin_insert_point, '\n')
    view.insert(edit, end_insert_point, '\n')

    shift_view(view, 1)


class AttractText(sublime_plugin.TextCommand):
  """
  Pulls neighboring text towards the text selection by removing
  empty lines or – depending on the setting – whitespace only
  lines.
  """
  def run(self, edit):
    view = self.view

    prev_line = view.line(view.text_point(view.rowcol(view.sel()[0].begin())[0] - 1, 0))
    next_line = view.line(view.text_point(view.rowcol(view.sel()[-1].end())[0] + 1, 0))

    if next_line.empty() or (slm_settings.get('squash_whitespace_only_lines') and view.substr(next_line).isspace()):
      view.erase(edit, sublime.Region(next_line.begin(), next_line.end() + 1))

    if prev_line.empty() or (slm_settings.get('squash_whitespace_only_lines') and view.substr(prev_line).isspace()):
      first_line = view.rowcol(view.visible_region().begin())[0]

      view.erase(edit, sublime.Region(prev_line.begin(), prev_line.end() + 1))

      shift_view(view, -1)


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


class SmarterLineMovesSettingsEventListener(sublime_plugin.EventListener):
    """
    Called to handle the custom slm_settings key in the package's keymap.
    """
    def on_query_context(self, view, key, operator, operand, match_all):
        if not key.startswith('slm_settings.'):
            return None

        setting = key[len('slm_settings.'):]
        lhs = slm_settings.get(setting)

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

        if command_name == 'swap_line_up' and slm_settings.get('smart_swap_up'):
            return ('smart_swap_line_up', {})

        if command_name == 'swap_line_down' and slm_settings.get('smart_swap_down'):
            return ('smart_swap_line_down', {})


def shift_view(view, amt):
  current_pos = view.viewport_position()
  view.set_viewport_position((current_pos[0], current_pos[1] + (view.line_height() * amt)), False)


def clear_top(view, inverse = False):
  first_line_pos = view.text_to_layout(view.sel()[0].begin())[1] - view.viewport_position()[1]
  min_pos = view.line_height() * slm_settings.get('move_up_clearance')

  if inverse and (first_line_pos - view.line_height()) > min_pos:
    shift_view(view, 1)

  if first_line_pos < min_pos:
    shift_amt = (min_pos - first_line_pos) // view.line_height() + 1
    shift_view(view, -shift_amt)


def clear_bottom(view):
  last_line_pos = view.text_to_layout(view.sel()[-1].end())[1] - view.viewport_position()[1] + view.line_height()
  max_pos = view.viewport_extent()[1] - view.line_height() * slm_settings.get('move_down_clearance')

  if last_line_pos > max_pos:
    shift_amt = (last_line_pos - max_pos) // view.line_height() + 1
    shift_view(view, shift_amt)
