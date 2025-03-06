import promotions

class Product:
    """A class representing a product"""
    def __init__(self, name, price, quantity, promotions_lst=None):
        """Initializes the product"""
        self.name = name
        self.price = price
        self.quantity = quantity
        self.promotions_lst = promotions_lst
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


    def get_promotion(self):
        """Returns the promotions of the product"""
        return self.promotions_lst


    def set_promotion(self, promotion):
        """Sets the promotions of the product"""
        if not self.promotions_lst:
            self.promotions_lst = []
        if promotion not in self.promotions_lst:
            self.promotions_lst.append(promotion)
            print(1)
        elif isinstance(promotion, promotions.PercentDiscount):
            for promo in self.promotions_lst:
                if isinstance(promo, promotions.PercentDiscount):
                    promo.percent = promotion.percent
                    promo.name = promotion.name
        else:
            raise ValueError("Promotion already exists!")


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
        if not self.promotions_lst:
            return (
                f"{self.name},"
                + f"Price: ${self.price}, "
                + f"Quantity: {self.quantity},"
                + f"Promotions: None"
            )
        else:
            output_string = (
                f"{self.name},"
                + f" Price: ${self.price},"
                + f" Quantity: {self.quantity},"
                + f"Promotions:"
            )
            counter = 0
            for promo in self.promotions_lst:
                counter += 1
                if counter == len(self.promotions_lst):
                    output_string += f" {promo.name}"
                else:
                    output_string += f" {promo.name},"
            return output_string


    def buy(self, quantity):
        """Buys a quantity of the product, updates quantity and returns the total price"""
        # Checking for overlapping discounts
        if quantity <= self.quantity:
            self.quantity -= quantity
            if self.quantity == 0:
                self.deactivate()
            if not self.promotions_lst:
                return quantity * self.price
            if self.promotions_lst:
                discount_exception = 0
                for promo in self.promotions_lst:
                    if isinstance(promo, promotions.SecondHalfPrice):
                        discount_exception += 1
                    elif isinstance(promo, promotions.ThirdOneFree):
                        discount_exception += 1
                if discount_exception == 2:
                    # Setting total price and adding overlapping
                    # discounts as every 6th product is for free and gets 50% off
                    total_price = ((quantity // 6) * self.price * 0.25)
                    for promo in self.promotions_lst:
                        total_price += promo.apply_promotion(self, quantity)
                    return total_price
                elif discount_exception != 2:
                    total_price = 0
                    for promo in self.promotions_lst:
                        total_price += promo.apply_promotion(self, quantity)
                    return total_price
        else:
            raise ValueError("Not enough quantity to buy!")


class NonStockedProduct(Product):
    """A class representing a product that is not stocked"""
    def __init__(self, name, price, promotions_lst=None):
        """Initializes the product"""
        super().__init__(name, price, quantity=0, promotions_lst=promotions_lst)
        self.activate()


    def buy(self, quantity):
        """Buys a quantity of the product and returns the total price"""
        if not self.promotions_lst:
            return quantity * self.price
        else:
            discount_exception = 0
            for promo in self.promotions_lst:
                if isinstance(promo, promotions.SecondHalfPrice):
                    discount_exception += 1
                elif isinstance(promo, promotions.ThirdOneFree):
                    discount_exception += 1
            if discount_exception == 2:
                # Setting total price and adding overlapping
                # discounts as every 6th product is for free and gets 50% off
                total_price = ((quantity // 6) * self.price * 0.25)
                for promo in self.promotions_lst:
                    total_price += promo.apply_promotion(self, quantity)
                return total_price
            elif discount_exception != 2:
                total_price = 0
                for promo in self.promotions_lst:
                    total_price += promo.apply_promotion(self, quantity)
                return total_price


    def show(self):
        """Returns the product details as string"""
        # If there are no promotions
        if not self.promotions_lst:
            return f"{self.name}, Price: ${self.price}, Quantity: Unlimited, Promotions: None"
        # If there are promotions
        else:
            output_string = f"{self.name}, Price: ${self.price}, Quantity: Unlimited, Promotions:"
            counter = 0
            for promo in self.promotions_lst:
                counter += 1
                if counter == len(self.promotions_lst):
                    output_string += f" {promo.name}"
                else:
                    output_string += f" {promo.name},"
            return output_string


class LimitedProduct(Product):
    """A class representing a product with limited quantity"""
    def __init__(self, name, price, quantity, maximum=1, promotions_lst=None):
        """Initializes the product"""
        super().__init__(name, price, quantity, promotions_lst=promotions_lst)
        self.maximum = maximum


    def buy(self, quantity):
        """Buys a quantity of the product, updates quantity and returns the total price"""
        if quantity <= self.maximum and quantity <= self.quantity:
            self.quantity -= quantity
            if not self.promotions_lst:
                return quantity * self.price
            else:
                discount_exception = 0
                for promo in self.promotions_lst:
                    if isinstance(promo, promotions.SecondHalfPrice):
                        discount_exception += 1
                    elif isinstance(promo, promotions.ThirdOneFree):
                        discount_exception += 1
                if discount_exception == 2:
                    # Setting total price and adding overlapping
                    # discounts as every 6th product is for free and gets 50% off
                    total_price = ((quantity // 6) * self.price * 0.25)
                    for promo in self.promotions_lst:
                        total_price += promo.apply_promotion(self, quantity)
                    return total_price
                elif discount_exception != 2:
                    total_price = 0
                    for promo in self.promotions_lst:
                        total_price += promo.apply_promotion(self, quantity)
                    return total_price
        else:
            raise ValueError(
                f"Not enough quantity({self.quantity})"
                + f" or tried to buy more than maximum({self.maximum})!"
            )


    def show(self):
        """Returns the product details as string"""
        # If there are no promotions
        if not self.promotions_lst:
            return (
                f"{self.name},"
                + f" Price: ${self.price},"
                + f" Limited to {self.maximum} per order!,"
                + f" Promotions: None"
            )
        # If there are promotions
        else:
            output_string = (
                f"{self.name},"
                + f" Price: ${self.price},"
                + f" Limited to {self.maximum} per order!,"
                + f"Promotions:"
            )
            counter = 0
            for promo in self.promotions_lst:
                counter += 1
                if counter == len(self.promotions_lst):
                    output_string += f" {promo.name}"
                else:
                    output_string += f" {promo.name},"
            return output_string


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
