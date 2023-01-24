import tkinter as tk
from tkinter import *
import csv
from tkinter import ttk

from Classes import *
from functools import partial
import tkinter.messagebox
from datetime import datetime

user_list = []
product_list = []
sale_records = []
giftCards = []
currentUser = None


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
            product_writer.writerow((product.product_id, product.name, product.price, product.costToMake, product.tax))
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
            product_list.append(Product(row[0], row[1], row[2], row[3], row[4]))
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


def addToSale(product):
    sale_items.append(product)


def printSale():
    total = 0.0
    for items in sale_items:
        total = float(total) + float(items.price)



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

def homeScreen():
    L1 = Label(top, text="Pin")
    L1.pack(side=LEFT)
    E1 = Entry(top)
    E1.pack()
    SigninB = tk.Button(top, text="Sign In", command=partial(signin, E1))
    SigninB.pack()


def salesScreen():
    for product in product_list:
        button = tk.Button(top, text=product.name + "\n$" + product.price,
                           command=partial(addToSale, product))
        button.pack()
    B = tk.Button(top, text="Total", command=printSale)
    B.pack()


homeScreen()
top.mainloop()
