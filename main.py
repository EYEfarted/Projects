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
    def search_location(self, part):
        with conn:
            c = conn.cursor()
            print(self.search_input.text)
            self.part = part
            mypart = self.part
            descriptors = mypart.split()
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
                c.execute("SELECT * FROM Inventory WHERE Description LIKE "+l+" OR Part_Number=?", (mypart,))
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

class PartDetails(EventDispatcher):
    part_number = StringProperty('')
    category = StringProperty('')
    description = StringProperty('')
    stock = StringProperty('')
    price = StringProperty('')
    percent = StringProperty('')
    pid = StringProperty('')

class Details(BoxLayout):
    pass

class LocationButton(ListItemButton, Button):
    def what_am_i(self):
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
            print(self.parent.parent.parent.parent.parent.parent.info.part_number,"this is the location button part_number")
            self.parent.parent.parent.parent.parent.parent.info.category = str(part[2])
            self.parent.parent.parent.parent.parent.parent.info.description = str(part[3])
            self.parent.parent.parent.parent.parent.parent.info.stock = str(part[4])
            self.parent.parent.parent.parent.parent.parent.info.price = str(part[5])
            self.parent.parent.parent.parent.parent.parent.info.percent = str(part[6])



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

class MyBackButton(Button):
    pass


class PartLabel(Label):
    pass
class DescLabel(Label):
    pass
class CategoryLabel(Label):
    pass
class StockLabel(Label):
    pass
class PriceLabel(Label):
    pass
class TotalLabel(Label):
    pass

class PartNumTextInput(TextInput):
    def update_part_number(self, obj):
        with conn:
            c = conn.cursor()
            pid = str(MyScreenManager.info.pid)
            new = str(self.text)
            c.execute("UPDATE Inventory SET Part_Number= ? WHERE ID = ?", (new, pid))
            conn.commit()

class PartNumPopup(Popup):
    t = None
    def __init__(self, **kwargs):
        super(PartNumPopup, self).__init__(**kwargs)
        self.t = PartNumTextInput(on_text_validate=self.dismiss)
        self.t.bind(on_text_validate=self.t.update_part_number)
        h = BoxLayout(orientation='horizontal')
        v = BoxLayout(orientation='vertical')
        n = Button(text='No', size_hint_x=0.25)
        yes_btn = Button(text='Yes', size_hint_x=0.25)
        l = Label(text='Commit changes to database?', size_hint_x=0.5)
        self.title = "What is the new Part Number?"
        h.add_widget(l)
        h.add_widget(yes_btn)
        h.add_widget(n)

        v.add_widget(self.t)
        v.add_widget(h)

        self.add_widget(v)

        n.bind(on_press=self.some_function)
        n.bind(on_release=self.dismiss)
        yes_btn.bind(on_press=self.t.update_part_number)
        yes_btn.bind(on_release=self.dismiss)

    def some_function(self, obj):
        self.t.text = MyScreenManager.info.part_number
        print('Pressed the no button')

class DescTextInput(TextInput):
    def update_description(self, obj):
        with conn:
            c = conn.cursor()
            pid = str(MyScreenManager.info.pid)
            new = str(self.text)
            c.execute("UPDATE Inventory SET Description= ? WHERE ID = ?", (new, pid))
            conn.commit()

class DescPopup(Popup):
    t = None
    def __init__(self, **kwargs):
        super(DescPopup, self).__init__(**kwargs)
        self.t = DescTextInput(on_text_validate=self.dismiss)
        self.t.bind(on_text_validate=self.t.update_description)
        h = BoxLayout(orientation='horizontal')
        v = BoxLayout(orientation='vertical')
        n = Button(text='No', size_hint_x=0.25)
        yes_btn = Button(text='Yes', size_hint_x=0.25)
        l = Label(text='Commit changes to database?', size_hint_x=0.5)
        self.title = "What is the new Description?"
        h.add_widget(l)
        h.add_widget(yes_btn)
        h.add_widget(n)

        v.add_widget(self.t)
        v.add_widget(h)

        self.add_widget(v)

        n.bind(on_press=self.some_function)
        n.bind(on_release=self.dismiss)
        yes_btn.bind(on_press=self.t.update_description)
        yes_btn.bind(on_release=self.dismiss)

    def some_function(self, obj):
        self.t.text = MyScreenManager.info.description
        print('Pressed the no button')

class StockTextInput(TextInput):
    def update_stock(self, obj):
        with conn:
            c = conn.cursor()
            pid = str(MyScreenManager.info.pid)
            new = str(self.text)
            c.execute("UPDATE Inventory SET Stock= ? WHERE ID = ?", (new, pid))
            conn.commit()


class StockPopup(Popup):
    t = None
    def __init__(self, **kwargs):
        super(StockPopup, self).__init__(**kwargs)
        self.t = StockTextInput(on_text_validate=self.dismiss)
        self.t.bind(on_text_validate=self.t.update_stock)
        h = BoxLayout(orientation='horizontal')
        v = BoxLayout(orientation='vertical')
        n = Button(text='No', size_hint_x=0.25)
        yes_btn = Button(text='Yes', size_hint_x=0.25)
        l = Label(text='Commit changes to database?', size_hint_x=0.5)
        self.title = "What is the new Stock count?"
        h.add_widget(l)
        h.add_widget(yes_btn)
        h.add_widget(n)

        v.add_widget(self.t)
        v.add_widget(h)

        self.add_widget(v)

        n.bind(on_press=self.some_function)
        n.bind(on_release=self.dismiss)
        yes_btn.bind(on_press=self.t.update_stock)
        yes_btn.bind(on_release=self.dismiss)

    def some_function(self, obj):
        self.t.text = MyScreenManager.info.stock
        print('Pressed the no button')




