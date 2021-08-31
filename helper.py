import json

class FilePaths:
    ITEM_LIMIT = 'item_limits.json'
    CATEGORY_LIMIT = 'category_limits.json'
    ORDER_ITEM_QTY = 'order_item_quantity.json'
    ORDER_CATEGORY_QTY = 'order_category_quantity.json'


def get_quantities(file_name, date):
    with open(file_name) as f:
        hashmap = json.load(f)
    return hashmap[date]


def can_fulfil_order(delivery_date, items_details):

    item_limits = get_quantities(FilePaths.ITEM_LIMIT, delivery_date)
    category_limits = get_quantities(FilePaths.CATEGORY_LIMIT, delivery_date)
    current_item_quantity = get_quantities(FilePaths.ORDER_ITEM_QTY, delivery_date)
    current_category_quantity = get_quantities(FilePaths.ORDER_CATEGORY_QTY, delivery_date)

    order_categorical_qty = {}
    order_items_qty = {}

    for item in items_details:
        if order_categorical_qty.get(item['category']):
            order_categorical_qty[item['category']] += item['quantity']
        else:
            order_categorical_qty[item['category']] = item['quantity']
        
        if order_items_qty.get(item['item_id']):
            order_items_qty[item['item_id']] += item['quantity']
        else:
            order_items_qty[item['item_id']] = item['quantity']
    
    for category_key in order_categorical_qty.keys():
        current_qty = current_category_quantity.get(category_key)
        limit_qty = category_limits.get(category_key)
        order_qty = order_categorical_qty.get(category_key)
        
        if current_qty + order_qty > limit_qty:
            return False
    for item_key in order_items_qty.keys():
        current_qty = current_item_quantity.get(item_key)['quantity']
        limit_qty = item_limits.get(item_key)['quantity']
        order_qty = order_items_qty.get(item_key)

        if current_qty + order_qty > limit_qty:
            return False
    
    return True

def read_json(file_name):
    with open(file_name) as f:
        hashmap = json.load(f)
    return hashmap

def write_json(dict_object, file_name):
    json_object = json.dumps(dict_object, indent = 4)
    with open(file_name, "w") as outfile:
        outfile.write(json_object)


def update_order_quantities(delivery_date, item_details):

    current_item_quantity = get_quantities(FilePaths.ORDER_ITEM_QTY, delivery_date)
    current_category_quantity = get_quantities(FilePaths.ORDER_CATEGORY_QTY, delivery_date)

    for item in item_details:
        current_item_quantity[item['item_id']]['quantity'] += item['quantity']
        current_category_quantity[item['category']] += item['quantity']
    
    items_order = read_json(FilePaths.ORDER_ITEM_QTY)
    category_order = read_json(FilePaths.ORDER_CATEGORY_QTY)

    items_order[delivery_date] = current_item_quantity
    category_order[delivery_date] = current_category_quantity

    write_json(items_order, FilePaths.ORDER_ITEM_QTY)
    write_json(category_order, FilePaths.ORDER_CATEGORY_QTY)
    