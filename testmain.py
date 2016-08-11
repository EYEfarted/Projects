from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
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
from kivy.uix.image import Image
from kivy.adapters.models import SelectableDataItem
from kivy.event import EventDispatcher
from kivy.graphics import Color
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
    def __init__(self, **kwargs):
        super(SearchForm, self).__init__(**kwargs)
        if SearchScreen.search_item == None:
            print('None')
        else:
            with conn:
                c = conn.cursor()
                # print(SearchScreen.search_item ," SearchScreen().search_item")
                self.search_input.text = SearchScreen.search_item
                mypart = SearchScreen.search_item
                descriptors = mypart.split()
                nums = len(descriptors)
                l = ''
                k = ''
                for word in descriptors:
                    if word != descriptors[nums-1]:
                        l += "'%"+word + "%' AND Description LIKE "
                        k += "'%"+word + "%' AND Category LIKE "
                    else:
                        l += "'%"+word+"%'"
                        k += "'%"+word+"%'"
                if l == '':
                    c.execute("SELECT * FROM Inventory")
                else:
                    c.execute("SELECT * FROM Inventory WHERE Description LIKE "+l+" OR Category LIKE "+k+" OR Part_Number=?", (mypart,))
                results = c.fetchall()
                self.search_results.adapter.data.clear()

                for res in results:

                    Id, PartNum, Coord, SubCat, Desc, Stock, Price, Condition = res
                    parts = [("%s Part Number: %s Description: %s and you have %s in stock at %s each.") % (Id, PartNum, Desc, Stock, Price)]

                    self.search_results.adapter.data.extend(parts)
                    self.search_results._trigger_reset_populate()


    def search_location(self, part):
        with conn:
            c = conn.cursor()
            # print('self.search_input.text = '+self.search_input.text)
            SearchScreen.search_item = self.search_input.text
            if SearchScreen.search_item == None:
                mypart = part
            else:
                mypart = SearchScreen.search_item


            descriptors = mypart.split()
            nums = len(descriptors)
            l = ''
            k = ''
            for word in descriptors:
                if word != descriptors[nums-1]:
                    l += "'%"+word + "%' AND Description LIKE "
                    k += "'%"+word + "%' AND Category LIKE "
                else:
                    l += "'%"+word+"%'"
                    k += "'%"+word+"%'"
            if l == '':
                c.execute("SELECT * FROM Inventory")
            else:
                c.execute("SELECT * FROM Inventory WHERE Description LIKE "+l+" OR Category LIKE "+k+" OR Part_Number=?", (mypart,))
            results = c.fetchall()
            self.search_results.adapter.data.clear()
            if results == []:
                x = [('Item not found. Try different search or click to add')]
                self.search_results.adapter.data.extend(x)
            for res in results:

                Id, PartNum, Coord, SubCat, Desc, Stock, Price, Condition = res
                parts = [("%s Part Number: %s Description: %s and you have %s in stock at %s each.") % (Id, PartNum, Desc, Stock, Price)]

                self.search_results.adapter.data.extend(parts)
                self.search_results._trigger_reset_populate()
            SearchScreen.search_item = self.search_input.text


class SearchScreen(Screen):
    search_item = None


    def search_word(self):
        # print("SearchForm().search_input.text under SearchScreen ="+self.SearchForm().search_input.text)
        self.clear_widgets()
        self.add_widget(SearchForm())

    def set_search_item(self, text):
        self.search_item = text


class PartDetails(EventDispatcher):
    part_number = ObjectProperty()
    category = ObjectProperty()
    description = ObjectProperty()
    stock = ObjectProperty()
    price = ObjectProperty()
    condition = ObjectProperty()
    pid = ObjectProperty()
    coordinates = ObjectProperty()

class Details(BoxLayout):
    pass

