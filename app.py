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
stored_sale = None
giftCards = []
currentUser = None
drawerTotal = 0

top = tk.Tk()
top.title("Welcome to SureCharge")
top.state('zoomed')

sale_items = []
screens = []
# Frames for switching screens
homeScrn = Frame(top)
saleScrn = Frame(top)
payScrn = Frame(top)
addUserScrn = Frame(top)
editUserScrn = Frame(top)
editSingleUserScrn = Frame(top)
addProductScrn = Frame(top)
editProductScrn = Frame(top)

screens.append(homeScrn)
screens.append(saleScrn)
screens.append(payScrn)
screens.append(addUserScrn)
screens.append(editUserScrn)
screens.append(editSingleUserScrn)
screens.append(addProductScrn)
screens.append(editProductScrn)


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


readData()
saveData()


def logout():
    global currentUser
    currentUser = None
    clear_frame()
    homeScreen()


def clockOut():
    global currentUser
    clock_in_time = datetime.strptime(currentUser.clock_in, '%Y-%m-%d, %H:%M:%S')
    hoursWorked = datetime.now() - clock_in_time
    hoursWorked = round(hoursWorked.total_seconds() / 3600, 2)
    currentUser.hoursWorked = round(hoursWorked + float(currentUser.hoursWorked), 2)
    currentUser.clock_in = '0'
    saveData()
    homeScreen()


def clockIn():
    global currentUser
    currentUser.clock_in = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    saveData()
    salesScreen()


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


def checkAdmin():
    # added as a fail-safe incase Admin User is deleted for any reason
    global user_list
    found = False
    for user in user_list:
        if user.name == 'Admin' and user.accessLevel == '0' and user.user_id == '0':
            found = True
    if found == False:
        user_list.append(User(0, 'Admin', 9999, '0', '20', '0', '0'))
        saveData()


checkAdmin()


def updateProductId():
    highest = 0
    for product in product_list:
        if int(product.product_id) > highest:
            highest = int(product.product_id)
    return highest + 1


def addToSale(product):
    sale_items.append(product)
    clear_frame()
    salesScreen()


def removeFromSale(product, num):
    global payScrn
    sale_items.remove(product)
    clear_frame()
    clear_frame()
    if num == 1:
        paymentScreen()
    else:
        salesScreen()


def exit():
    top.destroy()
    saveData()
    readData()


def saleTotal():
    total = 0
    for items in sale_items:
        total = float(items.price) + total
    return total


def cashSale(total, tax, discount):  # TODO: Not Working
    global currentUser
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
        if user.name == name:
            inUse = True
            tk.messagebox.showwarning("Invalid Name", "Another user has the same name!\nTry adding a last initial😊")
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


def selectEditUserScreen():
    clear_frame()
    button = Button(editUserScrn, text='Home', command=salesScreen)
    button.pack()
    for user in user_list:
        button = tk.Button(editUserScrn, text=(str(user.user_id) + "\n" + user.name),
                           command=partial(editSingleUser, user))
        button.pack()
    editUserScrn.pack()


def clear_frame():
    global screens
    for frame in screens:
        frame.pack_forget()
        for widgets in frame.winfo_children():
            widgets.pack_forget()


def editSingleUser(user):
    clear_frame()
    button = Button(editSingleUserScrn, text='Home', command=salesScreen)
    button.pack()
    L1 = Label(editSingleUserScrn, text="Name: ")
    E1 = Entry(editSingleUserScrn)
    E1.insert(0, user.name)

    L2 = Label(editSingleUserScrn, text="Pin: ")
    E2 = Entry(editSingleUserScrn)
    E2.insert(0, user.pin)
    if user.name == 'Admin' and user.user_id == '0':
        E1.config(state=DISABLED)
        E2.config(state=DISABLED)
    L1.pack()
    E1.pack()
    L2.pack()
    E2.pack()
    L3 = Label(editSingleUserScrn, text="Access Level: ")
    variable = StringVar(editSingleUserScrn)
    if user.accessLevel == '0':
        variable.set("Admin")
    else:
        variable.set("Basic")
    E3 = OptionMenu(editSingleUserScrn, variable, "Basic", "Admin")
    if user.name != 'Admin' and user.user_id != '0':
        L3.pack()
        E3.pack()
    L4 = Label(editSingleUserScrn, text="PayRate: ")
    E4 = Entry(editSingleUserScrn)
    E4.insert(0, user.payrate)
    L4.pack()
    E4.pack()
    L5 = Label(editSingleUserScrn, text="Clock In Time: ")
    E5 = Entry(editSingleUserScrn)
    E5.insert(0, user.clock_in)
    L5.pack()
    E5.pack()
    L6 = Label(editSingleUserScrn, text="Hours Worked:")
    E6 = Entry(editSingleUserScrn)
    E6.insert(0, user.hoursWorked)
    L6.pack()
    E6.pack()
    B1 = Button(editSingleUserScrn, text='Save', command=partial(editUser, E1, E2, variable, E4, E5, E6, user))
    B1.pack()
    if user.user_id != '0' and user.name != 'Admin':
        B2 = Button(editSingleUserScrn, text='Delete', command=partial(deleteUser, user))
        B2.pack()
    Warning = Label(editSingleUserScrn, text='Warning: Please use the "Y-m-d, H:M:S" format for changing clock in time')
    Warning.pack()
    editSingleUserScrn.pack()


