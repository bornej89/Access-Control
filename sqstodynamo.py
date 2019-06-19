import boto3
import json
import os
import itertools
import datetime

#this is the trigger for the lambda_handler
#It will kick off whenever a new message enters the sqs queue
def lambda_handler(events, context):
    messages_to_update = []
    messages_to_delete = []
    sqs = boto3.client('sqs')

    #find the correct queueurl to trigger off of
    queue_name = os.environ['QUEUE AS DEFINED IN CLOUDFORMATION TEMPLATE']
    queue_response = sqs.get_queue_url(QueueName=queue_name)
    queue_url = queue_response['QueueUrl']

    #This loop will iterate through the queue and
    #store all the information needed for dynamo
    for record in events['Records']:
        record_json = json.loads(record['body'])
        record_json.update(record['attributes'])
        # Track the information needed to record within Dynamo
        messages_to_update.append(record_json)

        # Track the information to delete the record from the SQS queue
        messages_to_delete.append({
            'Id': record['messageId'],
            'ReceiptHandle': record['receiptHandle']
        })

    #call the function to update the dynamo table
    update_dynamodb(messages_to_update)

    #make sure we clean up the messages in the queue so they don't 
    #hang around forever
    for message in messages_to_delete:
        deleted_message = sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )

    return update_dynamodb(messages_to_update)

#this will check to see if the table exists within dynamo
#if not it will create the table and then write to it

def update_dynamodb(messages_to_update):
    dynamodb = boto3.client('dynamodb')

    # We need to get a table name
    # Check if that table name exists
    # The real secret sauce is below
    # connection to the database is managed through policies
    dynamo_tables = dynamodb.list_tables()['TableNames']

    for message in messages_to_update:
        if ('TABLE NAME') not in dynamo_tables:

            table = dynamodb.create_table(
                    #create the new table
                 }
            )
            print(table)

        # Write data
        put_response = boto3.resource('dynamodb').Table('TABLE NAME']).put_item(
            Item={
                #insert whatever data you want into table
            }
        )

        print(put_response)