class LocationButton(ListItemButton, Button):
    def what_am_i(self):
        if self.text != 'Item not found. Try different search or click to add':
            x = self.text
            y = x.find(" ")
            z = x[:y]
            with conn:
                c = conn.cursor()
                c.execute("SELECT * FROM Inventory WHERE ID=?", (z,))
                part = c.fetchone()
                # print('Heres part[0]', part[0])

                self.parent.parent.parent.parent.parent.parent.info.pid = (str(part[0]))
                # print(self.parent.parent.parent.parent.parent.parent.info.pid,"this is the location button pid")
                self.parent.parent.parent.parent.parent.parent.info.part_number = str(part[1])
                self.parent.parent.parent.parent.parent.parent.info.coordinates = str(part[2])

                # print(self.parent.parent.parent.parent.parent.parent.info.part_number,"this is the location button part_number")
                self.parent.parent.parent.parent.parent.parent.info.category = str(part[3])
                self.parent.parent.parent.parent.parent.parent.info.description = str(part[4])
                self.parent.parent.parent.parent.parent.parent.info.stock = str(part[5])
                self.parent.parent.parent.parent.parent.parent.info.price = str(part[6])
                self.parent.parent.parent.parent.parent.parent.info.condition = str(part[7])
        else:
            with conn:
                c = conn.cursor()
                new_item = (0, 1234, 'category', 'description', 0, 0, 'new')
                c.execute("INSERT INTO Inventory (Part_Number, Shelf, Category, Description, Stock, Price, Condition) VALUES(?, ?, ?, ?, ?, ?, ?)", new_item)
                conn.commit()
                c.execute("SELECT * FROM Inventory WHERE ID=?", (c.lastrowid,))
                part = c.fetchone()

                self.parent.parent.parent.parent.parent.parent.info.pid = (str(part[0]))
                self.parent.parent.parent.parent.parent.parent.info.part_number = str(part[1])
                self.parent.parent.parent.parent.parent.parent.info.coordinates = str(part[2])
                self.parent.parent.parent.parent.parent.parent.info.category = str(part[3])
                self.parent.parent.parent.parent.parent.parent.info.description = str(part[4])
                self.parent.parent.parent.parent.parent.parent.info.stock = str(part[5])
                self.parent.parent.parent.parent.parent.parent.info.price = str(part[6])
                self.parent.parent.parent.parent.parent.parent.info.condition = str(part[7])



class LoginScreen(Screen):
    def creds(self):
        if self.ids['uname'].text == '' and self.ids['pword'].text == '':
            self.parent.current = 'select'


class SelectScreen(Screen):
    pass

class UploadScreen(Screen):
    upload_file = ObjectProperty()
    def go_back(self):
        print(self.upload_file.text)
        self.parent.current = 'select'


    def create_table(self):
        csvfile = self.upload_file.text

        try:
            print("Creating table...")
            c = conn.cursor()
            c.execute("DROP TABLE IF EXISTS Inventory")
            print("Checked for and dropped table if exists")
            c.execute("CREATE TABLE Inventory(ID INTEGER PRIMARY KEY, Part_Number INTEGER, Shelf INTEGER, Category TEXT, Description TEXT, Stock INTEGER, Price REAL, Condition TEXT)")
            print("Done.")
            print("Importing data now...")
    ## the inport happens here:
            things = csv.reader(open(csvfile))
            for line in things:
                stuff = [(i) for i in line]
                print(stuff)
                c.executemany("INSERT INTO Inventory (Part_Number, Shelf, Category, Description, Stock, Price, Condition) VALUES(?, ?, ?, ?, ?, ?, ?)", (stuff,))
            conn.commit()
        except sqlite3.Error:
            if conn:
                conn.rollback()
            print("Error %s:" % sqlite3.Error)
            sys.exit(1)
        finally:
            if conn:
                print("Data imported.")












class MyTextInput(TextInput):
    def update(self, obj, column):
        with conn:
            c = conn.cursor()
            pid = str(MyScreenManager.info.pid)
            new = str(self.text)
            self.column = column
            command = "UPDATE Inventory SET {column}= {new} WHERE ID = {pid}".format(self.column, new, self.pid)
            c.execute("UPDATE Inventory SET Part_Number= ? WHERE ID = ?", (new, pid))
            conn.commit()

class SearchScreen(Screen):
    search_item = None
    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        self.add_widget(SearchForm())

    def search_word(self):
        # print("SearchForm().search_input.text under SearchScreen ="+self.SearchForm().search_input.text)
        self.clear_widgets()
        self.add_widget(SearchForm())

    def set_search_item(self, text):
        self.search_item = text

class ResultsScreen(Screen):
    pass


class MyScreenManager(ScreenManager):
    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)
    screen_three = ObjectProperty(None)
    screen_four = ObjectProperty(None)
    screen_five = ObjectProperty(None)
    screen_six = ObjectProperty(None)
    info = PartDetails()


    def what_am_i(self):

        z = self.info.pid
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Inventory WHERE ID=?", (z,))
            part = c.fetchone()
            print(part)

            self.info.pid = str(part[0])
            self.info.part_number = str(part[1])
            self.info.coordinates = str(part[2])

            self.info.category = str(part[3])
            self.info.description = str(part[4])
            self.info.stock = str(part[5])
            self.info.price = str(part[6])
            self.info.condition = str(part[7])

    def update(self, column, new_value):
        with conn:
            c = conn.cursor()
            pid = str(MyScreenManager.info.pid)
            print(pid)
            print(column)
            print(new_value)
            command = "UPDATE Inventory SET %s= %s WHERE ID = %s" % (column, new_value, pid)
            print('command = '+command)
            c.execute(command)
            conn.commit()


class TestMainApp(App):
    def build(self):
        x = MyScreenManager()
        return x

print("Connecting to database...")
conn = sqlite3.connect('inventory.db')


if __name__ == '__main__':
    TestMainApp().run()


conn.close
print("closing database")
