from kivy.lang import Builder
from kivy.base import runTouchApp

from kivy.uix.gridlayout import GridLayout
from membersearch import MemberSearch

Builder.load_string('''
<TeamDisplay>
    cols: 2
    rows: 3
    Button:
        id: add_button
        text:'Add Pokémon'
        on_release: self.parent.add_pokemon()
''')


class TeamDisplay(GridLayout):
    add_index = 0

    def add_pokemon(self, *args):
        if len(self.children) > 5:
            self.remove_widget(self.ids['add_button'])
            self.add_widget(MemberSearch(self.add_index, self), 0)
        else:
            self.add_widget(MemberSearch(self.add_index, self), 1)
        self.add_index += 1

    def notificate(self, *args):
        old_widget = args[0]
        self.add_index = args[1]
        new_widget = args[2]
        self.remove_widget(old_widget)
        if self.add_index:
            self.add_widget(new_widget, -self.add_index)
        else:
            self.add_widget(new_widget, 5)
        self.add_index = len(self.children)-1

# runTouchApp(TeamDisplay())