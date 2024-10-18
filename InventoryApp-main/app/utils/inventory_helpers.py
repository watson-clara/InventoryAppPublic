def calculate_stock_status(quantity, min_quantity, max_quantity):
    if quantity <= min_quantity:
        return 'out of stock'
    elif quantity < max_quantity:
        return 'low stock'
    else:
        return 'in stock'