def deleteUser(user):
    global user_list
    user_list.remove(user)
    clear_frame()
    saveData()
    selectEditUserScreen()


def addProductScreen():
    clear_frame()
    button = Button(addProductScrn, text='Home', command=salesScreen)
    button.pack()
    L1 = Label(addProductScrn, text="Name:")
    E1 = Entry(addProductScrn)
    L1.pack()
    E1.pack()
    L2 = Label(addProductScrn, text="Price:")
    E2 = Entry(addProductScrn)
    L2.pack()
    E2.pack()
    L3 = Label(addProductScrn, text="Cost To Make:")
    E3 = Entry(addProductScrn)
    L3.pack()
    E3.pack()
    B1 = Button(addProductScrn, text='Save', command=partial(addProduct, E1, E2, E3))
    B1.pack()
    addProductScrn.pack()


def addProduct(E1, E2, E3):
    global product_list
    name = E1.get()
    price = E2.get()
    costToMake = E3.get()
    product_list.append(Product(updateProductId(), name, price, costToMake))
    saveData()
    salesScreen()


def selectEditProduct():
    clear_frame()
    button = Button(editProductScrn, text='Home', command=salesScreen)
    button.pack()
    global product_list
    for product in product_list:
        B1 = Button(editProductScrn, text=(product.product_id + "\n" + product.name),
                    command=partial(editProductScreen, product))
        B1.pack()
    editProductScrn.pack()


def editProductScreen(product):
    global product_list
    clear_frame()
    button = Button(editProductScrn, text='Home', command=salesScreen)
    button.pack()
    L1 = Label(editProductScrn, text="Name:")
    E1 = Entry(editProductScrn)
    E1.insert(0, product.name)
    L1.pack()
    E1.pack()
    L2 = Label(editProductScrn, text="Price:")
    E2 = Entry(editProductScrn)
    E2.insert(0, product.price)
    L2.pack()
    E2.pack()
    L3 = Label(editProductScrn, text="Cost To Make:")
    E3 = Entry(editProductScrn)
    E3.insert(0, product.costToMake)
    L3.pack()
    E3.pack()
    B1 = Button(editProductScrn, text='Save', command=partial(editProduct, E1, E2, E3, product))
    B1.pack()
    B2 = Button(editProductScrn, text='Delete', command=partial(deleteProduct, product))
    B2.pack()
    editProductScrn.pack()


def editProduct(E1, E2, E3, product):
    name = E1.get()
    price = E2.get()
    costToMake = E3.get()
    if name == '' or price == '' or costToMake == '':
        tk.messagebox.showwarning("Empty", "Error: one or more text field is empty")
    else:
        product.name = E1
        product.price = price
        product.costToMake = costToMake
        saveData()
        clear_frame()
        salesScreen()


def deleteProduct(product):
    global product_list
    product_list.remove(product)
    saveData()
    clear_frame()
    salesScreen()


def editUser(E1, E2, E3, E4, E5, E6, user):
    name = E1.get()
    pin = E2.get()
    accessLevel = E3.get()
    if accessLevel == 'Admin':
        accessLevelNum = 0
    else:
        accessLevelNum = 1
    payRate = E4.get()
    clock_in = E5.get()
    hoursWorked = E6.get()
    inUse = False
    for otherUser in user_list:
        if otherUser.pin == pin and user.user_id != otherUser.user_id:
            inUse = True
            tk.messagebox.showwarning("Invalid Pin", "Pin is already in Use!\nPlease Try Again")
        if otherUser.name == name and user.user_id != otherUser.user_id:
            inUse = True
            tk.messagebox.showwarning("Invalid Name", "Another user has the same name!\nTry adding a last initial😊")
    if payRate == '' or name == '' or pin == '' or accessLevel == '':
        tk.messagebox.showwarning("Invalid Entry", "One of your entries are blank!\nPlease Try Again")
    elif int(pin) < 999:
        tk.messagebox.showwarning("Invalid Entry", "The pin must be a minimum of 4 digits\nPlease Try Again")
    else:
        if not inUse:
            user.name = name
            user.pin = pin
            user.accessLevel = accessLevelNum
            user.payrate = payRate
            user.clock_in = clock_in
            user.hoursWorked = hoursWorked
            saveData()
            salesScreen()


def homeScreen():
    clear_frame()
    L1 = Label(homeScrn, text="Pin")
    L1.pack(side=LEFT)
    E1 = Entry(homeScrn)
    E1.pack()
    SigninB = tk.Button(homeScrn, text="Sign In", command=partial(signin, E1))
    SigninB.pack()
    homeScrn.pack()


def clearSale():
    global sale_items
    sale_items = []
    clear_frame()
    salesScreen()


