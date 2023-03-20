class User:
    def __init__(self, user_id, name, pin, accessLevel, payrate, hoursWorked, clock_in):
        self.clock_in = clock_in
        self.user_id = user_id
        self.name = name
        self.pin = pin
        self.accessLevel = accessLevel
        self.payrate = payrate
        self.hoursWorked = hoursWorked


class Product:
    def __init__(self, product_id, name, price, costToMake, disabled, groundsUsed, milkUsed, syrupUsed, category):
        self.category = category
        self.syrupUsed = syrupUsed
        self.milkUsed = milkUsed
        self.groundsUsed = groundsUsed
        self.disabled = disabled
        self.product_id = product_id
        self.name = name
        self.price = price
        self.costToMake = costToMake


class Sale:
    def __init__(self, checkNum, date, time, products, user, paymentType, paymentAmount, tax, discount):
        self.discount = discount
        self.tax = tax
        self.paymentAmount = paymentAmount
        self.paymentType = paymentType
        self.user = user
        self.products = products
        self.time = time
        self.date = date
        self.checkNum = checkNum
class saveOrder:
    def __init__(self,orderTotal,Items,Date,Time,user,customerName):
        self.customerName = customerName
        self.user = user
        self.Time = Time
        self.Date = Date
        self.Items = Items
        self.orderTotal = orderTotal


class Discount:
    def __init__(self, amount, type, employee, reason):
        self.amount = amount
        self.type = type
        self.employee = employee
        self.reason = reason


class cashDrawer:
    def __init__(self, startingTotal, CashOwed, cashSales, cardSales, Discounts, Paidin, Paidouts, Refunds, tax):
        self.tax = tax
        self.Refunds = Refunds
        self.Paidin = Paidin
        self.Discounts = Discounts
        self.cardSales = cardSales
        self.cashSales = cashSales
        self.Paidouts = Paidouts
        self.CashOwed = CashOwed
        self.startingTotal = startingTotal
class DrawerReport:
    def __init__(self,startingTotal, CashOwed, cashSales, cardSales, Discounts, Paidin, Paidouts, Refunds, tax, ranBy,
                 Date,Time,overShort):
        self.overShort = overShort
        self.Time = Time
        self.Date = Date
        self.ranBy = ranBy
        self.tax = tax
        self.Refunds = Refunds
        self.Paidouts = Paidouts
        self.Paidin = Paidin
        self.Discounts = Discounts
        self.cardSales = cardSales
        self.cashSales = cashSales
        self.CashOwed = CashOwed
        self.startingTotal = startingTotal