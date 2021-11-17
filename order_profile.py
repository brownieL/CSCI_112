#!/usr/bin/env python3
import boto3
from boto3.dynamodb.conditions import Key
import hashlib
import random
from decimal import Decimal

"""
Adds item to the table 
It includes the item_id, order_id, product_name, quantity, 
price, and a status with default value of "Pending"

The item_id is randomly generated. 

It accepts order_id, product_name, quantity, and price. 
"""
def add_item(order_id, product_name, quantity, price): 
    item_id = hashlib.sha256(product_name.encode()).hexdigest()[:8]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('new_users-orders-items')
    
    item = {
        'pk'           : '#ITEM#{0}'.format(item_id), 
        'sk'           : '#ORDER#{0}'.format(order_id),
        'product_name' : product_name,
        'quantity'     : quantity,
        'price'        : price,
        'status'       : "Pending"
    }
    table.put_item(Item=item)
    print("Added {0} to order {1}".format(product_name, order_id))


"""
Adds orders of a user in the table. Includes the address, a default status of 
"Placed", order_date, and a concat of the status and dat called status_date. 

It accepts the username, address, items, and order_date.
"""
def checkout(username, address, items, order_date): 
    # Generate order ID. In real life, there are better
    # ways of doing this
    order_id = hashlib.sha256(str(random.random()).encode()).hexdigest()[:random.randrange(1, 20)]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('new_users-orders-items')
    
    status="Placed"
    
    item = {
        'pk'      : '#USER#{0}'.format(username), 
        'sk'      : '#ORDER#{0}'.format(order_id),
        'address' : address,
        'status'  : status, 
        'order_date'    : order_date, 
        'status_date': '#STATUS#{0}#DATE#{1}'.format(status, order_date)
    }
    table.put_item(Item=item)
    
    for item in items:
        add_item(order_id, 
                 item['product_name'], 
                 item['quantity'], 
                 item['price']
                 )

