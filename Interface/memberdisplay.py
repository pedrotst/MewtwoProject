import os
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.base import runTouchApp

from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty, ObjectProperty, BooleanProperty

from kivy.uix.floatlayout import FloatLayout
from TeamBuilder.team import TeamMember

Builder.load_string('''
<MemberDisplay>
    Label:
        id: Title
        pos_hint: {'x':0.01, 'y':.89}
        font_size: root.font_resize
        font_bold: True
        size_hint: 0.3, 0.1
        on_texture: root.update(*args)
        on_size: root.update(*args)
        text: root.poke_name
    Image:
        #canvas:
        #    Color:
        #        rgba: 1, 0, 1, 0.3
        #    Rectangle:
        #        size: self.size
        #        pos: self.pos
        pos_hint: {'x':0.01, 'y':.58}
        size_hint: 0.3, 0.3
        source: root.poke_img
    GridLayout:
        cols: 2
        rows: 4
        size_hint: 0.2, 0.3
        pos_hint: {'x':.32, 'y':.58}
        Label:
            text: 'Level:'
            font_size: 12
        Button:
            text: '100'
            font_size: 11
        Label:
            text: 'Gender:'
            font_size: 10
        Button:
            text: root.poke_gender
            font_size: 11
            on_release: root.change_gender(*args)
        Label:
            text: 'Shiny:'
            font_size: 12
        Button:
            text: root.is_shinny
            font_size: 11
            on_release: root.set_shinny(*args)
        Label:
            text: 'Happiness:'
            font_size: 8
        Button:
            text: '255'
            font_size: 11
''')


class MemberDisplay(FloatLayout):
    add_index = 0
    font_resize = NumericProperty()

    member = ObjectProperty()

    poke_name = StringProperty()
    poke_img = StringProperty()
    poke_gender = StringProperty()
    is_shinny = StringProperty('F')

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.font_resize = 18
        self.poke_name = name
        self.member = TeamMember(name)
        self.poke_gender = self.member.get_gender()

        if self.member.is_shinny():
            self.is_shinny = 'Y'
            self.poke_img = os.path.join('..', 'Pokedex', self.member.get_img().get_spath_img())
        else:
            self.is_shinny = 'N'
            self.poke_img = os.path.join('..', 'Pokedex', self.member.get_img().get_path_img())

    def change_gender(self, *args):
        if self.poke_gender == 'M':
            self.poke_gender = 'F'

        elif self.poke_gender == 'F':
            self.poke_gender = 'M'

        self.member.set_gender(self.poke_gender)

    def set_shinny(self, *args):
        if self.is_shinny == 'Y':
            self.is_shinny = 'N'
            self.poke_img = os.path.join('..', 'Pokedex', self.member.get_img().get_path_img())

        elif self.is_shinny == 'N':
            self.is_shinny = 'Y'
            self.poke_img = os.path.join('..', 'Pokedex', self.member.get_img().get_spath_img())

        self.member.set_shinny(self.is_shinny)

    def update(self, *args):
        width_box = self.ids['Title'].size[0]
        width_font = self.ids['Title'].texture_size[0]

        if width_font:
            if width_box > 1.05*width_font:
                self.font_resize = self.ids['Title'].font_size + 1
            if width_box < 0.95*width_font:
                self.font_resize = self.ids['Title'].font_size - 1



# runTouchApp(MemberDisplay())