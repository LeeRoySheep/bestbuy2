import pytest
import products


def test_standard_product():
    '''Tests the Product class'''
    product = products.Product("MacBook Air M2", price=1450, quantity=100)
    assert product.show() == "MacBook Air M2, Price: (1450), Quantity: 100"
    assert product.get_quantity() == 100
    assert product.is_active() == True
    product.deactivate()
    assert product.is_active() == False
    product.activate()
    assert product.is_active() == True


def test_negative_quantity():
    '''Tests the Product class with negative quantity'''
    with pytest.raises(ValueError):
        products.Product("MacBook Air M2", price=1450, quantity=-100)


def test_empty_name():
    '''Tests the Product class with empty name'''
    with pytest.raises(ValueError):
        products.Product("", price=1450, quantity=100)


def test_zero_quantity():
    '''Tests the Product class with zero quantity'''
    product = products.Product("MacBook Air M2", price=1450, quantity=0)
    product2 = products.Product("MacBook Air M3", price=1950, quantity=10)
    assert product.is_active() == False
    product2.buy(10)
    assert product2.is_active() == False
    product2.set_quantity(5)
    assert product2.is_active() == True
    product2.set_quantity(0)
    assert product2.is_active() == False


def test_quantity_after_buy():
    '''Tests the product quantity after using buy()'''
    product = products.Product("MacBook Air M2", price=1450, quantity=100)
    assert product.get_quantity() == 100
    assert product.buy(50) == 50*1450
    assert product.get_quantity() == 50


pytest.main()