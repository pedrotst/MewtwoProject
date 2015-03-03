from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.properties import ListProperty

from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from memberdisplay import MemberDisplay

from Database.database import DatabaseManager

Builder.load_string('''
<MemberSearch>
    rows: 2
    cols: 1
    SearchText:
        id: poke_name
        size_hint_x: 1
        size_hint_y: None
        text: 'Pokémon'
        height: 30
        on_suggestions: root.create_drop_down(*args)
''')


class SearchText(TextInput):
    suggestions = ListProperty()
    drop_index = 0
    drop_view_pos = 0

    def on_focus(self, instance, focused, **kwargs):
        self.drop_index = 0
        self.drop_view_pos = 0

        super(SearchText, self).on_focus(instance, focused, **kwargs)
        if focused:
            Clock.schedule_once(lambda x: self.select_all())
        else:
            Clock.schedule_once(lambda x: self.cancel_selection())

    def do_backspace(self, from_undo=False, mode='bkspc'):
        super().do_backspace(from_undo, mode)

        self.drop_index = 0
        self.drop_view_pos = 0

        self.select_text(self.cursor_col, len(self.text))
        self.delete_selection()
        self.suggestions = []

        self.update_drop_down()

    def highlight_label(self, label, highlight=True):
        label.bold = highlight
        if highlight:
            label.color = [1, 0, 1, 1]
        else:
            label.color = [1, 1, 1, 1]

    def _key_down(self, key, repeat=False):
        displayed_str, internal_str, internal_action, scale = key

        drop_down = self.parent.drop_down

        grid = drop_down.children[0]

        max_height = grid.height

        labels = [label for label in grid.children]

        if internal_action == 'cursor_down':
            if self.drop_index < len(labels):
                self.drop_index += 1

                label = labels[-self.drop_index]

                self.drop_view_pos += label.height

                self.highlight_label(label)

                if self.drop_index > 1:
                    label = labels[-self.drop_index+1]

                    self.highlight_label(label, False)

        elif internal_action == 'cursor_up':
            if self.drop_index > 0:
                self.drop_index -= 1

                label = labels[-self.drop_index-1]

                self.drop_view_pos -= label.height

                self.highlight_label(label, False)

                if self.drop_index > 0:
                    label = labels[-self.drop_index]
                    self.highlight_label(label)

        elif internal_action == 'enter':
            if len(self.suggestions):
                if self.drop_index != 0:
                    poke_name = labels[-self.drop_index].text
                else:
                    poke_name = self.text
                self.cursor = (len(self.text), self.cursor_row)
                self.parent.replace_self(MemberDisplay(poke_name))# Label(text=poke_name))
        else:
            super()._key_down(key, repeat)

        if self.drop_view_pos > 44:
            drop_down.scroll_y = 1 - self.drop_view_pos / max_height
        else:
            drop_down.scroll_y = 1

    def update_drop_down(self):
        search_text = self.text
        if len(search_text) > 2:
            db_man = DatabaseManager()
            self.suggestions = db_man.find_pokemon_name(search_text)
            if len(self.suggestions):
                col = self.cursor_col
                suggestion = self.suggestions[0][col:]
                self.insert_text(suggestion)
                self.cursor = (col, self.cursor_row)

    def insert_text(self, substring, from_undo=False):
        self.drop_index = 0

        self.select_text(self.cursor_col, len(self.text))
        self.delete_selection()
        self.text = str(self.text).capitalize()
        super(SearchText, self).insert_text(substring, from_undo)
        if len(substring) == 1:
            self.update_drop_down()


class MemberSearch(GridLayout):
    drop_down = DropDown(max_height=132)

    def __init__(self, pos_index, observer, **kwargs):
        super().__init__(**kwargs)
        self.pos_index = pos_index
        self.observer = observer

    def create_drop_down(self, *args):
        drop_down = self.drop_down
        suggestions = args[1]
        drop_down.clear_widgets()
        for child in drop_down.children:
            drop_down.remove_widget(child)
        for suggestion in suggestions:
            lbl = Label(text=suggestion, size_hint_y=None, height=44)
            drop_down.add_widget(lbl)
        drop_down.open(args[0])

    def replace_self(self, new_widget):
        self.drop_down.dismiss()
        self.observer.notificate(self, self.pos_index, new_widget)

# runTouchApp(MemberSearch())