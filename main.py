import store
import products
import promotions
import copy


def print_main_menu():
    """Prints the store menu"""
    print("\n    Store Menu")
    print("    ----------")
    print("1. List all products in store")
    print("2. Show total amount in store")
    print("3. Make an order")
    print("4. Quit\n")


def print_product_menu(storeobject):
    """Prints the product menu"""
    index = 0
    print("------")
    for product in storeobject.get_all_products():
        index += 1
        print(f"{index}. {product}")
    print("------")


def print_total_product(storeobject):
    """
    print the total amount of product in store to terminal
    """
    print(f"Total of {storeobject.get_total_quantity()} items in store")


def order_products(storeobject):
    """
    function to arange product orders
    """
    order_list = {}
    print_product_menu(storeobject)
    print("When you want to finish order, enter empty text.")
    while True:
        product_index = input("Which product # do you want: ")
        order_quantity = input("What amount do you want: ")
        if not product_index or not order_quantity:
            break
        try:
            if 0 < int(product_index) <= len(storeobject.get_all_products()):
                product = storeobject.get_all_products()[int(product_index) - 1]
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
        if product not in order_list:
            order_list[product] = 0
        order_list[product] += order_amount
    try:
        # making a copy of old product status as exception might stop
        # the order, even if some orders where already booked
        old_products = [copy.copy(product) for product in storeobject.list_of_products]
        print(f"Order made! Total payment: ${storeobject.order(order_list)}")
    except ValueError as val_err:
        #bring order status back to original status
        storeobject.list_of_products = old_products
        print(val_err)


#function dispatcher
functions = {
    "1": print_product_menu,
    "2": print_total_product,
    "3": order_products,
}


def start(storeobject):
    """Starts the store"""
    while True:
        print_main_menu()
        choice = input("Enter your choice: ")
        if choice in ["1","2","3"]:
            functions[choice](storeobject)
        elif choice == "4":
            exit(0)
        else:
            print("Error with your choice! Try again!")


def main():
    """main function to start the store"""
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

    # Add promotions and multi promotions to products
    product_list[0].promotions_lst = second_half_price
    product_list[0].promotions_lst = third_one_free
    # checking that every promotion class only gest added once also working
    product_list[4].promotions_lst = third_one_free
    product_list[2].promotions_lst = thirty_percent
    product_list[3].promotions_lst = twenty_percent
    best_buy = store.Store(product_list)
    """
    products1 = best_buy.get_all_products()
    print(product_list[0])
    print(best_buy.get_total_quantity())
    # Testing the result should return second half price for 15 prods which makes 3.5 free products
    # should also give discount on 12 products of thirty percent which gives 3.6 free products
    # should give 6 products for free as every third product is free which gives us 6 free products
    # This gives us a total of 13.1 free products and leaves us with 4.9 products to pay
    # seems to be calculating as I expected and wanted
    print(best_buy.order({products1[0]: 18}))
    # setup initial stock of inventory
    mac2 = products.Product("MacBook Air M2", price=1450, quantity=100)
    bose2 = products.Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel2 = products.LimitedProduct("Google Pixel 7", price=500, quantity=250, maximum=1)
    # More testing for functionality
    best_buy2 = store.Store([mac2, bose2])
    print(mac2)  # Should print `MacBook Air M2, Price: $1450 Quantity:100`
    print(mac2 > bose2)  # Should print True
    print(mac2 in best_buy2)  # Should print True
    print(pixel2 in best_buy2)  # Should print False
    # Should create new shop with cheapest price all promos and quantities
    best_buy3 = best_buy + best_buy2
    print(best_buy3.get_total_quantity())  # + override works as expected
    for product in best_buy3.list_of_products:
        print(product)
    """
    start(best_buy)

if __name__ == "__main__":
    main()
