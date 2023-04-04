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
currentUser = None
drawer = cashDrawer(0, 0, 0, 0, 0, 0, 0, 0, 0)
refundMode = False
top = tk.Tk()
top.title("Welcome to SureCharge")
top.state('zoomed')

sale_items = []
discounts_Applied = 0
drawer_record = []
discount_Record = []
screens = []
saved_orders = []
category_list = []
# Frames for switching screens
homeScrn = Frame(top)
saleScrn = Frame(top)
payScrn = Frame(top)
addUserScrn = Frame(top)
editUserScrn = Frame(top)
editSingleUserScrn = Frame(top)
addProductScrn = Frame(top)
editProductScrn = Frame(top)
addCategoryScrn = Frame(top)
editCategoryScrn = Frame(top)
selectReportsScrn = Frame(top)
drawerReportScrn = Frame(top)
itemSalesReportScrn = Frame(top)
salesReportScrn = Frame(top)
clockedInReportScrn = Frame(top)
discountReportScrn = Frame(top)
refundReportScrn = Frame(top)
drawerHistReportScrn = Frame(top)
payrollReportScrn = Frame(top)

screens.append(payrollReportScrn)
screens.append(homeScrn)
screens.append(saleScrn)
screens.append(payScrn)
screens.append(addUserScrn)
screens.append(editUserScrn)
screens.append(editSingleUserScrn)
screens.append(addProductScrn)
screens.append(editProductScrn)
screens.append(addCategoryScrn)
screens.append(editCategoryScrn)
screens.append(selectReportsScrn)
screens.append(drawerReportScrn)
screens.append(itemSalesReportScrn)
screens.append(salesReportScrn)
screens.append(clockedInReportScrn)
screens.append(discountReportScrn)
screens.append(refundReportScrn)
screens.append(drawerHistReportScrn)


def saveData():
    with open('csv_files/drawer_hist.csv', mode='w', newline='') as drawerHist_file:
        fieldnames = ['startingTotal', 'CashOwed', 'cashSales', 'cardSales', 'Discounts', 'Paidin', 'Paidouts',
                      'Refunds', 'tax', 'ranBy',
                      'Date', 'Time', 'overShort']

        drawerHist_writer = csv.writer(drawerHist_file)
        drawerHist_writer.writerow(fieldnames)
        for hist in drawer_record:
            drawerHist_writer.writerow(
                (hist.startingTotal, hist.CashOwed, hist.cashSales, hist.cardSales, hist.Discounts, hist.Paidin,
                 hist.Paidouts, hist.Refunds, hist.tax, hist.ranBy,
                 hist.Date, hist.Time, hist.overShort))
    with open('csv_files/user_file.csv', mode='w', newline='') as user_file:
        fieldnames = ['user_id', 'name', 'pin', 'accessLevel', 'payrate', 'hoursWorked', 'clock-in']

        user_writer = csv.writer(user_file)
        user_writer.writerow(fieldnames)
        for user in user_list:
            user_writer.writerow(
                (user.user_id, user.name, user.pin, user.accessLevel, user.payrate, user.hoursWorked, user.clock_in))
    with open('csv_files/product_file.csv', mode='w', newline='') as product_file:
        fieldnames = ['product_id', 'name', 'price', 'costToMake', 'disabled', 'groundsUsed', 'milkUsed', 'syrupUsed',
                      'category']

        product_writer = csv.writer(product_file)
        product_writer.writerow(fieldnames)
        for product in product_list:
            product_writer.writerow(
                (product.product_id, product.name, product.price, product.costToMake, product.disabled,
                 product.groundsUsed, product.milkUsed, product.syrupUsed, product.category))
    with open('csv_files/discounts_file.csv', mode='w', newline='') as discounts_file:
        fieldnames = ['amount', 'type', 'employee', 'reason', 'date']

        discounts_writer = csv.writer(discounts_file)
        discounts_writer.writerow(fieldnames)
        for discounts in discount_Record:
            discounts_writer.writerow(
                (discounts.amount, discounts.type, discounts.employee, discounts.reason, discounts.date))

    with open('csv_files/sales_file.csv', mode='w', newline='') as sales_file:
        fieldnames = ['checkNum', 'date', 'time', 'products', 'user', 'paymentType', 'paymentAmount', 'tax', 'discount']

        sales_writer = csv.writer(sales_file)
        sales_writer.writerow(fieldnames)
        for sale in sale_records:
            sales_writer.writerow((sale.checkNum, sale.date, sale.time, sale.products, sale.user, sale.paymentType,
                                   sale.paymentAmount, sale.tax, sale.discount))
    with open('csv_files/saved_orders.csv', mode='w', newline='') as saved_orders_file:
        fieldnames = ['orderTotal', 'Items', 'Date', 'Time', 'user', 'customerName']

        saved_orders_writer = csv.writer(saved_orders_file)
        saved_orders_writer.writerow(fieldnames)
        for orders in saved_orders:
            saved_orders_writer.writerow((orders.orderTotal, orders.Items, orders.Date, orders.Time, orders.user,
                                          orders.customerName))
    with open('csv_files/drawer.csv', mode='w', newline='') as drawer_file:
        fieldnames = ['startingTotal', 'CashOwed', 'cashSales', 'cardSales', 'Discounts', 'Paidin', 'Paidouts',
                      'Refunds', 'tax']

        drawer_writer = csv.writer(drawer_file)
        drawer_writer.writerow(fieldnames)
        drawer_writer.writerow((drawer.startingTotal, drawer.CashOwed, drawer.cashSales, drawer.cardSales,
                                drawer.Discounts, drawer.Paidin, drawer.Paidouts, drawer.Refunds, drawer.tax))


