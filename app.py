import csv
import tkinter as tk
import tkinter.messagebox
from datetime import datetime
from functools import partial
from tkinter import *

from Classes import *

user_list = []
product_list = []
sale_records = []
giftCards = []
currentUser = None
drawerTotal = 0


def clockOut(user):
    clock_in_time = datetime.strptime(user.clock_in, '%H:%M')
    hoursWorked = datetime.now() - clock_in_time
    hoursWorked = round(hoursWorked.total_seconds() / 3600)
    user.hoursWorked += hoursWorked


def saveData():
    with open('csv_files/user_file.csv', mode='w', newline='') as user_file:
        fieldnames = ['user_id', 'name', 'pin', 'accessLevel', 'payrate', 'hoursWorked', 'clock-in']

        user_writer = csv.writer(user_file)
        user_writer.writerow(fieldnames)
        for user in user_list:
            user_writer.writerow(
                (user.user_id, user.name, user.pin, user.accessLevel, user.payrate, user.hoursWorked, user.clock_in))
    with open('csv_files/product_file.csv', mode='w', newline='') as product_file:
        fieldnames = ['product_id', 'name', 'price', 'costToMake', 'tax']

        product_writer = csv.writer(product_file)
        product_writer.writerow(fieldnames)
        for product in product_list:
            product_writer.writerow((product.product_id, product.name, product.price, product.costToMake))
    with open('csv_files/giftcards_file.csv', mode='w', newline='') as giftcards_file:
        fieldnames = ['cardNum', 'startAmount', 'currentBalance']

        giftcard_writer = csv.writer(giftcards_file)
        giftcard_writer.writerow(fieldnames)
        for cards in giftCards:
            giftcard_writer.writerow((cards.cardNum, cards.startAmount, cards.currentBalance))


with open('csv_files/sales_file.csv', mode='w', newline='') as sales_file:
    fieldnames = ['checkNum', 'date', 'time', 'products', 'user', 'paymentType', 'paymentAmount', 'tax', 'discount',
                  'refunded']

    sales_writer = csv.writer(sales_file)
    sales_writer.writerow(fieldnames)
    for sale in sale_records:
        sales_writer.writerow((sale.checkNum, sale.date, sale.time, sale.products, sale.user, sale.paymentType,
                               sale.paymentAmount, sale.tax, sale.discount, sale.refunded))


