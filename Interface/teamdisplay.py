from kivy.lang import Builder
from kivy.base import runTouchApp

from kivy.uix.gridlayout import GridLayout
from membersearch import MemberSearch

Builder.load_string('''
<TeamDisplay>
    cols: 2
    rows: 3
    text: 'THE BACKGROUND'
    font_size: 150
    Button:
        id: add_button
        text:'Add Pokémon'
        on_release: self.parent.add_pokemon()



''')


class TeamDisplay(GridLayout):
    def add_pokemon(self, *args):
        if len(self.children) > 5:
            self.remove_widget(self.ids['add_button'])
        self.add_widget(MemberSearch(), 1)


# runTouchApp(TeamDisplay())