def refund():
    global refundMode
    clear_frame()
    salesScreen()
    refundMode = True


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
    with open('csv_files/drawer_hist.csv', 'r') as csvfile:
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
            drawer_record.append(
                DrawerReport(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                             row[10], row[11], row[12]))
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
            product_list.append(Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
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
            sale_records.append(Sale(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
    with open('csv_files/saved_orders.csv', 'r') as csvfile:
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
            saved_orders.append(saveOrder(row[0], row[1], row[2], row[3], row[4], row[5]))
    with open('csv_files/discounts_file.csv', 'r') as csvfile:
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
            discount_Record.append(Discount(row[0], row[1], row[2], row[3], row[4]))
    with open('csv_files/drawer.csv') as csvfile:
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
            drawer.startingTotal = row[0]
            drawer.CashOwed = row[1]
            drawer.cashSales = row[2]
            drawer.cardSales = row[3]
            drawer.Discounts = row[4]
            drawer.Paidin = row[5]
            drawer.Paidouts = row[6]
            drawer.Refunds = row[7]
            drawer.tax = row[8]


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


def storeOrder(E1, newWindow):
    if float(saleTotal()) != 0:
        customerName = E1.get()
        itemList = ''
        for it in sale_items:
            itemList = itemList + '(' + str(it.product_id) + ')'
        saved_orders.append(
            saveOrder(saleTotal(), itemList, datetime.now().date(), datetime.now().time(), currentUser.name,
                      customerName))
        saveData()
        clearSale()
        clear_frame()
        newWindow.destroy()
        salesScreen()
    else:
        tk.messagebox.showwarning('Error', 'No Order To Save')
        newWindow.destroy()


def clockIn():
    global currentUser
    currentUser.clock_in = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    saveData()
    salesScreen()


def updateCheckNum():
    highest = 0
    for sales in sale_records:
        if sales.checkNum is None:
            return 1
        elif int(sales.checkNum) > highest:
            highest = int(sales.checkNum)
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
    if not found:
        user_list.append(User(0, 'Admin', 9999, '0', '20', '0', '0'))
        saveData()


checkAdmin()


def updateProductId():
    highest = 0
    for product in product_list:
        if int(product.product_id) > highest:
            highest = int(product.product_id)
    new_id = highest + 1
    if new_id == 999:
        new_id = new_id + 1
    return new_id


def addToSale(product, newWindow):
    sale_items.append(product)
    clear_frame()
    newWindow.destroy()
    salesScreen()


def removeFromSale(product, num):
    global payScrn
    sale_items.remove(product)
    clear_frame()
    clear_frame()
    if num == 1:
        payScrn.grid_remove()
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
    if refundMode:
        return 0 - total
    return total


def cashSale(total, tax, discount, newWindow):
    global currentUser
    global discounts_Applied
    global refundMode
    item_list = ''
    if refundMode:
        drawer.cashSales = round(float(drawer.cashSales) + total, 2)
        drawer.CashOwed = round(float(drawer.CashOwed) + total, 2)
        drawer.tax = round(float(drawer.tax) + tax, 2)
        drawer.Refunds = round(float(drawer.Refunds) + total, 2)
    else:
        drawer.cashSales = round(float(drawer.cashSales) + total, 2)
        drawer.CashOwed = round(float(drawer.CashOwed) + total, 2)
        drawer.tax = round(float(drawer.tax) + tax, 2)
    drawer.discount = round(float(drawer.Discounts) + discounts_Applied, 2)
    for items in sale_items:
        item_list = item_list + "(" + str(items.product_id) + ") "
    sale_records.append(
        Sale(1, datetime.now().date(), datetime.now().time(), item_list, currentUser.name, 'Cash',
             total,
             tax, discount))
    saveData()
    clearSale()
    clear_frame()
    salesScreen()
    refundMode = False
    discounts_Applied = 0.0
    newWindow.destroy()


def cardSale(total, tax, discount, newWindow):
    global currentUser
    global discounts_Applied
    global refundMode
    item_list = ''
    if refundMode:
        drawer.cardSales = round(float(drawer.cashSales) + total, 2)
        drawer.tax = round(float(drawer.tax) + tax, 2)
        drawer.Refunds = round(float(drawer.Refunds) + total, 2)
    else:
        drawer.cardSales = round(float(drawer.cashSales) + total, 2)
        drawer.tax = round(float(drawer.tax) + tax, 2)
    drawer.discount = round(float(drawer.Discounts) + discounts_Applied, 2)
    for items in sale_items:
        item_list = item_list + "(" + str(items.product_id) + ") "
    sale_records.append(
        Sale(updateCheckNum(), datetime.now().date(), datetime.now().time(), item_list, currentUser.name, 'Card',
             total,
             tax, discount))
    saveData()
    clearSale()
    discounts_Applied = 0.0
    refundMode = False
    clear_frame()
    newWindow.destroy()
    salesScreen()


def signin(en):
    pin = en.get()
    global currentUser
    found = False
    if pin == '' or ' ' in pin:
        tk.messagebox.showwarning("Invalid Pin", "Invalid Pin")
    else:
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


def clear_frame():
    global screens
    for frame in screens:
        frame.pack_forget()
        frame.grid_forget()
        for widgets in frame.winfo_children():
            widgets.pack_forget()
            widgets.grid_forget()


def selectEditUserScreen():
    clear_frame()
    button = Button(editUserScrn, text='Home', command=salesScreen)
    button.grid(row=0, column=0)
    row = 1
    column = 0
    for user in user_list:
        button = tk.Button(editUserScrn, text=(str(user.user_id) + "\n" + user.name),
                           command=partial(editSingleUser, user), height=3, width=20)
        # button.pack(side=LEFT)
        button.grid(row=row, column=column)
        row = row + 1
        if row % 5 == 0:
            column = column + 1
            row = 1
    editUserScrn.pack()


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


def itemsSalesReport():
    clear_frame()
    homeButton = Button(itemSalesReportScrn, text='Home', command=salesScreen)
    homeButton.pack()

    def loadItemSales(productId, E1, E2, item):
        for button1 in buttonArray:
            button1.pack_forget()
        startBox.pack_forget()
        L1.pack_forget()
        L2.pack_forget()
        endBox.pack_forget()
        startDate = E1.get()
        endDate = E2.get()
        if startDate:
            startDate = datetime.strptime(startDate, '%Y-%m-%d')
        if endDate:
            endDate = datetime.strptime(endDate, '%Y-%m-%d')
        count = 0
        if not endDate:
            endDate = datetime.now()
        for sales in sale_records:
            date = datetime.strptime(sales.date, '%Y-%m-%d')
            if "(" + productId + ")" in sales.products:
                if startDate and endDate:
                    if startDate <= date <= endDate:
                        count = count + sales.products.count("(" + productId + ")")
                else:
                    count = count + sales.products.count("(" + productId + ")")
        if startDate and endDate:
            info = Label(itemSalesReportScrn,
                         text=item.name + " was sold " + str(count) + " times between " + startDate.strftime(
                             '%Y-%m-%d') + " and " + endDate.strftime('%Y-%m-%d'))
        else:
            info = Label(itemSalesReportScrn,
                         text=item.name + " was sold " + str(count) + " times total")
        info.pack()
        itemSalesReportScrn.pack()

    L1 = Label(itemSalesReportScrn, text="Start Date: (YYYY-MM-DD)")
    L1.pack()
    startBox = Entry(itemSalesReportScrn)
    startBox.pack()
    L2 = Label(itemSalesReportScrn, text="End Date: (YYYY-MM-DD)")
    L2.pack()
    endBox = Entry(itemSalesReportScrn)
    endBox.pack()
    buttonArray = []
    for items in product_list:
        button = Button(itemSalesReportScrn, text=items.name, command=partial(loadItemSales, items.product_id, startBox,
                                                                              endBox, items))
        buttonArray.append(button)
        button.pack()
    itemSalesReportScrn.pack()


def salesReport():
    clear_frame()
    homeButton = Button(salesReportScrn, text='Home', command=salesScreen)
    homeButton.pack()

    def loadSales(E1, E2):
        startBox.pack_forget()
        L1.pack_forget()
        L2.pack_forget()
        loadButton.pack_forget()
        endBox.pack_forget()
        startDate = E1.get()
        endDate = E2.get()
        if not endDate:
            endDate = datetime.now()
        if not startDate:
            startDate = "1900-01-01"
        if startDate:
            startDate = datetime.strptime(startDate, '%Y-%m-%d')
        if endDate:
            endDate = datetime.strptime(endDate, '%Y-%m-%d')
        totalSales = 0
        totalTax = 0
        totalDiscount = 0
        totalCardSales = 0
        totalCashSales = 0
        totalRefunds = 0
        for sales in sale_records:
            date = datetime.strptime(sales.date, '%Y-%m-%d')
            if startDate and endDate:
                if startDate <= date <= endDate:
                    totalSales = totalSales + float(sales.paymentAmount)
                    totalTax = totalTax + float(sales.tax)
                    totalDiscount = totalDiscount + float(sales.discount)
                    if sales.paymentType == 'Card':
                        totalCardSales = totalCardSales + float(sales.paymentAmount)
                    else:
                        totalCashSales = totalCashSales + float(sales.paymentAmount)
                    if float(sales.paymentAmount) < 0:
                        totalRefunds = totalRefunds + float(sales.paymentAmount)
            else:
                totalSales = totalSales + float(sales.paymentAmount)
                totalTax = totalTax + float(sales.tax)
                totalDiscount = totalDiscount + float(sales.discount)
                if sales.paymentType == 'Card':
                    totalCardSales = totalCardSales + float(sales.paymentAmount)
                else:
                    totalCashSales = totalCashSales + float(sales.paymentAmount)
                if float(sales.paymentAmount) < 0:
                    totalRefunds = totalRefunds - float(sales.paymentAmount)
        if startDate or endDate:
            totalInfo = Label(salesReportScrn, text="$" + str(round(totalSales, 2)) + " between " + startDate.strftime(
                '%Y-%m-%d') + " and " + endDate.strftime('%Y-%m-%d'))
        else:
            totalInfo = Label(salesReportScrn, text="$" + str(round(totalSales, 2)))
        totalInfo.pack()
        taxInfo = Label(salesReportScrn, text="Tax: $" + str(round(totalTax, 2)))
        taxInfo.pack()
        discountInfo = Label(salesReportScrn, text="Discounts: $" + str(round(totalDiscount, 2)))
        discountInfo.pack()
        cardInfo = Label(salesReportScrn, text="Card Sales: $" + str(round(totalCardSales, 2)))
        cardInfo.pack()
        cashInfo = Label(salesReportScrn, text="Cash Sales: $" + str(round(totalCashSales, 2)))
        cashInfo.pack()
        refundInfo = Label(salesReportScrn, text="Refunds: -$" + str(round(totalRefunds, 2)))
        refundInfo.pack()
        salesReportScrn.pack()

    L1 = Label(salesReportScrn, text="Start Date: (YYYY-MM-DD)")
    L1.pack()
    startBox = Entry(salesReportScrn)
    startBox.pack()
    L2 = Label(salesReportScrn, text="End Date: (YYYY-MM-DD)")
    L2.pack()
    endBox = Entry(salesReportScrn)
    endBox.pack()
    loadButton = Button(salesReportScrn, text="Load", command=partial(loadSales, startBox, endBox))
    loadButton.pack()
    salesReportScrn.pack()


def clockedInReport():
    clear_frame()
    homeButton = Button(clockedInReportScrn, text='Home', command=salesScreen)
    homeButton.pack()

    def editTime(emp):
        newWindow = Toplevel(top)
        newWindow.geometry("750x250")
        newWindow.title("Edit Time")
        L1 = Label(newWindow, text="Input date and time of employee clock in \n (If it is not correct)")
        L1.pack()
        E1 = Entry(newWindow)
        E1.insert(0, emp.clock_in)
        E1.pack()
        L2 = Label(newWindow, text="Input date and time of employee clock Out \n (If it is not correct)")
        L2.pack()
        E2 = Entry(newWindow)
        E2.insert(0, datetime.now().strftime('%Y-%m-%d, %H:%M:%S'))
        E2.pack()
        L3 = Label(newWindow, text="Edit total hours worked \n (If it is not correct)")
        L3.pack()
        E3 = Entry(newWindow)
        E3.insert(0, emp.hoursWorked)
        E3.pack()
        B1 = Button(newWindow, text='Apply', command=partial(clockoutEmp, emp, E1, E2, newWindow, E3))
        B1.pack()

    def clockoutEmp(emp, inTime, outTime, window, totalHours):
        inTime = inTime.get()
        outTime = outTime.get()
        totalHours = totalHours.get()
        outTime = datetime.strptime(outTime, '%Y-%m-%d, %H:%M:%S')
        if str(inTime) != str(emp.clock_in):
            emp.clock_in = inTime
        if totalHours != emp.hoursWorked:
            emp.hoursWorked = totalHours
        if str(outTime) != datetime.now().strftime('%Y-%m-%d, %H:%M:%S'):
            clock_in_time = datetime.strptime(emp.clock_in, '%Y-%m-%d, %H:%M:%S')
            hoursWorked = outTime - clock_in_time
            hoursWorked = round(hoursWorked.total_seconds() / 3600, 2)
            emp.hoursWorked = round(hoursWorked + float(emp.hoursWorked), 2)
            emp.clock_in = '0'
            saveData()
            window.destroy()
            if currentUser == emp:
                homeScreen()
            else:
                salesScreen()

    for employees in user_list:
        if str(employees.clock_in) != '0':
            clockintime = datetime.strptime(employees.clock_in, '%Y-%m-%d, %H:%M:%S')
            L1 = Label(clockedInReportScrn,
                       text=employees.name + " Has been clocked in since " + clockintime.strftime("%m/%d/%Y, %I:%M %p"))
            B1 = Button(clockedInReportScrn, text=("Clock out " + employees.name), command=partial(editTime, employees))
            L1.pack()
            B1.pack()
    clockedInReportScrn.pack()


def refundReport():
    clear_frame()
    homeButton = Button(refundReportScrn, text='Home', command=salesScreen)
    homeButton.pack()

    def loadRefunds(E1, E2):
        startBox.pack_forget()
        L1.pack_forget()
        L2.pack_forget()
        B1.pack_forget()
        endBox.pack_forget()
        startDate = E1.get()
        endDate = E2.get()
        if not startDate:
            startDate = "1900-01-01"
        if startDate:
            startDate = datetime.strptime(startDate, '%Y-%m-%d')
        if endDate:
            endDate = datetime.strptime(endDate, '%Y-%m-%d')
        if not endDate:
            endDate = datetime.now()
        h = Scrollbar(refundReportScrn, orient='vertical')
        info = Text(refundReportScrn, font=('Helvetica', 10, 'bold'), yscrollcommand=h.set, width=300, height=300)
        info.grid_columnconfigure(0, weight=1)
        info.tag_configure("tag", justify='center')
        info.tag_add("tag", "end")
        for refunds in sale_records:
            itemsStr = ""
            for items in product_list:
                if items.product_id in refunds.products:
                    if itemsStr == "":
                        itemsStr = items.name
                    else:
                        itemsStr = itemsStr + ", " + items.name
            dateOfSale = datetime.strptime(refunds.date, '%Y-%m-%d')
            timeOfSale = datetime.strptime(refunds.time, '%H:%M:%S.%f')

            if float(refunds.paymentAmount) < 0:
                if startDate and endDate:
                    if startDate <= dateOfSale <= endDate:
                        info.insert(END,
                                    "Check Number: " + refunds.checkNum + "\nProducts: " + itemsStr + "\nUser" + refunds.user + "\nAmount: " + refunds.paymentAmount + "\nTax: " + refunds.tax + " \nDate: " + dateOfSale.strftime(
                                        "%m/%d/%Y") + "\nTime: " + timeOfSale.strftime('%I:%M:%S %p') + "\n")
                        info.insert(END,
                                    "-------------------------------------------------------------------------------------\n")

        info.pack()
        h.pack(side=RIGHT, fill=Y)
        discountReportScrn.pack()

    L1 = Label(refundReportScrn, text="Start Date: (YYYY-MM-DD)")
    L1.pack()
    startBox = Entry(refundReportScrn)
    startBox.pack()
    L2 = Label(refundReportScrn, text="End Date: (YYYY-MM-DD)")
    L2.pack()
    endBox = Entry(refundReportScrn)
    endBox.pack()
    B1 = Button(refundReportScrn, text="Run Report", command=partial(loadRefunds, startBox, endBox))
    B1.pack()
    refundReportScrn.pack()


def discountReport():
    clear_frame()
    homeButton = Button(discountReportScrn, text='Home', command=salesScreen)
    homeButton.pack()

    def loadDiscounts(E1, E2):
        startBox.pack_forget()
        L1.pack_forget()
        L2.pack_forget()
        B1.pack_forget()
        endBox.pack_forget()
        startDate = E1.get()
        endDate = E2.get()
        if not startDate:
            startDate = "1900-01-01"
        if startDate:
            startDate = datetime.strptime(startDate, '%Y-%m-%d')
        if endDate:
            endDate = datetime.strptime(endDate, '%Y-%m-%d')
        if not endDate:
            endDate = datetime.now()
        h = Scrollbar(discountReportScrn, orient='vertical')
        info = Text(discountReportScrn, font=('Helvetica', 10, 'bold'), yscrollcommand=h.set, width=300, height=300)
        info.grid_columnconfigure(0, weight=1)
        info.tag_configure("tag", justify='center')
        info.tag_add("tag", "end")
        for discounts in discount_Record:
            date = datetime.strptime(discounts.date, '%m/%d/%Y %H:%M:%S')
            if startDate and endDate:
                if startDate <= date <= endDate:
                    info.insert(END, "Amount: " + str(
                        round(float(discounts.amount), 2)) + " \nType: " + discounts.type + " \nEmployee: " +
                                discounts.employee + " \nReason: " + discounts.reason + " \nDate: " + date.strftime(
                        "%m/%d/%Y, %I:%M:%S %p") + "\n")
                    info.insert(END,
                                "-------------------------------------------------------------------------------------\n")

        info.pack()
        h.pack(side=RIGHT, fill=Y)
        discountReportScrn.pack()

    L1 = Label(discountReportScrn, text="Start Date: (YYYY-MM-DD)")
    L1.pack()
    startBox = Entry(discountReportScrn)
    startBox.pack()
    L2 = Label(discountReportScrn, text="End Date: (YYYY-MM-DD)")
    L2.pack()
    endBox = Entry(discountReportScrn)
    endBox.pack()
    B1 = Button(discountReportScrn, text="Run Report", command=partial(loadDiscounts, startBox, endBox))
    B1.pack()
    discountReportScrn.pack()


def drawerHistReport():
    clear_frame()
    homeButton = Button(drawerHistReportScrn, text='Home', command=salesScreen)
    homeButton.pack()

    def loadDiscounts(E1, E2):
        startBox.pack_forget()
        L1.pack_forget()
        L2.pack_forget()
        B1.pack_forget()
        endBox.pack_forget()
        startDate = E1.get()
        endDate = E2.get()
        if not startDate:
            startDate = "1900-01-01"
        if startDate:
            startDate = datetime.strptime(startDate, '%Y-%m-%d')
        if endDate:
            endDate = datetime.strptime(endDate, '%Y-%m-%d')
        if not endDate:
            endDate = datetime.now()
        h = Scrollbar(drawerHistReportScrn, orient='vertical')
        info = Text(drawerHistReportScrn, font=('Helvetica', 10, 'bold'), yscrollcommand=h.set, width=300, height=300)
        info.grid_columnconfigure(0, weight=1)
        info.tag_configure("tag", justify='center')
        info.tag_add("tag", "end")
        for hist in drawer_record:
            date = datetime.strptime(hist.Date, '%Y-%m-%d')
            time = datetime.strptime(hist.Time, '%H:%M:%S.%f')
            if startDate and endDate:
                if startDate <= date <= endDate:
                    info.insert(END,
                                "Starting Total: " + hist.startingTotal + "\nCash Owed: " + hist.CashOwed + "\nCash Sales: " + hist.cashSales + "\nCard Sales: " + hist.cardSales + "\nDiscounts: " + hist.Discounts + "\nPaidin: " + hist.Paidin + "\nPaidouts: " + hist.Paidouts + "\nRefunds: "
                                                                                                                                                                                                                                                                                     "" + hist.Refunds + "\nTax:" + hist.tax + "\nRan By: " + hist.ranBy + "\nTime: " + time.strftime(
                                    '%I:%M:%S %p') + "\noverShort: " + hist.overShort + " \nDate: " + date.strftime(
                                    "%m/%d/%Y") + "\n")
                    info.insert(END,
                                "-------------------------------------------------------------------------------------\n")

        info.pack()
        h.pack(side=RIGHT, fill=Y)
        drawerHistReportScrn.pack()

    L1 = Label(discountReportScrn, text="Start Date: (YYYY-MM-DD)")
    L1.pack()
    startBox = Entry(discountReportScrn)
    startBox.pack()
    L2 = Label(discountReportScrn, text="End Date: (YYYY-MM-DD)")
    L2.pack()
    endBox = Entry(discountReportScrn)
    endBox.pack()
    B1 = Button(discountReportScrn, text="Run Report", command=partial(loadDiscounts, startBox, endBox))
    B1.pack()
    discountReportScrn.pack()


def payrollReport(win):
    win.destroy()
    clear_frame()
    button = Button(payrollReportScrn, text='Home', command=salesScreen)
    button.pack()
    arr = []
    for emp in user_list:
        if emp.clock_in != '0':
            clock_in_time = datetime.strptime(emp.clock_in, '%Y-%m-%d, %H:%M:%S')
            hoursWorked = datetime.now() - clock_in_time
            hoursWorked = round(hoursWorked.total_seconds() / 3600, 2)
            emp.hoursWorked = round(hoursWorked + float(emp.hoursWorked), 2)
            emp.clock_in = '0'
        file1 = open("Payroll Reports/Payroll " + datetime.now().strftime('%Y-%m-%d, %I-%M-%S %p') + ".txt", "a")  # append mode
        file1.write(str(emp.name) + " Hours Worked: " + str(emp.hoursWorked) + " Paycheck Amount: " + str(
            round((float(emp.hoursWorked) * float(emp.payrate)), 2))+ "\n")
        file1.close()
        arr.append(str(emp.name) + " Hours Worked: " + str(emp.hoursWorked) + " Paycheck Amount: " + str(
            round((float(emp.hoursWorked) * float(emp.payrate)), 2))+ "\n")
        emp.hoursWorked = 0
    for a in arr:
        L1 = Label(payrollReportScrn, text=a)
        L1.pack()
    payrollReportScrn.pack()


def selectReportsScreen():
    def confirmPayroll():
        newWindow = Toplevel(top)
        newWindow.geometry("750x250")
        newWindow.title("Confirm Payroll")
        L1 = Label(newWindow, text='Are you sure you want to run payroll? \nthis action can not be undone.\n All '
                                   'Employees will be clocked out and hours reset.')
        L1.pack()
        B1 = Button(newWindow, text="Yes", command=partial(payrollReport, newWindow))
        B1.pack()
        B2 = Button(newWindow, text="No", command=newWindow.destroy)
        B2.pack()

    clear_frame()
    button = Button(selectReportsScrn, text='Home', command=salesScreen)
    button.pack()
    drawer_reportButton = Button(selectReportsScrn, text='Drawer Report', command=drawerReport)
    drawer_reportButton.pack()
    itemSales_reportButton = Button(selectReportsScrn, text='Item Sales Report', command=itemsSalesReport)
    itemSales_reportButton.pack()
    Sales_reportButton = Button(selectReportsScrn, text='Sales Report', command=salesReport)
    Sales_reportButton.pack()
    Sales_reportButton = Button(selectReportsScrn, text='Discount Report', command=discountReport)
    Sales_reportButton.pack()
    Refund_reportButton = Button(selectReportsScrn, text='Refund Report', command=refundReport)
    Refund_reportButton.pack()
    clockin_reportButton = Button(selectReportsScrn, text='Clocked-in Report', command=clockedInReport)
    clockin_reportButton.pack()
    payRoll_reportButton = Button(selectReportsScrn, text='Payroll Report', command=confirmPayroll)
    payRoll_reportButton.pack()
    DrawerHistReportButton = Button(selectReportsScrn, text='Drawer History Report',
                                    command=drawerHistReport)
    DrawerHistReportButton.pack()
    selectReportsScrn.pack()


def drawerReport():
    def updateStartTotal(E1):
        newTotal = E1.get()
        drawer.startingTotal = newTotal

    def runDrawer(E1):
        inDrawer = E1.get()
        overShort = float(inDrawer) - (float(drawer.startingTotal) + float(drawer.CashOwed))
        overShort = round(overShort, 2)
        answer = tk.messagebox.askyesno('Confirm', ('Drawer is Over/Short: $' + str(overShort)))
        if answer:
            drawer_record.append(DrawerReport(drawer.startingTotal, drawer.CashOwed, drawer.cashSales, drawer.cardSales,
                                              drawer.Discounts, drawer.Paidin,
                                              drawer.Paidouts, drawer.Refunds, drawer.tax, currentUser.name,
                                              datetime.now().date(), datetime.now().time(), overShort))
            drawer.startingTotal = float(inDrawer) - float(drawer.CashOwed)
            drawer.CashOwed = 0
            drawer.tax = 0
            drawer.Paidin = 0
            drawer.Paidouts = 0
            drawer.cashSales = 0
            drawer.cardSales = 0
            drawer.Refunds = 0
            drawer.Discounts = 0
            clear_frame()
            drawerReport()

    clear_frame()
    button = Button(drawerReportScrn, text='Home', command=salesScreen)
    button.grid(row=0, column=0)
    StartTotal = Label(drawerReportScrn, text='Starting Total: $')
    StartTotal.grid(row=1, column=0)
    startTotalEntry = Entry(drawerReportScrn)
    startTotalEntry.insert(0, drawer.startingTotal)
    startTotalEntry.grid(row=1, column=1)
    currentTotal = Label(drawerReportScrn, text=('Cash Owed: $' + str(drawer.CashOwed)))
    currentTotal.grid(row=2, column=0)
    cashSales = Label(drawerReportScrn, text=('Cash Sales: $' + str(drawer.cashSales)))
    cashSales.grid(row=3, column=0)
    cardSales = Label(drawerReportScrn, text=('Card Sales: $' + str(drawer.cardSales)))
    cardSales.grid(row=4, column=0)
    Discounts = Label(drawerReportScrn, text=('Discounts: $' + str(drawer.Discounts)))
    Discounts.grid(row=5, column=0)
    Paidin = Label(drawerReportScrn, text=('Paid-in: $' + str(drawer.Paidin)))
    Paidin.grid(row=6, column=0)
    Paidouts = Label(drawerReportScrn, text=('Paid-out: $' + str(drawer.Paidouts)))
    Paidouts.grid(row=7, column=0)
    Refunds = Label(drawerReportScrn, text=('Refunds: $' + str(drawer.Refunds)))
    Refunds.grid(row=8, column=0)
    tax = Label(drawerReportScrn, text=('Tax: $' + str(drawer.tax)))
    tax.grid(row=9, column=0)
    countL = Label(drawerReportScrn, text='Enter Total Amount In Drawer: $')
    countL.grid(row=10, column=0)
    countE = Entry(drawerReportScrn)
    countE.grid(row=10, column=1)
    B1 = Button(drawerReportScrn, text='Save Starting Total', command=partial(updateStartTotal, startTotalEntry))
    if float(drawer.CashOwed) == 0:
        B1.grid(row=11, column=0)
    B2 = Button(drawerReportScrn, text='Run Drawer', command=partial(runDrawer, countE))
    B2.grid(row=12, column=0)

    drawerReportScrn.pack()


def addProductScreen():  # TODO: app must be rebooted to show new products
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
    L4 = Label(addProductScrn, text="Grounds Used in grams:")
    E4 = Entry(addProductScrn)
    L4.pack()
    E4.pack()
    L5 = Label(addProductScrn, text="Milk Used in oz:")
    E5 = Entry(addProductScrn)
    L5.pack()
    E5.pack()
    L6 = Label(addProductScrn, text="Syrup Used in oz:")
    E6 = Entry(addProductScrn)
    L6.pack()
    E6.pack()
    L7 = Label(addProductScrn, text="Category:")
    E7 = Entry(addProductScrn)
    L7.pack()
    E7.pack()
    B1 = Button(addProductScrn, text='Save', command=partial(addProduct, E1, E2, E3, E4, E5, E6, E7))
    B1.pack()
    addProductScrn.pack()


def addProduct(E1, E2, E3, E4, E5, E6, E7):  # TODO: app must be rebooted to show new products
    global product_list
    name = E1.get()
    price = E2.get()
    costToMake = E3.get()
    groundsUsed = E4.get()
    milkUsed = E5.get()
    syrupUsed = E6.get()
    category = E7.get()
    product_list.append(
        Product(updateProductId(), name, price, costToMake, 0, milkUsed, groundsUsed, syrupUsed, category))
    saveData()
    clear_frame()
    salesScreen()


def selectEditProduct():
    clear_frame()
    button = Button(editProductScrn, text='Home', command=salesScreen)
    button.grid(row=0, column=1)
    global product_list
    row = 1
    column = 0
    for product in product_list:
        button = tk.Button(editProductScrn, text=product.name + "\n$" + product.price,
                           command=partial(editProductScreen, product), height=3, width=20)
        # button.pack(side=LEFT)
        button.grid(row=row, column=column)
        row = row + 1
        if row % 5 == 0:
            column = column + 1
            row = 1
    editProductScrn.pack()


def editProductScreen(product):
    global product_list
    global category_list
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
    L4 = Label(editProductScrn, text="Disabled: ")
    variable = StringVar(editProductScrn)
    if product.disabled == 1:
        variable.set("True")
    else:
        variable.set("False")
    E4 = OptionMenu(editProductScrn, variable, "True", "False")
    L4.pack()
    E4.pack()
    L4 = Label(editProductScrn, text="Grounds Used in grams:")
    E4 = Entry(editProductScrn)
    E4.insert(0, product.groundsUsed)
    L4.pack()
    E4.pack()
    L5 = Label(editProductScrn, text="Milk Used in oz:")
    E5 = Entry(editProductScrn)
    E3.insert(0, product.milkUsed)
    L5.pack()
    E5.pack()
    L6 = Label(editProductScrn, text="Syrup Used in oz:")
    E6 = Entry(editProductScrn)
    E6.insert(0, product.syrupUsed)
    L6.pack()
    E6.pack()
    L7 = Label(editProductScrn, text='Category:')
    E7 = Entry(editProductScrn)
    E7.insert(0, product.category)  # TODO: Find a better way to select categories
    L7.pack()
    E7.pack()
    B1 = Button(editProductScrn, text='Save',
                command=partial(editProduct, E1, E2, E3, variable, E4, E5, E6, E7, product))
    B1.pack()
    B2 = Button(editProductScrn, text='Delete', command=partial(deleteProduct, product))
    B2.pack()
    editProductScrn.pack()


def editProduct(E1, E2, E3, E4, E5, E6, E7, var2, product):
    name = E1.get()
    price = E2.get()
    costToMake = E3.get()
    disabled = E4.get()
    groundsUsed = E5.get()
    milkUsed = E6.get()
    syrupUsed = E7.get()
    category = var2.get()
    if disabled == 'True':
        disabled = '1'
    else:
        disabled = '0'
    if name == '' or price == '' or costToMake == '':
        tk.messagebox.showwarning("Empty", "Error: one or more text field is empty")
    else:
        product.name = name
        product.price = price
        product.costToMake = costToMake
        product.disabled = disabled
        product.groundsUsed = groundsUsed
        product.milkUsed = milkUsed
        product.syrupUsed = syrupUsed
        product.category = category
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
            if user.name == 'Admin' and user.user_id == '0':
                user.accessLevel = 0
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


def getCatList():
    global category_list
    for products in product_list:
        if products.category not in category_list:
            category_list.append(products.category)
    return category_list


def clearSale():
    global sale_items
    global refundMode
    global discounts_Applied
    sale_items = []
    discounts_Applied = 0.0
    clear_frame()
    refundMode = False
    salesScreen()


def salesScreen():
    global currentUser
    global screens
    clear_frame()
    frames = []

    def pullOrder(order, newWindow):
        for prod in product_list:
            prodid = '(' + str(prod.product_id) + ')'
            if prodid in order.Items:
                sale_items.append(prod)
        newWindow.destroy()
        saved_orders.remove(order)
        clear_frame()
        salesScreen()

    def saveOrderName():
        newWindow = Toplevel(top)
        newWindow.geometry("750x250")
        newWindow.title("Enter name")
        L1 = Label(newWindow, text='Enter Customer Name')
        E1 = Entry(newWindow)
        E1.pack()
        L1.pack()
        B1 = Button(newWindow, text='Save', command=partial(storeOrder, E1, newWindow))
        B1.pack()

    def retrieveSale():
        newWindow = Toplevel(top)
        newWindow.geometry("750x250")
        newWindow.title("Select Order")
        for order in saved_orders:
            B1 = Button(newWindow, text=(
                    'Customer: ' + order.customerName + '\n$' + str(order.orderTotal) + '\nDate:' + str(
                order.Date) + '\nTime:' + str(order.Time) +
                    '\nUser:' + str(order.user)), command=partial(pullOrder, order, newWindow))
            B1.pack()

    def addOpenItem(E1, E2, win, win2):
        amount = E1.get()
        valid = True
        try:
            float(amount)
        except:
            valid = False
            tk.messagebox.showwarning('Error', 'Invalid Entry')
        if valid:
            Description = E2.get()
            sale_items.append(Product(999, ('Open Item ' + Description), amount, 0, 0, 0, 0, 0, 'misc'))
            clear_frame()
            salesScreen()
        win.destroy()
        win2.destroy()

    def openDollar(win):
        newWindow = Toplevel(top)
        newWindow.geometry("750x250")
        newWindow.title("Open Dollar")
        L1 = Label(newWindow, text='Enter Dollar Amount')
        E1 = Entry(newWindow)
        L1.pack()
        E1.pack()
        L2 = Label(newWindow, text='Enter Description')
        E2 = Entry(newWindow)
        L2.pack()
        E2.pack()
        B1 = Button(newWindow, text='Enter', command=partial(addOpenItem, E1, E2, newWindow, win))
        B1.pack()

    def showCategory(cat):
        newWindow = Toplevel(top)
        newWindow.geometry("750x750")
        newWindow.title("Select Product")
        row = 0
        column = 0
        for product in product_list:
            if product.disabled == '0':
                if product.category == cat:
                    button = tk.Button(newWindow, text=product.name + "\n$" + product.price,
                                       command=partial(addToSale, product, newWindow), height=3, width=20)
                    # button.pack(side=LEFT)
                    button.grid(row=row, column=column)
                    row = row + 1
                    if row % 5 == 0 and row != 0:
                        column = column + 1
                        row = 0
        if currentUser.accessLevel == '0' and cat == 'misc':
            openItem = Button(newWindow, text='Open Dollar', command=partial(openDollar, newWindow), height=3, width=20)
            openItem.grid(row=row, column=column)

    salesFrame = Frame(saleScrn)
    itemsFrame = Frame(saleScrn)
    menuFrame = Frame(saleScrn)
    totalFrame = Frame(saleScrn)
    frames.append(salesFrame)
    frames.append(itemsFrame)
    frames.append(menuFrame)
    frames.append(totalFrame)
    global refundMode
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
        menubutton.menu.add_command(label="Reports Screen",
                                    command=selectReportsScreen)
        menubutton.menu.add_command(label="Inventory Screen",
                                    command=None)  # TODO: Implement
        if str(currentUser.accessLevel) == '0':
            menubutton.pack(side=TOP)
            # menubutton.grid(row=0, column=0)
        clr_sale = Button(menuFrame, text='Clear Sale', command=clearSale)
        clr_sale.pack(side=BOTTOM)
        if not sale_items and currentUser.accessLevel == '0':
            refund_sale = Button(menuFrame, text='Refund Sale', command=refund)
            refund_sale.pack(side=BOTTOM)
        save_sale = Button(menuFrame, text='Save Sale', command=saveOrderName)
        save_sale.pack(side=BOTTOM)
        retrieve_sale = Button(menuFrame, text='Retrieve Sale', command=retrieveSale)
        retrieve_sale.pack(side=BOTTOM)
        # clr_sale.grid(row=3, column=3)
        B1 = Button(menuFrame, text='Clock Out', command=clockOut)
        B1.pack(side=RIGHT)
        # B1.grid(row=1, column=0)
        B2 = Button(menuFrame, text='Sign Out', command=logout)
        B2.pack(side=LEFT)
        # B2.grid(row=2, column=0)
        # menuFrame.grid_columnconfigure(3, weight=2)
        row = 4
        column = 0
        getCatList()
        for cat in category_list:
            cat_button = Button(itemsFrame, text=cat, command=partial(showCategory, cat))
            cat_button.grid(row=row, column=column)
            row = row + 1
            if row % 5 == 0 and row != 5:
                column = column + 1
                row = 4
        row = 4
        for items in sale_items:
            if not refundMode:
                L1 = Label(salesFrame, text=(items.name + ' $' + items.price))
            else:
                L1 = Label(salesFrame, text=(items.name + ' -$' + items.price))

            # L1.pack(side=RIGHT)
            L1.grid(row=row, column=1)
            B1 = Button(salesFrame, text="Remove", command=(partial(removeFromSale, items, 0)))
            # B1.pack(side=RIGHT)
            B1.grid(row=row, column=2)
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
        itemsFrame.pack(side=LEFT, pady=10, padx=10, expand=FALSE)
        salesFrame.pack(side=RIGHT, pady=10, padx=10, expand=FALSE)
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


def discount(amount, discountType, E1, fixed, newWindow):
    if type(E1) is Entry:
        reason = E1.get()
    else:
        reason = E1
    if type(amount) is Entry:
        amount = amount.get()
        amount = float(amount)
    global discounts_Applied
    if saleTotal() < amount:
        tk.messagebox.showwarning('Error', 'Discount is lower than total')
        newWindow.destroy()
    elif reason == '':
        tk.messagebox.showwarning('Error', 'Please enter the reason')
        newWindow.destroy()
    else:
        if not fixed:
            discountAmount = amount * saleTotal()
        else:
            discountAmount = amount
        discounts_Applied = discountAmount
        drawer.Discounts = float(drawer.Discounts) + discountAmount
        discount_Record.append(
            Discount(discountAmount, discountType, currentUser.name, reason,
                     datetime.now().strftime("%m/%d/%Y %H:%M:%S")))
        clear_frame()
        newWindow.destroy()
        paymentScreen()


def paymentScreen():
    clear_frame()

    def openDiscountScreen():
        newWindow = Toplevel(top)
        newWindow.geometry("750x250")
        newWindow.title("Discounts")
        if int(currentUser.accessLevel) == 0:
            L1 = Label(newWindow, text='Enter Reason')
            E1 = Entry(newWindow)
            L1.grid(row=0, column=1)
            E1.grid(row=1, column=1)
            Label(newWindow, text="Please select a discount")
            Emp_Discount = Button(newWindow, text='Employee Discount',
                                  command=partial(discount, 1.00, 'EmployeeDiscount', E1, False, newWindow))
            Emp_Discount.grid(row=2, column=0)
            tenPercent = Button(newWindow, text='10% Off',
                                command=partial(discount, .10, '10Percent', E1, False, newWindow))
            tenPercent.grid(row=3, column=0)
            twentyPercent = Button(newWindow, text='20% Off',
                                   command=partial(discount, .20, '20Percent', E1, False, newWindow))
            twentyPercent.grid(row=4, column=0)
            L3 = Label(newWindow, text='Enter Custom Amount:')
            E2 = Entry(newWindow)
            L4 = Label(newWindow, text="Please enter decimal amount for percent")
            L3.grid(row=0, column=2)
            E2.grid(row=1, column=2)
            L4.grid(row=2, column=2)
            customPercent = Button(newWindow, text='Custom Percent',
                                   command=partial(discount, E2, 'Custom Percent', E1, False, newWindow))
            customPercent.grid(row=3, column=2)
            customDollar = Button(newWindow, text='Custom Dollar',
                                  command=partial(discount, E2, 'Custom Dollar', E1, True, newWindow))
            customDollar.grid(row=4, column=2)
        byoc = Button(newWindow, text="BYO Cup", command=partial(discount, .50, 'BYO Cup', 'BYO Cup', True, newWindow))
        byoc.grid(row=5, column=0)
        warn = Label(newWindow, text='One Discount Per transaction')
        warn.grid(row=5, column=1)
        clear_frame()
        paymentScreen()

    def openPaymentScreen():
        newWindow = Toplevel(top)
        newWindow.geometry("750x250")
        newWindow.title("Tender")
        Cash = Button(newWindow, text='Cash', command=partial(cashSale, total, tax, discounts_Applied, newWindow))
        Cash.pack()
        Card = Button(newWindow, text='Card', command=partial(cardSale, total, tax, discounts_Applied, newWindow))
        Card.pack()

    button = Button(payScrn, text='Home', command=salesScreen)
    button.grid(row=0, column=1)
    payScrn.grid_columnconfigure(2, minsize=10)
    border = Label(payScrn, text='-----------------------')
    border.grid(row=3, column=1)
    row = 4
    for items in sale_items:
        L1 = Label(payScrn, text=(items.name + ' $' + items.price))
        # L1.pack(side=RIGHT)
        L1.grid(row=row, column=1)
        B1 = Button(payScrn, text="Remove", command=(partial(removeFromSale, items, 1)))
        # B1.pack(side=RIGHT)
        B1.grid(row=row, column=2)
        row = row + 1
    border2 = Label(payScrn, text='-----------------------')
    border2.grid(row=row, column=1)
    subtotal = saleTotal()
    Subtotal_Label = Label(payScrn, text=('Subtotal: $' + str(round(subtotal, 2))))
    Subtotal_Label.grid(row=row + 1, column=1)
    discount_label = Label(payScrn, text=('Discounts: ' + str(round(discounts_Applied, 2))))
    discount_label.grid(row=row + 2, column=1)
    subtotal = subtotal - discounts_Applied
    tax = subtotal * 0.07
    tax = round(tax, 2)
    Tax_Label = Label(payScrn, text=('Tax: $' + str(tax)))
    Tax_Label.grid(row=row + 3, column=1)
    total = subtotal + tax
    total = round(total, 2)
    Total_Label = Label(payScrn, text=('Total: $' + str(total)))
    Total_Label.grid(row=row + 4, column=1)
    if not refundMode:
        Discount_Button = Button(payScrn, text="Discounts", command=openDiscountScreen)
        Discount_Button.grid(row=row + 5, column=1)
    tender_Button = Button(payScrn, text='Payment', command=openPaymentScreen)
    tender_Button.grid(row=row + 6, column=1)
    payScrn.pack()


homeScreen()
homeScrn.pack()


def on_close():
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        top.destroy()
        saveData()


top.protocol("WM_DELETE_WINDOW", on_close)
top.mainloop()
