from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import time
import random
from openpyxl import load_workbook
import sqlite3
import csv





class LoginScreen(Screen):
    def creds(self):
        if self.ids['uname'].text == "a" and self.ids['pword'].text == "a":
            print("We caught it")
            self.parent.current = 'select'


class SelectScreen(Screen):
    pass

class SearchScreen(Screen):

    def query(self):
        with conn:
            c = conn.cursor()
            pn = self.ids['pn'].text
            print((self.ids['pn'].text) + 'HERE I AM')
            # pn = str(input("Give me the part number or just tell me what you are looking for.\n"))
            discriptors = pn.split()
            nums = len(discriptors)
            things = ""
            l = ""
            for word in discriptors:
                if word != discriptors[nums-1]:
                    l += "'%"+word + "%' AND Description LIKE "
                else:
                    l += "'%"+word+"%'"
            c.execute("SELECT * FROM Inventory WHERE Description LIKE "+l+" OR Part_Number=?", (pn,))
            results = c.fetchall()


            if results != []:
                print("\nHere's what I found:")
                for res in results:
                    if res in results:
                        # something = ResultsScreen()
                        # self.add_widget(something)
                        self.current = 'results'

                        Id, PartNum, SubCat, Desc, Stock, Price, Percent, Totdollars = res
                        print(("\nItem Id: %s \nPart Number: %s \nDescription: %s \nand you have %s in stock at %s each\nTotal value of %s") % (Id, PartNum, Desc, Stock, Price, Totdollars))



            if results == []:
                print("I can't seem to find that.")
            # return results

    # def results_return(self):
    #     name = str(time.time())
    #     for res in parent.query().results:
    #         s = Label(ids=['results'], text=res)
    #         self.add_widget(s)
    #         self.current = name

class UploadScreen(Screen):
    pass

class ScanScreen(Screen):
    pass

class ReportsScreen(Screen):
    pass

class SelectScreen(Screen):
    pass

class ResultsScreen(Screen):
    pass
        # color = ListProperty([1., 0., 0., 1.])

class MyScreenManager(ScreenManager):
    def new_results_screen(self):
        name = str(time.time())
        s = ResultsScreen(name=name)
        self.add_widget(s)
        self.current = name
    # def new_color_screen(self):
    #     name = str(time.time())
    #     s = ColorScreen(name=name, color=[random.random() for _ in range(3)] + [1])
    #     self.add_widget(s)
    #     self.current = name

    def page_names():
        print("Loading Excel Workbook...")
        book = load_workbook("LOGINinventory.xlsx")
        pages = book.get_sheet_names()
        print("Workbook loaded.")
        print("These are the pages...")
        print(pages)
        return pages

    def choose_option():
        print("=====================================================================")
        print("Welcome to the L.I.S.T")
        print("Choose an option to proceede")
        options = ("Query", "Update Existing", "Add/Remove Column", "Add/Remove Item", "Reports", "Count", "Import", "Quit")
        for thing in options:
            print(options.index(thing), thing)
        choice = int(input("> "))
        return choice


    def update_existing():
        with conn:
            c = conn.cursor()
            part = str(input("I'm going to need the part number of the item.\n"))
            for row in c.execute("SELECT * FROM Inventory WHERE Part_Number=?", (part,)):
                Id, PartNum, SubCat, Desc, Stock, Price, Percent, Totdollars = row
                print("\nHere ya go..")
                print(("Item Id: %s\nPart Number: %s\nSub Category: %s\nDescription: %s\nTotal in Stock: %s\nList Price: %s\nPercent of cost: %s\nTotal Value of Stock: %s") % (row))
            columns = ('Id', 'Part Number', 'Category', 'Description', 'Stock', 'Price', 'Percent', 'Value')
            print("\nWhat are changing about this item?")
            print("Choose a number")
            for x in columns:
                print(columns.index(x), x)
            col = int(input("> "))
            new = "'"+input("What is the new value?:  ")+"'"
            stack = columns[col]

        #### this may be bad need to make more secure
            cmd = "UPDATE Inventory SET %s=%s WHERE Part_Number=%s" % (stack,new,part)
            c.execute(cmd)
            conn.commit()
            c.execute("SELECT * FROM Inventory WHERE Part_Number=?", (part,))

    def create_table(csvfile):
        try:
            print("Creating table...")
            c = conn.cursor()
            c.execute("DROP TABLE IF EXISTS Inventory")
            c.execute("CREATE TABLE Inventory(ID INTEGER PRIMARY KEY, Part_Number TEXT, Category TEXT, Description TEXT, Stock INTEGER, Price REAL, Percent INTEGER, Value REAL)")
            print("Done.")
            print("Importing data now...")
    ## the inport happens here:
            things = csv.reader(open(csvfile))
            c.executemany("INSERT INTO Inventory (Part_Number, Category, Description, Stock, Price, Percent, Value) VALUES(?, ?, ?, ?, ?, ?, ?)", things)
            conn.commit()
        except sqlite3.Error:
            if conn:
                conn.rollback()
            print("Error %s:" % sqlite3.Error)
            sys.exit(1)
        finally:
            if conn:
                print("Data imported.")

    def add_remove_item():
        with conn:
            c = conn.cursor()
            add_or_remove = str(input("Are we going to add or remove something?   "))
            if "add" in add_or_remove:
                print("Gonna need some info from you.")
                partnum = str(input("What is the part number?    "))
                cat = str(input("What category are we putting it in?    "))
                desc = str(input("Tell me about it. Common names, uses, and measurements    "))
                stk = int(input("How many of them do you have?    "))
                lprice = float(input("What is the list price per unit?    "))
                ofcost = int(input("What percent of cost do we pay?    "))
                val = float(input("I really should calculate this for you, I just don't know how yet. So for now just gimme something.   "))

                new_item = (partnum, cat, desc, stk, lprice, ofcost, val)
                c.execute("INSERT INTO Inventory (Part_Number, Category, Description, Stock, Price, Percent, Value) VALUES(?, ?, ?, ?, ?, ?, ?)", new_item)
                conn.commit()
                lid = c.lastrowid
                print("The last Id of the inserted row is %d" % lid)
            elif "re" in add_or_remove:
                partnum = str(input("What is the part number?    "))
                c.execute("SELECT * FROM Inventory WHERE Part_Number=?", (partnum,))
                results = c.fetchone()
                print("\nHere's what I found:")
                Id, PartNum, SubCat, Desc, Stock, Price, Percent, Totdollars = results
                print(("\nItem Id: %s \nPart Number: %s \nDescription: %s \nand you have %s in stock at %s each\nTotal value of %s") % (Id, PartNum, Desc, Stock, Price, Totdollars))
                print("This the right one?")
                pick = input(" ")
                if "y" in pick:
                    c.execute("DELETE FROM Inventory WHERE Part_Number =?", (partnum,))
                    conn.commit()
                else:
                    print("Dunno how we got here..")

    def xport_csv():
        with open('fromLIST.csv', 'wb') as f:
            writer = csv.writer(f, delimiter=' ')
            writer.writerow(['Id', 'Part_Number', 'Sub_Category', 'Description', 'Stock', 'List_Price', 'Percent_Value', 'Value'])
            for row in c.execute('SELECT * FROM Inventory'):
                writer.writerow(row)









