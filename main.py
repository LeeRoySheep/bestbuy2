import store
import products

# setup initial stock of inventory
product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250),
                    products.NonStockedProduct("Windows License", price=125),
                    products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                    ]
# add product list to store
best_buy = store.Store(product_list)


def print_main_menu():
    '''Prints the store menu'''
    print("\n    Store Menu")
    print("    ----------")
    print("1. List all products in store")
    print("2. Show total amount in store")
    print("3. Make an order")
    print("4. Quit\n")


def print_product_menu(store_obj):
    '''Prints the product menu'''
    index = 0
    print("------")
    for product in store_obj.list_of_products:
        index += 1
        print(f"{index}. " + product.show())
    print("------")


def start(store_object):
    '''Starts the store'''
    while True:
        print_main_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            print_product_menu(store_object)
        elif choice == "2":
            print(f"Total of {store_object.get_total_quantity()} items in store")
        elif choice == "3":
            order_list = []
            print_product_menu(store_object)
            print("When you want to finish order, enter empty text.")
            while True:
                product_index = input("Which product # do you want: ")
                order_quantity = input("What amount do you want: ")
                if not product_index or not order_quantity:
                    break
                try:
                    product = store_object.list_of_products[int(product_index) - 1]
                    order_amount = int(order_quantity)
                except ValueError:
                    print("Invalid input! Try again!")
                    continue
                except IndexError:
                    print("Invalid product index! Try again!")
                    continue
                order_list.append((product, order_amount))
            try:
                print(f"Order made! Total payment: ${store_object.order(order_list)}")
            except ValueError as val_err:
                print(val_err)
        elif choice == "4":
            break
        else:
            print("Error with your choice! Try again!")


def main():
    '''main function to start the store'''
    start(best_buy)

if __name__ == "__main__":
    main()
