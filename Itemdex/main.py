from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics.vertex_instructions import (Rectangle,
                                                Ellipse,
                                                Line)

from kivy.uix.scatter import Scatter
import itensdb

class MySearchButtons(BoxLayout):
    db = itensdb.ItemManager()
    ag_drop = DropDown()
    hr_drop = DropDown()
    sz_drop = DropDown()
    start_message = StringProperty("Welcome, please choose an item")
    text_item = StringProperty()
    category = StringProperty()
    type1 = StringProperty()
    type2 = StringProperty()
    jap_name = StringProperty()
    jap_transl = StringProperty()
    fling = NumericProperty()
    purch_price = NumericProperty()
    sell_price = NumericProperty()
    effect = StringProperty()
    versions_avail = ListProperty(['']*19)
    flav_texts = ListProperty(['']*9)
    locations = ListProperty(['']*10)


    def update_text(self, name, *args):
        self.vers_db = itensdb.ItemVersions()
        self.flav_bd = itensdb.FlavourText()
        self.loc_bd = itensdb.Locations()
        item_table = self.db.get_by_name(name)
        self.text_item = item_table[0]
        self.category = item_table[1]
        self.type1 = item_table[2]
        self.type2 = item_table[3]
        self.jap_name = item_table[4]
        self.jap_transl = item_table[5]
        self.fling = item_table[6]
        self.purch_price = item_table[7]
        self.sell_price = item_table[8]
        self.effect = item_table[9]
        self.versions_avail = self.vers_db.get_by_name(name)
        self.flav_texts = self.flav_bd.get_by_name(name)
        self.locations = self.loc_bd.get_by_name(name)
        # print(?)
    def __init__(self, **kwargs):
        super(MySearchButtons, self).__init__(**kwargs)

        self.ag_drop = DropDown()
        self.hr_drop = DropDown()
        self.sz_drop = DropDown()
        ag_list = self.db.get_names_a_r()
        hr_list = self.db.get_names_h_r()
        sz_list = self.db.get_names_s_z()

        for item_name in ag_list:
            btn = Button(text= item_name, size_hint_y=None, height=20)
            btn.bind(on_press =lambda btn: self.update_text(btn.text), on_release = self.ag_drop.dismiss)
            self.ag_drop.add_widget(btn)
        for item_name in hr_list:
            btn = Button(text= item_name, size_hint_y=None, height=20)
            btn.bind(on_press =lambda btn: self.update_text(btn.text), on_release = self.hr_drop.dismiss)
            self.hr_drop.add_widget(btn)
        for item_name in sz_list:
            btn = Button(text= item_name, size_hint_y=None, height=20)
            btn.bind(on_press =lambda btn: self.update_text(btn.text), on_release = self.sz_drop.dismiss)
            self.sz_drop.add_widget(btn)

class SearchButtonApp(App):
    def build(self):
        return MySearchButtons()


if __name__ == '__main__':
    SearchButtonApp().run()