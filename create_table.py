#!/usr/bin/env python
"""
This file defines the table to be created which is named "new_users-orders-items" 
where the PK is partition_key while SK is sort_key

The table has two indexes: 
    one local secondary index named "lsi_status_ordereddate_index" where the SK is lsi
    one global secondary index named "gsi_status_order_index" where the PK is gsi_pk and the SK is sort_key. 
    
"""
import boto3

def create_new_users_status_date_table(
        ddb_table_name,
        partition_key,
        sort_key, 
        gsi_pk,
        lsi
        ):

    dynamodb = boto3.resource('dynamodb')

    # The variables below transform the arguments into the parameters expected by dynamodb.create_table.

    table_name = ddb_table_name
    
    attribute_definitions = [
        {'AttributeName': partition_key, 'AttributeType': 'S'},
        {'AttributeName': sort_key, 'AttributeType': 'S'}, 
        {'AttributeName': gsi_pk, 'AttributeType': 'S'}, 
        {'AttributeName': lsi, 'AttributeType': 'S'}
    ]
    
    key_schema = [{'AttributeName': partition_key, 'KeyType': 'HASH'}, 
                  {'AttributeName': sort_key, 'KeyType': 'RANGE'}]
                  
    provisioned_throughput = {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10}
        
    local_secondary_indexes = [{
            'IndexName': 'lsi_status_ordereddate_index',
            'KeySchema': [
                {'AttributeName': partition_key, 'KeyType': 'HASH'},
                {'AttributeName': lsi, 'KeyType': 'RANGE'}],
            'Projection': {'ProjectionType': 'INCLUDE',
                           'NonKeyAttributes': ['sk']
            }
    }]
    
    global_secondary_indexes = [{
        'IndexName': 'gsi_status_order_index',
        'KeySchema': [
            {'AttributeName': gsi_pk, 'KeyType': 'HASH'},
            {'AttributeName': sort_key, 'KeyType': 'RANGE'}],
        'Projection': {'ProjectionType': 'KEYS_ONLY'
        },
        'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10}
    }]
    
    try:
        # Create a DynamoDB table with the parameters provided
        table = dynamodb.create_table(TableName=table_name,
                                      KeySchema=key_schema,
                                      AttributeDefinitions=attribute_definitions,
                                      ProvisionedThroughput=provisioned_throughput,
                                      LocalSecondaryIndexes=local_secondary_indexes, 
                                      GlobalSecondaryIndexes=global_secondary_indexes
                                      )
        return table
    except Exception as err:
        print("{0} Table could not be created".format(table_name))
        print("Error message {0}".format(err))

if __name__ == '__main__':
    table = create_new_users_status_date_table("new_users-orders-items", "pk", "sk", "status","status_date")
