from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.base import RunTouchApps


class MySearchButtons(BoxLayout):
    pass

class SearchButtonApp(App):
    def build(self):
        return MySearchButtons()


RunTouchApp(SearchButtonApp())