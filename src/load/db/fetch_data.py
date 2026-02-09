def get_products_by_seller(db_connection):
    query = """
        SELECT product_id, seller_id, discount_price
        FROM product
    """
    
    try:
        with db_connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        seller_products = {}

        for product_id, seller_id, discount_price in rows:
            seller_products.setdefault(seller_id, []).append({
                "product_id": product_id,
                "discount_price": discount_price
            })

        return seller_products

    except Exception as e:
        print(f"Error fetching products by seller: {e}")
        raise