def readData():
    with open('csv_files/user_file.csv', 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        fields = []
        rows = []
        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
        for row in rows:
            user_list.append(User(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    with open('csv_files/product_file.csv', 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        fields = []
        rows = []
        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
        for row in rows:
            product_list.append(Product(row[0], row[1], row[2], row[3]))
    with open('csv_files/sales_file.csv', 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        fields = []
        rows = []
        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
        for row in rows:
            sale_records.append(Sale(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
    with open('csv_files/giftcards_file.csv', 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        fields = []
        rows = []
        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
        for row in rows:
            giftCards.append(GiftCard(row[0], row[1], row[2]))


top = tk.Tk()
top.title("Welcome to SureCharge")
top.geometry("380x400")
readData()
saveData()
sale_items = []

# Frames for switching screens
homeScrn = Frame(top)
saleScrn = Frame(top)
payScrn = Frame(top)
addUserScrn = Frame(top)


def updateCheckNum():
    highest = 0
    for sales in sale_records:
        if 0 > highest:
            highest = sales.checkNum
            return highest + 1


def updateUserId():
    highest = 0
    for user in user_list:
        if int(user.user_id) > highest:
            highest = int(user.user_id)
    return highest + 1


def addToSale(product):
    sale_items.append(product)


def removeFromSale(product):
    global payScrn
    sale_items.remove(product)
    payScrn.destroy()
    payScrn = Frame(top)
    paymentScreen()


def exit():
    top.destroy()
    saveData()
    readData()


def saleTotal():
    total = 0
    for items in sale_items:
        total = float(items.price) + total
    return total


def cashSale(total, tax, discount):
    global drawerTotal
    item_list = ''
    drawerTotal = drawerTotal + total
    for items in sale_items:
        item_list = item_list + "(" + items.product_id + ") "
    sale_records.append(
        Sale(1, datetime.now().date(), datetime.now().time(), item_list, currentUser.name, 'Cash',
             total,
             tax, discount, 0))
    saveData()
    readData()
    print(sale_records[0].products)


def signin(en):
    pin = en.get()
    print(pin)
    global currentUser
    found = False
    for user in user_list:
        if int(user.pin) == int(pin):
            currentUser = user
            found = True
            salesScreen()
    if not found:
        tk.messagebox.showwarning("Invalid Pin", "Invalid Pin")


def createUser(E1, E2, E3, E4):
    global user_list
    user_id_ = updateUserId()
    name = E1.get()
    pin = E2.get()
    accessLevel = E3.get()
    if accessLevel == 'Admin':
        accessLevelNum = 0
    else:
        accessLevelNum = 1
    payRate = E4.get()
    inUse = False
    for user in user_list:
        if user.pin == pin:
            inUse = True
            tk.messagebox.showwarning("Invalid Pin", "Pin is already in Use!\nPlease Try Again")
    if payRate == '' or name == '' or pin == '' or accessLevel == '':
        tk.messagebox.showwarning("Invalid Entry", "One of your entries are blank!\nPlease Try Again")
    elif int(pin) < 999:
        tk.messagebox.showwarning("Invalid Entry", "The pin must be a minimum of 4 digits\nPlease Try Again")
    else:
        if not inUse:
            user_list.append(User(user_id_, name, pin, accessLevelNum, payRate, 0, 0))
            saveData()
            tk.messagebox.showwarning("Success!", (
                    name + " Was added! \nPin: " + pin + "\nAccessLevel: " + accessLevel + "\nPay Rate:" + payRate))
            addUserScrn.pack_forget()
            salesScreen()


def homeScreen():
    L1 = Label(homeScrn, text="Pin")
    L1.pack(side=LEFT)
    E1 = Entry(homeScrn)
    E1.pack()
    SigninB = tk.Button(homeScrn, text="Sign In", command=partial(signin, E1))
    SigninB.pack()


def salesScreen():
    homeScrn.pack_forget()
    menubutton = Menubutton(saleScrn, text="Manager Menu")
    menubutton.menu = Menu(menubutton)
    menubutton["menu"] = menubutton.menu

    menubutton.menu.add_command(label="Add User",
                                command=addUser)
    menubutton.menu.add_command(label="Edit/Delete User",
                                command=None)  # TODO: Implement
    menubutton.menu.add_command(label="Add Product",
                                command=None)  # TODO: Implement
    menubutton.menu.add_command(label="Edit/Delete Product",
                                command=None)  # TODO: Implement
    menubutton.menu.add_command(label="Reports Screem",
                                command=None)  # TODO: Implement
    menubutton.pack()

    for product in product_list:
        button = tk.Button(saleScrn, text=product.name + "\n$" + product.price,
                           command=partial(addToSale, product))
        button.pack()
    B = tk.Button(saleScrn, text="Total", command=paymentScreen)
    B.pack()
    saleScrn.pack()


def addUser():
    saleScrn.pack_forget()
    payScrn.pack_forget()
    L1 = Label(addUserScrn, text="Name: ")
    E1 = Entry(addUserScrn)
    L1.pack()
    E1.pack()
    L2 = Label(addUserScrn, text="Pin: ")
    E2 = Entry(addUserScrn)
    L2.pack()
    E2.pack()
    L3 = Label(addUserScrn, text="Access Level: ")
    variable = StringVar(addUserScrn)
    variable.set("Basic")
    w = OptionMenu(addUserScrn, variable, "Basic", "Admin")
    L3.pack()
    w.pack()
    L4 = Label(addUserScrn, text="PayRate: ")
    E4 = Entry(addUserScrn)
    L4.pack()
    E4.pack()
    B1 = Button(addUserScrn, text="Save", command=partial(createUser, E1, E2, variable, E4))
    B1.pack()
    addUserScrn.pack()


def paymentScreen():
    saleScrn.pack_forget()
    payScrn.pack_forget()
    for items in sale_items:
        L1 = Label(payScrn, text=(items.name + items.price))
        L1.pack()
        B1 = Button(payScrn, text="Remove", command=(partial(removeFromSale, items)))
        B1.pack()
    subtotal = saleTotal()
    tax = subtotal * 0.07
    tax = round(tax, 2)
    total = subtotal + tax
    total = round(total, 2)
    print(total)
    B1 = Button(payScrn, text='Cash', command=partial(cashSale, total, tax,
                                                      0))  # TODO: Sales saving to sale_records but not writing to sales_file
    B1.pack()
    exit_button = Button(top, text="Exit", command=exit)
    exit_button.pack(pady=20)
    payScrn.pack()


homeScreen()
homeScrn.pack()
top.mainloop()
