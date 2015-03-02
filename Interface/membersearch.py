from kivy.clock import Clock
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.properties import ListProperty

from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

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

    def on_focus(self, instance, focused, **kwargs):
        super(SearchText, self).on_focus(instance, focused, **kwargs)
        if focused:
            Clock.schedule_once(lambda x: self.select_all())
        else:
            Clock.schedule_once(lambda x: self.cancel_selection())

    def do_backspace(self, from_undo=False, mode='bkspc'):
        super().do_backspace(from_undo, mode)
        self.select_text(self.cursor_col, len(self.text))
        self.delete_selection()
        self.parent.dropdown.dismiss()

    def _key_down(self, key, repeat=False):
        if key[2] == 'cursor_down':
            print('Baixo')
        elif key[2] == 'cursor_up':
            print('Cima')
        else:
            super()._key_down(key, repeat)


    def insert_text(self, substring, from_undo=False):
        self.select_text(self.cursor_col, len(self.text))
        self.delete_selection()
        self.text = str(self.text).capitalize()
        super(SearchText, self).insert_text(substring, from_undo)

        search_text = self.text
        if len(search_text) > 2 and len(substring) == 1:
            db_man = DatabaseManager()
            self.suggestions = db_man.find_pokemon_name(search_text)
            if len(self.suggestions):
                col = self.cursor_col
                suggestion = self.suggestions[0][col:]
                self.insert_text(suggestion)
                self.cursor = (col, self.cursor_row)


class MemberSearch(GridLayout):
    dropdown = DropDown(max_height=140)
    def create_drop_down(self, *args):
        dropdown = self.dropdown
        suggestions = args[1]
        dropdown.clear_widgets()
        for child in dropdown.children:
            dropdown.remove_widget(child)
        for suggestion in suggestions:
            lbl = Label(text=suggestion, size_hint_y=None, height=44)
            dropdown.add_widget(lbl)
        dropdown.open(args[0])


# runTouchApp(MemberSearch())