root_widget = Builder.load_string('''
MyScreenManager:
    LoginScreen:
    SelectScreen:
    SearchScreen:
    UploadScreen:
    ScanScreen:
    ReportsScreen:
    ResultsScreen:

<LoginScreen>:
    name: 'login'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Welcome to the L.I.S.T."
            font_size: 30
        Image:
            source: 'logo.png'
            allow_stretch: True
            keep_ratio: True
        BoxLayout:
            Label:
                text: "Username"
                font_size: 30
            TextInput:
                id: uname
                text_hint: 'Username'
                multiline: False
            Label:
                text: "Password"
                font_size: 30

            TextInput:
                id: pword
                multiline: False
                password: True

            Button:
                text: 'Login'
                font_size: 30
                on_release: root.creds()


<SelectScreen>:
    name: 'select'
    GridLayout:
        cols: 2
        padding: 25, 25, 25, 25
        spacing: 25, 25
        Button:
            text: "Search"
            font_size: 20
            on_release: app.root.current  = "search"
        Button:
            text: "Upload"
            font_size: 20
            on_release: app.root.current  = "upload"
        Button:
            text: "Scan"
            font_size: 20
            on_release: app.root.current  = "scan"
        Button:
            text: "Reports"
            font_size: 20
            on_release: app.root.current  = "reports"
        Button:
            text: "Quit"
            font_size: 20
            on_release: app.get_running_app().stop()

<SearchScreen>:
    name: 'search'
    BoxLayout
        orientation: 'vertical'
        TextInput:
            id: pn
            name: 'pn'
            text: 'Give me the part number or just tell me what you are looking for.'

        Button:
            text: "search"
            font_size: 20
            on_release: root.query(), app.root.new_results_screen()

        Button:
            text: "Go Back"
            font_size: 20
            on_release: app.root.current = "select"



<UploadScreen>:
    name: 'upload'
    FloatLayout:
        Label:
            pos_hint: {'center_x':.5, 'center_y':1}
            text_size: (self.width*.5), self.height
            text: "This will be the upload screen where you grab the most current database from somewhere and start the actual program with that db."

    FloatLayout:
        Button:
            text: "Go Back"
            size_hint: 0.12, 0.1
            font_size: 20
            pos_hint: {'center_x':.5, 'center_y':.1}
            on_release: app.root.current = "select"

<ScanScreen>:
    name: 'scan'
    FloatLayout:
        Label:
            pos_hint: {'center_x':.5, 'center_y':1}
            text_size: (self.width*.5), self.height
            text: "This will open up the camera utility and will scan barcodes to count or to find in inventory.  If not found ask to add, then pull info and populate an item page."
    FloatLayout:
        Button:
            text: "Go Back"
            size_hint: 0.12, 0.1
            font_size: 20
            pos_hint: {'center_x':.5, 'center_y':.1}
            on_release: app.root.current = "select"


<ReportsScreen>:
    name: 'reports'
    canvas:
    FloatLayout:
        Label:
            pos_hint: {'center_x':.5, 'center_y':1}
            text_size: (self.width*.5), self.height
            text: "Will print out pull sheets, cycle counts, total inventory, and maybe the spec sheets."
    FloatLayout:
        Button:
            text: "Go Back"
            size_hint: 0.12, 0.1
            font_size: 20
            pos_hint: {'center_x':.5, 'center_y':.1}
            on_release: app.root.current = "select"


<ResultsScreen>:
    name: 'results'
    id: results

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "need to display results here.. Figure it out!"
            font_size: 30

        BoxLayout:
            Button:
                text: 'Return to Select screen'
                size_hint: 0.12, 0.1
                font_size: 30
                on_release: app.root.current = 'select'


''')

class ScreenManagerApp(App):
    def build(self):
        return root_widget


print("Loading Database...")
conn = sqlite3.connect("inventory.db")
print("Database opened successfully.")



ScreenManagerApp().run()
