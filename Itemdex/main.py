from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics.vertex_instructions import (Rectangle,
                                                Ellipse,
                                                Line)

from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import itensdb
import os

class MySearchButtons(GridLayout):
    db = itensdb.ItemManager()
    ag_drop = DropDown()
    hr_drop = DropDown()
    sz_drop = DropDown()
    battle_drop = DropDown()
    berry_drop = DropDown()
    evolution_drop = DropDown()
    fossil_drop = DropDown()
    holditem_drop = DropDown()
    key_drop = DropDown()
    mail_drop = DropDown()
    misc_drop = DropDown()
    pokeball_drop = DropDown()
    recovery_drop = DropDown()


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
    shop = ListProperty(['']*9)
    pick_up = ListProperty(['']*6)
    # flav_versions =

    def update_effect_box(self):
        self.ids.effect_box.clear_widgets()
        if self.effect != '':
            lab = (Label(text = self.effect, font_size = 14, text_size = (self.width, None), size_hint_y = None))
            # calculating height here
            before = lab._label.render()
            lab.text_size=(self.width, None)
            after = lab._label.render()
            lab.height = (after[1]/before[1])*before[1] # ammount of rows * single row height
            # end
            self.ids.effect_box.add_widget(lab)
            self.ids.effect_box.height = lab.height

    def update_flav_box(self):
        self.ids.flav_box.clear_widgets()
        # self.ids.flav_box.unbind()
        flav_versions = ['GSC', 'RSE', 'FRLG', 'DPPl', 'HGSS', 'BW', 'B2W2', 'XY', 'oRaS']
        # self.garbage_colect()
        for text, ver in zip(self.flav_texts, flav_versions):
            if text != '':
                lab = (Label(text = ver+': '+text, font_size = 14, text_size = (self.width, None), size_hint_y = None))

                # calculating height here
                before = lab._label.render()
                lab.text_size=(self.width, None)
                after = lab._label.render()
                lab.height = (after[1]/before[1])*before[1] # ammount of rows * single row height
                # end
                self.ids.flav_box.add_widget(lab)
        self.ids.flav_box.height = self.get_children_height(self.ids.flav_box)

    def update_locations(self):
        self.ids.location_box.clear_widgets()
        loc_versions = ['GSC', 'RSE', 'FRLG', 'DPPl', 'HGSS', 'BW', 'B2W2', 'XY', 'oRaS', 'PokéWalker']
        for text, ver in zip(self.locations, loc_versions):
            if text != '':
                lab = (Label(text = ver+': '+text, font_size = 14, text_size = (self.width, None), size_hint_y = None))

                # calculating height here
                before = lab._label.render()
                lab.text_size=(self.width, None)
                after = lab._label.render()
                lab.height = (after[1]/before[1])*before[1] # ammount of rows * single row height
                # end
                self.ids.location_box.add_widget(lab)
        self.ids.location_box.height = self.get_children_height(self.ids.location_box)

    def update_shop(self):
        self.ids.shop_box.clear_widgets()
        shop_versions = ['GSC', 'RSE', 'FRLG', 'DPPl', 'HGSS', 'BW', 'B2W2', 'XY', 'oRaS', 'Battle Revolution']
        for text, ver in zip(self.shop, shop_versions):
            if text != '':
                lab = (Label(text = ver+': '+text, font_size = 14, text_size = (self.width, None), size_hint_y = None))

                # calculating height here
                before = lab._label.render()
                lab.text_size=(self.width, None)
                after = lab._label.render()
                lab.height = (after[1]/before[1])*before[1] # ammount of rows * single row height
                # end
                self.ids.shop_box.add_widget(lab)
        self.ids.shop_box.height = self.get_children_height(self.ids.shop_box)

    def update_pick_up(self):
        self.ids.pickup_box.clear_widgets()
        pickup_versions = ['RS', 'FRLG', 'Emerald', 'HGSS', 'BW', 'XY']
        for text, ver in zip(self.pick_up, pickup_versions):
            if text != '':
                lab = (Label(text = ver+': '+text, font_size = 14, text_size = (self.width, None), size_hint_y = None))

                # calculating height here
                before = lab._label.render()
                lab.text_size=(self.width, None)
                after = lab._label.render()
                lab.height = (after[1]/before[1])*before[1] # ammount of rows * single row height
                # end
                self.ids.pickup_box.add_widget(lab)
        self.ids.pickup_box.height = self.get_children_height(self.ids.pickup_box)

    def update_scroll(self):
        self.ids.scroll_box.height = self.get_children_height(self.ids.scroll_box)

    def get_children_height(self, node):
        total_height = 0
        for child in node.children:
            total_height = child.height + total_height
        return total_height

    def garbage_colect(self):
        pass

    def update_text(self, name, *args):
        self.vers_db = itensdb.ItemVersions()
        self.flav_bd = itensdb.FlavourText()
        self.loc_bd = itensdb.Locations()
        self.shop_db = itensdb.Shop()
        self.pick_db = itensdb.Pickup()
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
        self.shop = self.shop_db.get_by_name(name)
        self.pick_up = self.pick_db.get_by_name(name)

        img_path = os.path.join('Itens', self.category,'Sprites', self.text_item + '.tiff')
        if os.path.exists(img_path):
            self.ids.item_img.source = img_path
        else:
            self.ids.item_img.source = os.path.join('Itens', 'Sprites', 'mewtwo.gif')

        # self.garbage_colect()
        self.update_effect_box()
        self.update_flav_box()
        self.update_locations()
        self.update_shop()
        self.update_pick_up()
        self.update_scroll()
    def __init__(self, **kwargs):
        super(MySearchButtons, self).__init__(**kwargs)

        ag_list = self.db.get_names_a_r()
        hr_list = self.db.get_names_h_r()
        sz_list = self.db.get_names_s_z()
        battle_list = self.db.get_cat('battle')
        berry_list = self.db.get_cat('berry')
        evolution_list = self.db.get_cat('evolution')
        fossil_list = self.db.get_cat('fossil')
        holditem_list = self.db.get_cat('holditem')
        key_list = self.db.get_cat('key')
        mail_list = self.db.get_cat('mail')
        misc_list = self.db.get_cat('misc')
        pokeball_list = self.db.get_cat('pokeball')
        recovery_list = self.db.get_cat('recovery')

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

        for item_name in battle_list:
            btn = Button(text= item_name, size_hint_y=None, height=20)
            btn.bind(on_press =lambda btn: self.update_text(btn.text), on_release = self.battle_drop.dismiss)
            self.battle_drop.add_widget(btn)

        for item_name in berry_list:
            btn = Button(text= item_name, size_hint_y=None, height=20)
            btn.bind(on_press =lambda btn: self.update_text(btn.text), on_release = self.berry_drop.dismiss)
            self.berry_drop.add_widget(btn)

        for item_name in evolution_list:
            btn = Button(text= item_name, size_hint_y=None, height=20)
            btn.bind(on_press =lambda btn: self.update_text(btn.text), on_release = self.evolution_drop.dismiss)
            self.evolution_drop.add_widget(btn)

        for item_name in fossil_list:
            btn = Button(text= item_name, size_hint_y=None, height=20)
            btn.bind(on_press =lambda btn: self.update_text(btn.text), on_release = self.fossil_drop.dismiss)
            self.fossil_drop.add_widget(btn)

        for item_name in holditem_list:
            btn = Button(text= item_name, size_hint_y=None, height=20)
            btn.bind(on_press =lambda btn: self.update_text(btn.text), on_release = self.holditem_drop.dismiss)
            self.holditem_drop.add_widget(btn)

        for item_name in key_list:
            btn = Button(text= item_name, size_hint_y=None, height=20)
            btn.bind(on_press =lambda btn: self.update_text(btn.text), on_release = self.key_drop.dismiss)
            self.key_drop.add_widget(btn)

        for item_name in mail_list:
            btn = Button(text= item_name, size_hint_y=None, height=20)
            btn.bind(on_press =lambda btn: self.update_text(btn.text), on_release = self.mail_drop.dismiss)
            self.mail_drop.add_widget(btn)

        for item_name in misc_list:
            btn = Button(text= item_name, size_hint_y=None, height=20)
            btn.bind(on_press =lambda btn: self.update_text(btn.text), on_release = self.misc_drop.dismiss)
            self.misc_drop.add_widget(btn)

        for item_name in pokeball_list:
            btn = Button(text= item_name, size_hint_y=None, height=20)
            btn.bind(on_press =lambda btn: self.update_text(btn.text), on_release = self.pokeball_drop.dismiss)
            self.pokeball_drop.add_widget(btn)

        for item_name in recovery_list:
            btn = Button(text= item_name, size_hint_y=None, height=20)
            btn.bind(on_press =lambda btn: self.update_text(btn.text), on_release = self.recovery_drop.dismiss)
            self.recovery_drop.add_widget(btn)

class SearchButtonApp(App):
    def build(self):
        return MySearchButtons()


if __name__ == '__main__':
        SearchButtonApp().run()
