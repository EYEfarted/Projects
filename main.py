from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton, ListView
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.listview import ListItemButton, ListView
from kivy.adapters.listadapter import ListAdapter
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.adapters.models import SelectableDataItem
from openpyxl import load_workbook
import time
import random
import sqlite3
import csv
import barcode
import json




class SearchForm(BoxLayout):
    search_input = ObjectProperty()
    search_results = ObjectProperty()
    def search_location(self):
        with conn:
            c = conn.cursor()
            part = self.search_input.text
            descriptors = part.split()
            nums = len(descriptors)
            l = ''
            for word in descriptors:
                if word != descriptors[nums-1]:
                    l += "'%"+word + "%' AND Description LIKE "
                else:
                    l += "'%"+word+"%'"
            if l == '':
                c.execute("SELECT * FROM Inventory")
            else:
                c.execute("SELECT * FROM Inventory WHERE Description LIKE "+l+" OR Part_Number=?", (part,))
            results = c.fetchall()
            self.search_results.adapter.data.clear()
            if results == []:
                x = [('No Results')]
                self.search_results.adapter.data.extend(x)
            for res in results:

                Id, PartNum, SubCat, Desc, Stock, Price, Percent, Totdollars = res
                parts = [("%s Part Number: %s Description: %s and you have %s in stock at %s each.") % (Id, PartNum, Desc, Stock, Price)]

                self.search_results.adapter.data.extend(parts)
                self.search_results._trigger_reset_populate()

class PartDetails(object):
    part_number = None
    subcategory = None
    description = None
    stock = None
    price = None
    percent = None
    pid = None

class Details(BoxLayout):
    pass

class LocationButton(ListItemButton, Button):
    def what_am_i(self):
        x = self.text
        y = x.find(" ")
        z = x[:y]
        with conn:
            l = ''
            c = conn.cursor()
            c.execute("SELECT * FROM Inventory WHERE ID=?", (z,))
            part = c.fetchone()

            self.parent.parent.parent.parent.parent.parent.info.pid = (part[0])
            self.parent.parent.parent.parent.parent.parent.info.part_number = (part[1])
            self.parent.parent.parent.parent.parent.parent.info.subcategory = (part[2])
            self.parent.parent.parent.parent.parent.parent.info.description = (part[3])
            self.parent.parent.parent.parent.parent.parent.info.stock = (part[4])
            self.parent.parent.parent.parent.parent.parent.info.price = (part[5])
            self.parent.parent.parent.parent.parent.parent.info.percent = (part[6])
            self.parent.parent.parent.parent.parent.parent.info.pid = (part[7])


class LoginScreen(Screen):
    def creds(self):
        if self.ids['uname'].text == '' and self.ids['pword'].text == '':
            self.parent.current = 'select'

class BarcodeScreen(Screen):
    def generate_barcode(self):
        time.sleep(1)
        self.parent.current = 'search'

class SelectScreen(Screen):
    pass

class UploadScreen(Screen):
    pass

class ReportsScreen(Screen):
    pass

class SelectScreen(Screen):
    pass

class DetailPartView(BoxLayout):
    pass

class SearchScreen(Screen):
    def search_word(self):
        self.clear_widgets()
        self.add_widget(SearchForm())

class MyPopup(Popup):
    def update_existing(self, part, col, pid):
        with conn:
            c = conn.cursor()
            self.col = col
            self.pid = pid
            self.part = part
            part = str(self.part).replace("'","")
            col = str(self.col).replace("'","")
            pid = str(self.pid).replace("'","")
            new = str(self.new.text).replace("'","")
            # for row in c.execute("SELECT * FROM Inventory WHERE ID = ?", (pid,)):
            #     Id, PartNum, SubCat, Desc, Stock, Price, Percent, Totdollars = row
            #     print("\nItem before changes..")
            #     print(("Item Id: %s\nPart Number: %s\nSub Category: %s\nDescription: %s\nTotal in Stock: %s\nList Price: %s\nPercent of cost: %s\nTotal Value of Stock: %s") % (row))
            #
            #         #### this may be bad need to make more secure
            c.execute("UPDATE Inventory SET "+col+"= ? WHERE ID = ?", (new, pid))
            conn.commit()
            #
            # for item in c.execute("SELECT * FROM Inventory WHERE ID = ?", (pid,)):
            #     Id, PartNum, SubCat, Desc, Stock, Price, Percent, Totdollars = item
            #     print("\nThese are the new values")
            #     print(("Item Id: %s\nPart Number: %s\nSub Category: %s\nDescription: %s\nTotal in Stock: %s\nList Price: %s\nPercent of cost: %s\nTotal Value of Stock: %s") % (item))
            #


class ResultsScreen(Screen):

    def show_results(self):
        self.clear_widgets()        # need to add a go back here
        self.add_widget(DetailPartView())

    def change_quantity(self):
        popup = MyPopup(title='What is the new quantity?', size_hint=(0.7, 0.3))
        popup.col = 'Stock'
        popup.open()

    def change_price(self):
        popup = MyPopup(title= 'What is the new price?', size_hint=(0.7, 0.3))
        popup.col = 'Price'
        popup.open()

    def change_description(self):
        popup = MyPopup(title= 'What is the new description?', size_hint=(0.7, 0.3))
        popup.col = 'Description'
        popup.open()

    def change_part_number(self):
        popup = MyPopup(title= 'What is the new Part Number?', size_hint=(0.7, 0.3))
        popup.col = 'Part_Number'
        popup.open()

    def change_picture(self):
        print("no camera yet")

class MyScreenManager(ScreenManager):
    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)
    screen_three = ObjectProperty(None)
    screen_four = ObjectProperty(None)

    info = PartDetails()


class MainApp(App):
    def build(self):
        x = MyScreenManager()
        return x


conn = sqlite3.connect('inventory.db')


if __name__ == '__main__':
    MainApp().run()
print("closing database")
conn.close
