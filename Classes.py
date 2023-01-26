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
    def __init__(self, product_id, name, price, costToMake,disabled):
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




class Discount:
    def __init__(self, amount, type, employee, reason):
        self.amount = amount
        self.type = type
        self.employee = employee
        self.reason = reason
