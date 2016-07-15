from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, Screen
from os.path import join



sm = ScreenManager()

for i in range(4):
    screen = Screen(name="title %d" % i)
    sm.add_widget(screen)

class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.row = 3
        self.add_widget(Image(source="logo.png"))
        self.hello = Button(text="Login")
        self.hello.bind(on_press=self.auth)
        self.add_widget(self.hello)

        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.username.bind(on_text_validation=self.auth)

        self.add_widget(self.username)
        self.add_widget(Label(text='Password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)


    def auth(self, button):
        print("button pressed")
        if self.username == "admin":
            print("user is admin")


class MyApp(App):
    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
