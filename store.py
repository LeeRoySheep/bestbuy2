import products
import promotions

class Store:
    """Store class creating a stor with a list of products"""
    def __init__(self, list_of_products):
        self.list_of_products = list_of_products


    def add_product(self, product):
        """Adds a product to the list of products"""
        self.list_of_products.append(product)


    def remove_product(self, product):
        """Removes a product from the list of products"""
        self.list_of_products.remove(product)


    def get_total_quantity(self):
        """Returns the total quantity of all products"""
        return sum([product.quantity for product in self.list_of_products])


    def get_all_products(self):
        """Returns the list of all active products"""
        active_products = []
        for item in self.list_of_products:
            if item.is_active():
                active_products.append(item)
        return active_products


    def order(self, shopping_list):
        """Orders a list of products"""
        total_price = 0
        for product_quantity in shopping_list:
            for product in self.list_of_products:
                if product == product_quantity[0]:
                    total_price += product.buy(product_quantity[1])
        return total_price


    def __contains__(self, product):
        """Checks if a product is in the store"""
        return product.name in [prod.name for prod in self.list_of_products]


    def __add__(self, other):
        """Adds two stores together"""
        new_products_list = []
        for product in self.list_of_products:
            new_products_list.append(product)
        new_store = Store(new_products_list)
        for product in other.list_of_products:
            if product in new_store:
                for ind, prod in enumerate(new_store.list_of_products):
                    if prod.name == product.name:
                        new_store.list_of_products[ind].quantity = product.quantity + prod.quantity
                        print(new_store.list_of_products[ind].quantity)
                        if product < prod:
                            new_store.list_of_products[ind].price = product.price
            else:
                new_products_list.append(product)
        return Store(new_products_list)



def main():
    """Main function as using example and for testing purposes"""

    # setup initial stock of inventory
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250),
                    products.NonStockedProduct("Windows License", price=125),
                    products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                    ]

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)
    twenty_percent = promotions.PercentDiscount("20% off!", percent=20)

    # Add promotions to products
    product_list[0].promotions_lst = second_half_price
    product_list[0].promotions_lst = third_one_free
    product_list[1].promotions_lst = third_one_free
    product_list[1].promotions_lst = thirty_percent
    product_list[3].promotions_lst = twenty_percent
    best_buy = Store(product_list)
    products1 = best_buy.get_all_products()
    print(product_list[0])
    print(best_buy.get_total_quantity())
    print(best_buy.order([(products1[0], 18)]))
    # setup initial stock of inventory
    mac2 = products.Product("MacBook Air M2", price=1450, quantity=100)
    bose2 = products.Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel2 = products.LimitedProduct("Google Pixel 7", price=500, quantity=250, maximum=1)

    best_buy2 = Store([mac2, bose2])
    print(mac2)  # Should print `MacBook Air M2, Price: $1450 Quantity:100`
    print(mac2 > bose2)  # Should print True
    print(mac2 in best_buy2)  # Should print True
    print(pixel2 in best_buy2)  # Should print False
    best_buy3 = best_buy + best_buy2
    print(best_buy3.get_total_quantity())
    for product in best_buy3.list_of_products:
        print(product)

if __name__ == "__main__":
    main()