def salesScreen():
    global currentUser
    global screens
    clear_frame()
    frames = []

    salesFrame = Frame(saleScrn)
    itemsFrame = Frame(saleScrn)
    menuFrame = Frame(saleScrn)
    totalFrame = Frame(saleScrn)
    # itemsFrame.grid(row=1, column=0)
    # salesFrame.grid(row=1, column=1)
    # menuFrame.grid(row=0, column=0)
    # totalFrame.grid(row=2, column=2)
    frames.append(salesFrame)
    frames.append(itemsFrame)
    frames.append(menuFrame)
    frames.append(totalFrame)
    h = Scrollbar(salesFrame, orient='horizontal')
    if currentUser.clock_in != '0':
        menubutton = Menubutton(menuFrame, text="Manager Menu")
        menubutton.menu = Menu(menubutton)
        menubutton["menu"] = menubutton.menu

        menubutton.menu.add_command(label="Add User",
                                    command=addUser)
        menubutton.menu.add_command(label="Edit/Delete User",
                                    command=selectEditUserScreen)
        menubutton.menu.add_command(label="Add Product",
                                    command=addProductScreen)
        menubutton.menu.add_command(label="Edit/Delete Product",
                                    command=selectEditProduct)
        menubutton.menu.add_command(label="Reports Screem",
                                    command=None)  # TODO: Implement
        if currentUser.accessLevel == '0':
            menubutton.pack(side=TOP)
            # menubutton.grid(row=0, column=0)
        clr_sale = Button(menuFrame, text='Clear Sale', command=clearSale)
        clr_sale.pack(side=BOTTOM)
        # clr_sale.grid(row=3, column=3)
        B1 = Button(menuFrame, text='Clock Out', command=clockOut)
        B1.pack(side=RIGHT)
        # B1.grid(row=1, column=0)
        B2 = Button(menuFrame, text='Sign Out', command=logout)
        B2.pack(side=LEFT)
        # B2.grid(row=2, column=0)
        # menuFrame.grid_columnconfigure(3, weight=2)
        row = 4
        for product in product_list:
            button = tk.Button(itemsFrame, text=product.name + "\n$" + product.price,
                               command=partial(addToSale, product))
            # button.pack(side=LEFT)
            button.grid(row=row, column=0)
            row = row + 1
        row = 4
        for items in sale_items:
            L1 = Label(salesFrame, text=(items.name + ' $' + items.price))
            # L1.pack(side=RIGHT)
            L1.grid(row=row, column=1)
            row = row + 1
            B1 = Button(salesFrame, text="Remove", command=(partial(removeFromSale, items, 0)))
            # B1.pack(side=RIGHT)
            B1.grid(row=row, column=1)
            row = row + 1
        if saleTotal() < 0 and currentUser.accessLevel != '0':
            Manager_Alert = Label(totalFrame, text='Total is Below 0, Please have a manager Login to finish the '
                                                   'transaction or clear sale.')
            Manager_Alert.pack()
            # Manager_Alert.grid(row=row, column=2)
            swtch_user = Button(totalFrame, text='Switch User', command=homeScreen)
            swtch_user.pack()
            # swtch_user.grid(row=row, column=2)
        else:
            B = tk.Button(totalFrame, text="Total", command=paymentScreen)
            B.pack(side=TOP)
            # B.grid(row=row, column=2)
        # saleScrn.grid(row=row, column=9)
        totalFrame.pack(side=BOTTOM)
        menuFrame.pack(side=TOP)
        itemsFrame.pack(side=LEFT,pady=10,padx=10,expand=FALSE)
        salesFrame.pack(side=RIGHT,pady=10,padx=10,expand=FALSE)
        saleScrn.pack()
    else:
        button = Button(saleScrn, text='Cancel', command=homeScreen)
        button.pack()
        L1 = Label(saleScrn, text='Please Clock in')
        B1 = Button(saleScrn, text='Clock In', command=clockIn)
        L1.pack()
        B1.pack()
        saleScrn.pack()


def addUser():
    clear_frame()
    button = Button(addUserScrn, text='Home', command=salesScreen)
    button.pack()
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
    clear_frame()
    button = Button(payScrn, text='Home', command=salesScreen)
    button.pack()
    for items in sale_items:
        L1 = Label(payScrn, text=(items.name + ' $' + items.price))
        L1.pack()
        B1 = Button(payScrn, text="Remove", command=(partial(removeFromSale, items, 1)))
        B1.pack()
    subtotal = saleTotal()
    Subtotal_Label = Label(payScrn, text=('Subtotal: $' + str(subtotal)))
    Subtotal_Label.pack()
    tax = subtotal * 0.07
    tax = round(tax, 2)
    Tax_Label = Label(payScrn, text=('Tax: $' + str(tax)))
    Tax_Label.pack()
    total = subtotal + tax
    total = round(total, 2)
    Total_Label = Label(payScrn, text=('Total: $' + str(total)))
    Total_Label.pack()
    # B1 = Button(payScrn, text='Cash', command=partial(cashSale, total, tax, 0))  # TODO: Sales saving to sale_records but not writing to sales_file
    # B1.pack()
    payScrn.pack()


homeScreen()
homeScrn.pack()
top.mainloop()
