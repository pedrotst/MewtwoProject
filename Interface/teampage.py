from kivy.lang import Builder
from kivy.base import runTouchApp

from kivy.uix.gridlayout import GridLayout

from teamdisplay import TeamDisplay

Builder.load_string('''
<TeamPage>
    cols: 2
    rows: 1

    TeamDisplay:

    Label:
        size_hint_x: 0.3
        text: 'Text2'

''')

class TeamPage(GridLayout):
    pass

runTouchApp(TeamPage())