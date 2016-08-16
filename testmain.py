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
from kivy.uix.checkbox import CheckBox
from kivy.adapters.models import SelectableDataItem
from kivy.event import EventDispatcher
from kivy.graphics import Color
from kivy.uix.dropdown import DropDown
from openpyxl import load_workbook
import time
import random
import sqlite3
import csv
import json
import os
import qrcode
import qrcode.image.svg
from qrcode.image.pure import PymagingImage
import png
import subprocess


username = ''
password = ''


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
                print('Heres part[0]', part[0])

                self.parent.parent.parent.parent.parent.parent.info.pid = (str(part[0]))
                print(self.parent.parent.parent.parent.parent.parent.info.pid,"this is the location button pid")
                self.parent.parent.parent.parent.parent.parent.info.part_number = str(part[1])
                self.parent.parent.parent.parent.parent.parent.info.coordinates = str(part[2])

                print(self.parent.parent.parent.parent.parent.parent.info.part_number,"this is the location button part_number")
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
        if self.ids['uname'].text == username and self.ids['pword'].text == password:
            self.parent.current = 'select'

class BarcodeScreen(Screen):
    def generate_single_barcode(self):

        data = "Part Number = "+str(MyScreenManager.info.part_number)+"\n"+str(MyScreenManager.info.description)+"\nYou have "+str(MyScreenManager.info.stock)+" in stock."+"\nAt $"+str(MyScreenManager.info.price)+" each"
        qrcode = subprocess.check_output("qr --factory=svg '"+data+"' > sometest.svg", shell=True)


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


class CategoryChecklist(GridLayout):
    category_textinput = ''

    def __init__(self, **kwargs):
        super(CategoryChecklist, self).__init__(**kwargs)
        self.cols = 4


        with conn:
            c = conn.cursor()
            c.execute("SELECT DISTINCT Category FROM Inventory")
            part = c.fetchall()
            for i in part:
                check = CheckBox(group='categories')
                check.id = i[0]
                check.bind(active=self.on_checkbox_active)
                print(check.id)
                self.add_widget(check)
                self.add_widget(Label(text=i[0]))

    def on_checkbox_active(self, checkbox, value):
        if value:
            print('The checkbox', self.category_textinput, 'is active', checkbox.id)
            MyScreenManager.info.category = checkbox.id
            print(MyScreenManager.info.category)
        else:
            print('The checkbox', checkbox, 'is inactive')



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

    def total_cost(self, stock, price):
        if stock == None:
            print("Stock = ", stock)
            return('0')
        if price == None:
            print("Price = ", price)
            return('0')
        if stock != None and price != None:
            return '%.2f' % (float(stock)*float(price))



class MyScreenManager(ScreenManager):
    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)
    screen_three = ObjectProperty(None)
    screen_four = ObjectProperty(None)
    screen_five = ObjectProperty(None)
    screen_six = ObjectProperty(None)
    info = PartDetails()



    def image_name(self, part_number):
        if os.path.exists(part_number+'.jpg') == True:
            return (part_number+'.jpg')
        else:
            return ('parts.jpg')
    def what_am_i(self):

        z = self.info.pid


        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Inventory WHERE ID=?", (z,))
            part = c.fetchone()
            print('This is part',part)

            self.info.pid = part[0]
            print(self.info.pid)
            self.info.part_number = part[1]
            print(self.info.part_number)
            self.info.coordinates = part[2]

            self.info.category = part[3]
            self.info.description = part[4]
            self.info.stock = part[5]
            self.info.price = part[6]
            self.info.condition = part[7]

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

    def delete_item(self, pid):
        print("deleting item", MyScreenManager.info.part_number)
        print(pid)
        print(MyScreenManager.info.pid)
        with conn:
            c = conn.cursor()
            c.execute("DELETE FROM Inventory WHERE ID =?", (MyScreenManager.info.pid,))
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
