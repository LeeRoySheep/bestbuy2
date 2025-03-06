class Product:
    """A class representing a product"""
    def __init__(self, name, price, quantity):
        """Initializes the product"""
        self.name = name
        self.price = price
        self.quantity = quantity
        if quantity == 0:
            self._active = False
        if quantity > 0:
            self._active = True
        if not name:
            raise ValueError("Name cannot be empty!")
        if price < 0:
            raise ValueError("Price cannot be negative!")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative!")


    def get_quantity(self):
        """Returns the quantity of the product"""
        return self.quantity


    def set_quantity(self, quantity):
        """Sets the quantity of the product"""
        if quantity == 0:
            self.deactivate()
        if quantity > 0 and self.quantity == 0:
            self.activate()
        self.quantity = quantity



    def is_active(self):
        """Returns the active status of the product"""
        return self._active


    def activate(self):
        """Activates the product"""
        self._active = True


    def deactivate(self):
        """Deactivates the product"""
        self._active = False


    def show(self):
        """Returns the product details as string"""
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}"


    def buy(self, quantity):
        """Buys a quantity of the product, updates quantity and returns the total price"""
        if quantity <= self.quantity:
            self.quantity -= quantity
        else:
            raise ValueError("Not enough quantity to buy!")
        if self.quantity == 0:
            self.deactivate()
        return self.price * quantity


class NonStockedProduct(Product):
    """A class representing a product that is not stocked"""
    def __init__(self, name, price):
        """Initializes the product"""
        super().__init__(name, price, quantity=0)
        self.activate()


    def buy(self, quantity):
        """Buys a quantity of the product and returns the total price"""
        return self.price * quantity


    def show(self):
        """Returns the product details as string"""
        return f"{self.name}, Price: ${self.price}, Quantity: Unlimited"


class LimitedProduct(Product):
    """A class representing a product with limited quantity"""
    def __init__(self, name, price, quantity, maximum=1):
        """Initializes the product"""
        super().__init__(name, price, quantity)
        self.maximum = maximum


    def buy(self, quantity):
        """Buys a quantity of the product, updates quantity and returns the total price"""
        if quantity <= self.maximum and quantity <= self.quantity:
            self.quantity -= quantity
        else:
            raise ValueError(f"Not enough quantity({self.quantity}) or tried to buy more than maximum({self.maximum})!")
        return self.price * quantity


    def show(self):
        """Returns the product details as string"""
        return f"{self.name}, Price: ${self.price}, Limited to {self.maximum} per order!"

def main():
    """Main function as using example and for testing purposes"""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    google = Product("Google Pixel 7", price=500, quantity=250)
    windows = NonStockedProduct("Windows License", price=125)
    shipping = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)

    print(bose.buy(50))
    print(mac.buy(100))
    print(google.buy(200))
    print(windows.buy(22))
    print(windows.is_active())
    print(shipping.buy(1))
    print(mac.is_active())

    print(bose.show())
    print(mac.show())

    bose.set_quantity(1000)
    print(bose.show())

if __name__ == "__main__":
    main()
