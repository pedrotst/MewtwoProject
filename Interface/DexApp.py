__author__ = 'Rodrigo'
from kivy.app import App
from kivy.uix.widget import Widget


class BasicInfo(Widget):
    pass


class DexWindow(Widget):
    pass


class DexApp(App):
    def build(self):
        return DexWindow()


if __name__ == '__main__':
    DexApp().run()