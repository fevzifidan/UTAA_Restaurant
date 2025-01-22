class Order:
    # We create a class for Order
    def __init__(self):
        self.orderList = []
        self.orderTypeList = []

    def addToOrder(self, order):
        self.orderList.append(order)
        self.orderTypeList.append(order[1])
    
    def changeOrder(self, old_order, new_order):
        self.orderList[self.orderList.index(old_order)] = new_order

    def sameCategory(self, category):
        if category in self.orderTypeList:
            # In addition to a boolean value, we also return the existing order to
            # provide the customer with chance to change their decision later on.
            return (True, self.orderList[self.orderTypeList.index(category)])
        else: return (False, None)
    
    def showOrder(self):
        return self.orderList
    
    def totalOrderedProductNumber(self):
        return len(self.orderList)
    
    def calculateOrderFee(self):
        fee = 0
        for order in self.orderList:
            fee += int(order[2])
        return fee


# END