class PriceTextInput(TextInput):
    def update_price(self, obj):
        with conn:
            c = conn.cursor()
            pid = str(MyScreenManager.info.pid)
            new = str(self.text)
            c.execute("UPDATE Inventory SET Price= ? WHERE ID = ?", (new, pid))
            conn.commit()

class PricePopup(Popup):

    t = None
    def __init__(self, **kwargs):
        super(PricePopup, self).__init__(**kwargs)
        self.t = PriceTextInput(on_text_validate=self.dismiss)
        self.t.bind(on_text_validate=self.t.update_price)
        h = BoxLayout(orientation='horizontal')
        v = BoxLayout(orientation='vertical')
        n = Button(text='No', size_hint_x=0.25)
        yes_btn = Button(text='Yes', size_hint_x=0.25)
        l = Label(text='Commit changes to database?', size_hint_x=0.5)
        self.title = "What is the new Price?"
        h.add_widget(l)
        h.add_widget(yes_btn)
        h.add_widget(n)

        v.add_widget(self.t)
        v.add_widget(h)

        self.add_widget(v)

        n.bind(on_press=self.some_function)
        n.bind(on_release=self.dismiss)
        yes_btn.bind(on_press=self.t.update_price)
        yes_btn.bind(on_release=self.dismiss)

    def some_function(self, obj):
        self.t.text = MyScreenManager.info.price
        print('Pressed the no button')

class MyImage(Image):
    pass
class MyRefreshButton(Button):
    pass

class DetailPartView(BoxLayout):
    def __init__(self, **kwargs):
        super(DetailPartView, self).__init__(**kwargs)

        self.orientation = "vertical"
        b = BoxLayout(orientation='horizontal')
        v = BoxLayout(orientation='vertical', size_hint_x=0.70)
        g = GridLayout(cols=2)

        details = Details(size_hint_x=0.3)

        part_btn = Button(text='Change Part Number')
        desc_btn = Button(text='Change Description')
        stock_btn = Button(text='Update Quantity')
        price_btn = Button(text='Adjust Price')
        pic_btn = Button(text='Doesn\'t do anything')
        back_btn = MyBackButton()

        pic = MyImage()

        part_lbl = PartLabel()
        part_popup = PartNumPopup()
        print("part_popup.t.text = "+part_popup.t.text)
        part_popup.t.bind(text=part_lbl.setter('text'))

        category_lbl = CategoryLabel()

        desc_lbl = DescLabel()
        desc_popup = DescPopup()
        print("popup.t.text = "+desc_popup.t.text)
        desc_popup.t.bind(text=desc_lbl.setter('text'))

        stock_lbl = StockLabel()
        stock_popup = StockPopup()
        print("popup.t.text = "+stock_popup.t.text)
        stock_popup.t.bind(text=stock_lbl.setter('text'))

        price_lbl = PriceLabel()
        price_popup = PricePopup()
        print("popup.t.text = "+price_popup.t.text)
        price_popup.t.bind(text=price_lbl.setter('text'))

        total_lbl = TotalLabel()
        print('MyScreenManager.info.stock'+ MyScreenManager.info.stock, MyScreenManager.info.price)

        part_btn.bind(on_press=part_popup.open)
        desc_btn.bind(on_press=desc_popup.open)
        stock_btn.bind(on_press=stock_popup.open)
        price_btn.bind(on_press=price_popup.open)
        # pic_btn.bind(on_press=self.go_back)
        back_btn.bind(on_press=self.go_back)
        # part_btn.bind(on_press=self.change_quantity)

        v.add_widget(part_lbl)
        v.add_widget(category_lbl)
        v.add_widget(desc_lbl)
        v.add_widget(stock_lbl)
        v.add_widget(price_lbl)
        v.add_widget(total_lbl)


        b.add_widget(details)
        b.add_widget(v)
        b.add_widget(pic)

        g.add_widget(part_btn)
        g.add_widget(desc_btn)
        g.add_widget(stock_btn)
        g.add_widget(price_btn)
        g.add_widget(pic_btn)
        g.add_widget(back_btn)

        self.add_widget(b)
        self.add_widget(g)



    def go_back(self, instance):
        print('test', instance)
        self.clear_widgets


    def change_picture(self, obj):
        print("no camera yet")


class SearchScreen(Screen):
    def search_word(self):
        self.clear_widgets()
        self.add_widget(SearchForm())


class ResultsScreen(Screen):
    def show_results(self):
        self.clear_widgets()        # need to add a go back here
        self.add_widget(DetailPartView())

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

            self.info.pid = str(part[0])
            print(self.info.pid,"this is the screenmanager button pid")
            self.info.part_number = str(part[1])
            self.info.category = str(part[2])
            self.info.description = str(part[3])
            self.info.stock = str(part[4])
            self.info.price = str(part[5])
            self.info.percent = str(part[6])


class MainApp(App):
    def build(self):
        x = MyScreenManager()
        return x

print("Connecting to database...")
conn = sqlite3.connect('inventory.db')


if __name__ == '__main__':
    MainApp().run()


conn.close
print("closing database")
