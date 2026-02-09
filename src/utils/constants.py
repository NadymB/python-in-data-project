from datetime import date

SELLER_TYPE = ['Official', 'Marketplace']
PROMOTION_TYPE = ['product', 'category', 'seller', 'flash_sale', 'other']
DISCOUNT_TYPE = {
    0: 'percentage',
    1: 'fixed_amount'
}
ORDER_STATUS = {
    0: 'PLACED', 
    1: 'PAID', 
    2: 'SHIPPED', 
    3: 'DELIVERED', 
    4: 'CANCELLED', 
    5: 'RETURNED'
}

ACTIVE_PRODUCTS_DATE = {
    "from": date(2025, 8, 1),
    "to": date(2025, 10, 31)
}

