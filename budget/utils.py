from .models import Prices

def get_quantity(quantity):
    price = 0
    total = 0
    
    if quantity <= 5:
        price = Prices.objects.get(value=1).price
        total = quantity * price

    elif quantity > 5 and quantity <= 10:
        price = Prices.objects.get(value=2).price
        total = quantity * price

    elif quantity > 11 and quantity <= 30:
        price = Prices.objects.get(value=3).price
        total = quantity * price

    elif quantity > 30:
        price = Prices.objects.get(value=4).price
        total = quantity * price

    return price, total
