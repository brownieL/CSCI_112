import boto3
from boto3.dynamodb.conditions import Key

"""
Returns the record/s of orders with a stated status 
The only input needed is the status
"""
def query_pending_orders(status): 
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('new_users-orders-items')
    response = table.query(
        IndexName='gsi_status_order_index',
        KeyConditionExpression=Key('status').eq(status) & 
                               Key('sk').begins_with('#ORDER#')
    )
    return response['Items']

"""
print all pending orders
"""

if __name__ == '__main__':
    orders = query_pending_orders('Pending')
    list =[]
    #prints only the unique order bumbers
    for indiv_order in orders:
        order_num= indiv_order['sk']
        if order_num not in list:
                print(order_num)
                list.append(order_num)
    number_of_pendingorder= len(list)
    if number_of_pendingorder>1: 
        print('There are '+ str(number_of_pendingorder) + ' pending orders.')
    elif number_of_pendingorder==1: 
        print('There is '+ str(number_of_pendingorder) + ' pending order.')
    elif number_of_pendingorder==0: 
        print('There is no pending order.')
            
            
