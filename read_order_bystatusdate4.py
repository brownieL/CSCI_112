import user_profile as user
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key

"""
This returns the records that have the same username, status and order_date. 
In order to query with three attributes the status_date is a concat of the status and the order_date.
It accepts the username, status, and date. The date is a string in the format of 'YYYY-MM-DD'
"""
def query_userorder_statusdate(username, status, date):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('new_users-orders-items')
    response = table.query(
        IndexName='lsi_status_ordereddate_index',
        KeyConditionExpression=Key('pk').eq('#USER#{0}'.format(username)) & 
                               Key('status_date').eq('#STATUS#{0}#DATE#{1}'.format(status, date))
    )
    return response['Items']
    

"""
It prints the profile of user "tgrimes1
It also prints the "Placed" orders of user "tgrimes1" on "1987-02-26" 
"""
if __name__ == '__main__':

    print(user.query_user_profile("tgrimes1"))
    
    #print all pending orders of tgrimes ordered on 1987=02=26
    orders = query_userorder_statusdate("tgrimes1", "Placed", "1987-02-26")
    for indiv_order in orders:
        print(indiv_order['sk'])