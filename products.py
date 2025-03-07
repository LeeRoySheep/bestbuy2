import promotions


class Product:
    """A class representing a product"""
    def __init__(self, name, price, quantity, promotions_lst=None):
        """Initializes the product"""
        self._name = name
        self._price = price
        self._quantity = quantity
        self._promotions_lst = promotions_lst
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

    @property
    def promotions_lst(self):
        """Returns the promotions of the product"""
        return self._promotions_lst

    @promotions_lst.setter
    def promotions_lst(self, promotion):
        """Sets the promotions of the product"""
        if not self._promotions_lst:
            self._promotions_lst = []
            self._promotions_lst.append(promotion)
        else:
            new_promotions = []
            for promo in self._promotions_lst:
                if not isinstance(promo, type(promotion)):
                    new_promotions.append(promo)
            new_promotions.append(promotion)
            self._promotions_lst = new_promotions

    @property
    def quantity(self):
        """Returns the quantity of the product"""
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of the product"""
        if quantity == 0:
            self._quantity = 0
            self.deactivate()
        if quantity > 0:
            if self.quantity == 0:
                self.activate()
            self._quantity = quantity
        if quantity < 0:
            raise ValueError("Quantity cannot be negative!")

    @property
    def price(self):
        """Returns the price of the product"""
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of the product"""
        if price >= 0:
            self._price = price
        else:
            raise ValueError("Price cannot be negative!")

    @property
    def name(self):
        """Returns the name of the product"""
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of the product"""
        if name:
            self._name = name
        else:
            raise ValueError("Name cannot be empty!")

    def is_active(self):
        """Returns the active status of the product"""
        return self._active

    def activate(self):
        """Activates the product"""
        self._active = True

    def deactivate(self):
        """Deactivates the product"""
        self._active = False

    def __str__(self):
        """Returns the product details as string"""
        if not self.promotions_lst:
            return (
                f"{self.name},"
                + f" Price: ${self.price}, "
                + f" Quantity: {self.quantity},"
                + " Promotions: None"
            )

        output_string = (
            f"{self.name},"
            + f" Price: ${self.price},"
            + f" Quantity: {self.quantity},"
            + " Promotions:"
        )
        counter = 0
        for promo in self.promotions_lst:
            counter += 1
            if counter == len(self.promotions_lst):
                output_string += f" {promo.name}"
            else:
                output_string += f" {promo.name},"
        return output_string

    def __gt__(self, other):
        """Returns True if the price of the product is greater than the other"""
        return self.price > other.price

    def __lt__(self, other):
        """Returns True if the price of the product is less than the other"""
        return self.price < other.price

    def buy(self, quantity):
        """Buys a quantity of the product, updates quantity and returns the total price"""
        # Checking for overlapping discounts
        if 0 < quantity <= self.quantity:
            self.quantity -= quantity
            if self.quantity == 0:
                self.deactivate()
            if not self.promotions_lst:
                return quantity * self.price
            if len(self.promotions_lst) == 1:
                return self.promotions_lst[0].apply_promotion(self, quantity)
            discount_exception = False
            for promo in self.promotions_lst:
                # as every 3rd product is for free and gets 100% off
                # we need to make sure not to discount the free product
                # other double discounts are allowed and calculated to full extent
                if isinstance(promo, promotions.ThirdOneFree):
                    discount_exception = True
            if discount_exception:
                # Setting total price and adding overlapping
                # discounts as every 6th product is for free and gets 50% off
                total_price = quantity * self.price
                for promo in self.promotions_lst:
                    if isinstance(promo, promotions.SecondHalfPrice):
                        total_price -= (
                                ((quantity - (quantity // 6)) * self.price)
                                - promo.apply_promotion(self, (quantity - (quantity // 6)))
                        )
                    elif isinstance(promo, promotions.ThirdOneFree):
                        total_price -= (
                                (quantity * self.price)
                                - promo.apply_promotion(self, quantity)
                        )
                    else:
                        total_price -= (
                                ((quantity - quantity // 3) * self.price)
                                - promo.apply_promotion(self, quantity - (quantity // 3))
                        )
                return total_price

            total_price = quantity * self.price
            for promo in self.promotions_lst:
                total_price -= quantity * self.price - promo.apply_promotion(self, quantity)
            return total_price
        raise ValueError("Not enough quantity in store or negative quantity!")


class NonStockedProduct(Product):
    """A class representing a product that is not stocked"""
    def __init__(self, name, price, promotions_lst=None):
        """Initializes the product"""
        super().__init__(name, price, quantity=0, promotions_lst=promotions_lst)
        self.activate()


    def buy(self, quantity):
        """Buys a quantity of the product and returns the total price"""
        if quantity > 0:
            if not self.promotions_lst:
                return quantity * self.price
            if len(self.promotions_lst) == 1:
                return self.promotions_lst[0].apply_promotion(self, quantity)
            discount_exception = False
            for promo in self.promotions_lst:
                # as every 3rd product is for free and gets 100% off
                # we need to make sure not to discount the free product
                # other double discounts are allowed and calculated to full extent
                if isinstance(promo, promotions.ThirdOneFree):
                    discount_exception = True
            if discount_exception:
                # Setting total price and adding overlapping
                # discounts as every 6th product is for free and gets 50% off
                total_price = quantity * self.price
                for promo in self.promotions_lst:
                    if isinstance(promo, promotions.SecondHalfPrice):
                        total_price -= (
                                ((quantity - (quantity // 6)) * self.price)
                                - promo.apply_promotion(self, (quantity - (quantity // 6)))
                        )
                    elif isinstance(promo, promotions.ThirdOneFree):
                        total_price -= (
                                (quantity * self.price)
                                - promo.apply_promotion(self, quantity)
                        )
                    else:
                        total_price -= (
                                ((quantity - quantity // 3) * self.price)
                                - promo.apply_promotion(self, quantity - (quantity // 3))
                        )
                return total_price
            total_price = quantity * self.price
            for promo in self.promotions_lst:
                total_price -= quantity * self.price - promo.apply_promotion(self, quantity)
            return total_price
        raise ValueError("Quantity cannot be negative or smaller than 0")

    def __str__(self):
        """Returns the product details as string"""
        # If there are no promotions
        if not self.promotions_lst:
            return f"{self.name}, Price: ${self.price}, Quantity: Unlimited, Promotions: None"
        # If there are promotions
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
    def __init__(self, name, price, quantity, **kwargs):
        """Initializes the product"""
        super().__init__(name, price, quantity, promotions_lst=kwargs.get("promotions_lst"))
        self.maximum = kwargs.get("maximum", 1)


    def buy(self, quantity):
        """Buys a quantity of the product, updates quantity and returns the total price"""
        if 0 < quantity <= self.maximum and quantity <= self.quantity:
            self.quantity -= quantity
            if not self.promotions_lst:
                return quantity * self.price
            if len(self.promotions_lst) == 1:
                return self.promotions_lst[0].apply_promotion(self, quantity)
            discount_exception = False
            for promo in self.promotions_lst:
                # as every 3rd product is for free and gets 100% off
                # we need to make sure not to discount the free product
                # other double discounts are allowed and calculated to full extent
                if isinstance(promo, promotions.ThirdOneFree):
                    discount_exception = True
            if discount_exception:
                # Setting total price and adding overlapping
                # discounts as every 6th product is for free and gets 50% off
                # and every 3rd product is actually for free and  gets xx percent discount
                total_price = quantity * self.price
                for promo in self.promotions_lst:
                    if isinstance(promo, promotions.SecondHalfPrice):
                        total_price -= (
                                ((quantity - (quantity // 6)) * self.price)
                                - promo.apply_promotion(self, (quantity - (quantity // 6)))
                        )
                    elif isinstance(promo, promotions.ThirdOneFree):
                        total_price -= (
                                (quantity * self.price)
                                - promo.apply_promotion(self, quantity)
                        )
                    else:
                        total_price -= (
                                ((quantity - quantity // 3) * self.price)
                                - promo.apply_promotion(self, quantity - (quantity // 3))
                        )
                return total_price
            total_price = quantity * self.price
            for promo in self.promotions_lst:
                total_price -= quantity * self.price - promo.apply_promotion(self, quantity)
            return total_price
        raise ValueError(
                f"Not enough stock or negative quantity({self.quantity})"
                + f" or tried to buy more than maximum({self.maximum})!"
            )


    def __str__(self):
        """Returns the product details as string"""
        # If there are no promotions
        if not self.promotions_lst:
            return (
                f"{self.name},"
                + f" Price: ${self.price},"
                + f" Limited to {self.maximum} per order!,"
                + " Promotions: None"
            )
        # If there are promotions
        output_string = (
            f"{self.name},"
            + f" Price: ${self.price},"
            + f" Limited to {self.maximum} per order!,"
            + "Promotions:"
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

    print(bose)
    print(mac)

    bose.quantity = 1000
    print(bose)

if __name__ == "__main__":
    main()
