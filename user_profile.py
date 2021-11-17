#!/usr/bin/env python3
import boto3
from boto3.dynamodb.conditions import Key


"""
Creates and places user profiles which includes username, SK as with default
value of 'PROFILE', email, and address which is still empty in the table. 

It accepts the username, fullname, and email. 
"""
def create_user(username, fullname, email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('new_users-orders-items')
    
    user = {
        'pk'      : '#USER#{0}'.format(username), 
        'sk'      : 'PROFILE',
        'email'   : email,
        'address' : {}
    }
    table.put_item(Item=user)
    print("User {0} created".format(username))
    

"""
Adds address to the user profile. It also includes a label to the address. 

It accepts the username, address_label, and address. 
"""
def add_address(username, address_label, address):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('new_users-orders-items')
    
    try:
        # Update item in table for the given username key.
        retsp = table.update_item(
            Key={'pk' : '#USER#{0}'.format(username),
                 'sk' : 'PROFILE'
            },
            UpdateExpression='SET address.#address = :address',
            ExpressionAttributeNames={'#address' : address_label},
            ExpressionAttributeValues={':address': address},
            ConditionExpression = "attribute_not_exists(address.#address)"
            )
        print("Address added")
    except Exception as err:
        print("Error message {0}".format(err))

"""
Queries for  the user profile given the username 
The username does not include the '#USER#'
"""
def query_user_profile(username):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('new_users-orders-items')
    response = table.query(
        KeyConditionExpression=Key('pk').eq('#USER#{0}'.format(username)) & 
                               Key('sk').eq('PROFILE')
    )
    return response['Items']