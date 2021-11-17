import boto3
from boto3.dynamodb.conditions import Key

"""
Returns the record/s of orders with a 'Pending' status 
There are no inputs needed 
"""
def query_pending_orders(): 
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('new_users-orders-items')
    response = table.query(
        IndexName='gsi_status_order_index',
        KeyConditionExpression=Key('status').eq('Pending') & 
                               Key('sk').begins_with('#ORDER#')
    )
    return response['Items']

"""
print all pending orders
"""

if __name__ == '__main__':
    orders = query_pending_orders()
    list =[]
    #prints only the unique order bumbers
    for indiv_order in orders:
        order_num= indiv_order['sk']
        if order_num not in list:
            print(order_num)
            list.append(order_num)
            
            
