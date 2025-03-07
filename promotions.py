from abc import ABC, abstractmethod


class Promotion(ABC):
    """An abstract class representing a promotion."""
    def __init__(self, name):
        """Initializes the promotion."""
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity):
        """Calculates the discount for the cart."""
        pass


class SecondHalfPrice(Promotion):
    """A class representing a promotion where
    the second product is half price."""
    def __init__(self, name):
        """Initializes the promotion."""
        super().__init__(name)

    def apply_promotion(self, product, quantity):
        """Calculates the discount for the cart."""
        if quantity % 2 == 0:
            return product.price * quantity * 0.75
        else:
            return (product.price * quantity * 0.75) + (product.price * 0.25)


class ThirdOneFree(Promotion):
    """A class representing a promotion where the third product is free."""
    def __init__(self, name):
        """Initializes the promotion."""
        super().__init__(name)

    def apply_promotion(self, product, quantity):
        """Calculates the discount for the cart."""
        return (product.price * quantity) - ((quantity // 3) * product.price)


class PercentDiscount(Promotion):
    """A class representing a promotion where a percentage is discounted."""
    def __init__(self, name, percent):
        """Initializes the promotion."""
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity):
        """Calculates the discount for the cart."""
        return product.price * quantity * (100 - self.percent) / 100
