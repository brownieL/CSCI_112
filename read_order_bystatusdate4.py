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
    username = "tgrimes1"
    status="Placed"
    date= "1987-02-26"
    profile=user.query_user_profile(username)
    #print all pending orders of tgrimes ordered on 1987=02=26
    orders = query_userorder_statusdate(username, status, date)
    list =[]
    for indiv_order in orders: 
        list.append(indiv_order['sk'])
    number_of_order = len(list)
    if number_of_order>1: 
        print('The ' + status +' order of user ' + username+ ' on '+ date + ' are:')
        for i in list: 
            print(i)
        print('User ' + username+ "'s adress include " + str(profile[0]['address'])+', while their email is '+ str(profile[0]['email'])+'.')
    elif number_of_order==1: 
        print('The ' + status +' order of user ' + username+ ' on '+ date + ' is:'+ str(list[0]))
        print('User ' + username+ "'s adress include " + str(profile[0]['address'])+', while their email is '+ str(profile[0]['email'])+'.')
    elif number_of_order==0: 
        print('User ' + username+ ' has no '+ status +' orders on ' + date+'.')
