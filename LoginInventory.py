print("Importing Modules...")
from openpyxl import load_workbook
import sqlite3
import csv
print("Modules imported.")


def page_names():
    print("Loading Excel Workbook...")
    book = load_workbook("LOGINinventory.xlsx")
    pages = book.get_sheet_names()
    print("Workbook loaded.")
    print("These are the pages...")
    print(pages)
    return pages

def choose_option():
    print("============================================================================")
    print("Welcome to the L.I.S.T")
    print("Choose an option to proceede")
    options = ("Query", "Update Existing", "Add/Remove Column", "Add/Remove Item", "Reports", "Count", "Quit")
    for thing in options:
        print options.index(thing), thing
    choice = int(raw_input("> "))
    return choice

def query():
    pn = str(raw_input("Give me the part number or just tell me what you are looking for.\n"))
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
    print("\nHere's what I found:")
    for res in results:
        Id, PartNum, SubCat, Desc, Stock, Price, Percent, Totdollars = res
        print("\nItem Id: %s \nPart Number: %s \nDescription: %s \nand you have %s in stock at %s each\nTotal value of %s") % (Id, PartNum, Desc, Stock, Price, Totdollars)

def update_existing():
    part = str(raw_input("I'm going to need the part number of the item.\n"))
    for row in c.execute("SELECT * FROM Inventory WHERE Part_Number=?", (part,)):
        Id, PartNum, SubCat, Desc, Stock, Price, Percent, Totdollars = row
        print("\nHere ya go..")
        print("Item Id: %s\nPart Number: %s\nSub Category: %s\nDescription: %s\nTotal in Stock: %s\nList Price: %s\nPercent of cost: %s\nTotal Value of Stock: %s") % (row)
    columns = ('Id', 'Part Number', 'Category', 'Description', 'Stock', 'Price', 'Percent', 'Value')
    print("\nWhat are changing about this item?")
    print("Choose a number")
    for x in columns:
        print columns.index(x), x
    col = int(raw_input("> "))
    new = "'"+raw_input("What is the new value?:  ")+"'"
    stack = columns[col]

#### this may be bad need to make more secure
    cmd = "UPDATE Inventory SET %s=%s WHERE Part_Number=%s" % (stack,new,part)
    c.execute(cmd)
    conn.commit()
    c.execute("SELECT * FROM Inventory WHERE Part_Number=?", (part,))

def create_database():
    print "Creating database..."
    conn = sqlite3.connect("inventory.db")
    print "Database created."
    print "Creating table..."

    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS Inventory")
    c.execute("CREATE TABLE Inventory(ID INTEGER PRIMARY KEY, Part_Number TEXT, Category TEXT, Description TEXT, Stock INTEGER, Price REAL, Percent INTEGER, Value REAL)")
    print "Done."
    print "Populating..."
    things = csv.reader(open('inserttestinventory.csv'))
    c.executemany("INSERT INTO Inventory (Part_Number, Category, Description, Stock, Price, Percent, Value) VALUES(?, ?, ?, ?, ?, ?, ?)", things)
    conn.commit()
    print "Finished. Closing connection"
    conn.close()

def add_remove_item():
    add_or_remove = str(raw_input("Are we going to add or remove something?   "))
    if "add" in add_or_remove:
        print "Gonna need some info from you."
        partnum = str(raw_input("What is the part number?    "))
        cat = str(raw_input("What category are we putting it in?    "))
        desc = str(raw_input("Tell me about it. Common names, uses, and measurements    "))
        stk = int(raw_input("How many of them do you have?    "))
        lprice = float(raw_input("What is the list price per unit?    "))
        ofcost = int(raw_input("What percent of cost do we pay?    "))
        val = float(raw_input("I really should calculate this for you, I just don't know how yet. So for now just gimme something.   "))

        new_item = (partnum, cat, desc, stk, lprice, ofcost, val)
        c.execute("INSERT INTO Inventory (Part_Number, Category, Description, Stock, Price, Percent, Value) VALUES(?, ?, ?, ?, ?, ?, ?)", new_item)
        conn.commit()
        lid = c.lastrowid
        print "The last Id of the inserted row is %d" % lid
    elif "re" in add_or_remove:
        partnum = str(raw_input("What is the part number?    "))
        c.execute("SELECT * FROM Inventory WHERE Part_Number=?", (partnum,))
        results = c.fetchone()
        print("\nHere's what I found:")
        Id, PartNum, SubCat, Desc, Stock, Price, Percent, Totdollars = results
        print("\nItem Id: %s \nPart Number: %s \nDescription: %s \nand you have %s in stock at %s each\nTotal value of %s") % (Id, PartNum, Desc, Stock, Price, Totdollars)
        print "This the right one?"
        pick = raw_input(" ")
        if "y" in pick:
            c.execute("DELETE FROM Inventory WHERE Part_Number =?", (partnum,))
            conn.commit()
        else:
            print "Dunno how we got here.."

def xport_csv():
    with open('fromLIST.csv', 'wb') as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerow(['Id', 'Part_Number', 'Sub_Category', 'Description', 'Stock', 'List_Price', 'Percent_Value', 'Value'])
        for row in c.execute('SELECT * FROM Inventory'):
            writer.writerow(row)


#create_database()
print("Loading Database...")
conn = sqlite3.connect("inventory.db")
c = conn.cursor()
print("Database opened successfully.")


while True:
    choice = choose_option()
    if choice == 0:
        print "Search thru database returning all results"
        query()

    if choice == 1:
        print "Update existing entry, changing any value in any column"
        update_existing()

    if choice == 2:
        print "Add/Remove column"

        columns = ('Id', 'Part_Number', 'Sub_Category', 'Description', 'Stock', 'List_Price', 'Percent_Value', 'Value')


    if choice == 3:
        print "Add/Remove item"
        add_remove_item()
        ## want to end up with:
            # scan barcode --> check all ok
            # select add or remove from database
            # update database

    if choice == 4:
        print("Export Inventory as .csv file")
        xport_csv()


    if choice == 5:
        print("""open camera on client to scan barcodes
            each scan ==> prompt "How many?" input from keyboard or from voice
            all items saved to secondary database
            verify to use new database""")

    if choice == 6:
        conn = sqlite3.connect("second.db")
        cur = conn.cursor()
        conn.close
        print("Database disconnected.")
        print("Completed")
        quit()
