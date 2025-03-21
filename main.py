import store
import products
import promotions
import copy

# setup initial stock of inventory
product_list = [ products.Product("MacBook Air M2", price=1450, quantity=100),
                 products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                 products.Product("Google Pixel 7", price=500, quantity=250),
                 products.NonStockedProduct("Windows License", price=125),
                 products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
               ]

# Create promotion catalog
second_half_price = promotions.SecondHalfPrice("Second Half price!")
third_one_free = promotions.ThirdOneFree("Third One Free!")
thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

# Add promotions to products
product_list[0].promotions_lst = second_half_price
product_list[1].promotions_lst = third_one_free
product_list[3].promotions_lst = thirty_percent
# add product list to store
best_buy = store.Store(product_list)


def print_main_menu():
    """Prints the store menu"""
    print("\n    Store Menu")
    print("    ----------")
    print("1. List all products in store")
    print("2. Show total amount in store")
    print("3. Make an order")
    print("4. Quit\n")


def print_product_menu(store_obj):
    """Prints the product menu"""
    index = 0
    print("------")
    for product in store_obj.get_all_products():
        index += 1
        print(f"{index}. {product}")
    print("------")


def start(store_object):
    """Starts the store"""
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
                    if 0 < int(product_index) <= len(store_object.get_all_products()):
                        product = store_object.get_all_products()[int(product_index) - 1]
                        order_amount = int(order_quantity)
                    else:
                        print("Wrong # choose a number from the list of products!")
                        continue
                except ValueError:
                    print("Invalid input! Try again!")
                    continue
                except IndexError:
                    print("Invalid product index! Try again!")
                    continue
                order_list.append((product, order_amount))
            try:
                # making a copy of old product status as exception might stop
                # the orde, even if some orders where already booked
                old_products = [copy.copy(product) for product in store_object.list_of_products]
                print(f"Order made! Total payment: ${store_object.order(order_list)}")
            except ValueError as val_err:
                #bring order status back to original status
                store_object.list_of_products = old_products
                print(val_err)
        elif choice == "4":
            break
        else:
            print("Error with your choice! Try again!")


def main():
    """main function to start the store"""
    start(best_buy)

if __name__ == "__main__":
    main()
