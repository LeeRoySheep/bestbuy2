import  products

class Store:
    '''Store class creating a stor with a list of products'''
    def __init__(self, list_of_products):
        self.list_of_products = list_of_products


    def add_product(self, product):
        '''Adds a product to the list of products'''
        self.list_of_products.append(product)


    def remove_product(self, product):
        '''Removes a product from the list of products'''
        self.list_of_products.remove(product)


    def get_total_quantity(self):
        '''Returns the total quantity of all products'''
        return sum([product.get_quantity() for product in self.list_of_products])


    def get_all_products(self):
        '''Returns the list of all active products'''
        active_products = []
        for item in self.list_of_products:
            if item.is_active():
                active_products.append(item)
        return active_products


    def order(self, shopping_list):
        '''Orders a list of products'''
        total_price = 0
        for product_quantity in shopping_list:
            for product in self.list_of_products:
                if product == product_quantity[0]:
                    if product_quantity[1] <= product.get_quantity():
                        total_price += product.buy(product_quantity[1])
                    else:
                        raise ValueError(
                            "Error while making order! Quantity larger than what exists"
                        )
        return total_price


def main():
    '''Main function as using example and for testing purposes'''
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250),
                    ]

    best_buy = Store(product_list)
    products1 = best_buy.get_all_products()
    print(best_buy.get_total_quantity())
    print(best_buy.order([(products1[0], 1), (products1[1], 2)]))

if __name__ == "__main__":
    main()
