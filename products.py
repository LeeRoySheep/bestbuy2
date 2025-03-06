class Product:
    '''A class representing a product'''
    def __init__(self, name, price, quantity):
        '''Initializes the product'''
        self.name = name
        self.price = price
        self.quantity = quantity
        if quantity == 0:
            self.active = False
        if quantity > 0:
            self.active = True
        if not name:
            raise ValueError("Name cannot be empty!")
        if price < 0:
            raise ValueError("Price cannot be negative!")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative!")


    def get_quantity(self):
        '''Returns the quantity of the product'''
        return self.quantity


    def set_quantity(self, quantity):
        '''Sets the quantity of the product'''
        if quantity == 0:
            self.deactivate()
        if quantity > 0 and self.quantity == 0:
            self.activate()
        self.quantity = quantity



    def is_active(self):
        '''Returns the active status of the product'''
        return self.active


    def activate(self):
        '''Activates the product'''
        self.active = True


    def deactivate(self):
        '''Deactivates the product'''
        self.active = False


    def show(self):
        '''Returns the product details as string'''
        return f"{self.name}, Price: ({self.price}), Quantity: {self.quantity}"


    def buy(self, quantity):
        '''Buys a quantity of the product, updates quantity and returns the total price'''
        if quantity <= self.quantity:
            self.quantity -= quantity
        else:
            raise ValueError("Not enough quantity to buy!")
        if self.quantity == 0:
            self.deactivate()
        return self.price * quantity


def main():
    '''Main function as using example and for testing purposes'''
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    print(bose.show())
    print(mac.show())

    bose.set_quantity(1000)
    print(bose.show())

if __name__ == "__main__":
    main()
