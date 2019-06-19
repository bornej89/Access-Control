# Lambda
This lambda function reads JSON from an SQS Queue and inserts it into a dynamo DB.

I have deployed this using a cloudformation template and have attached a policy to the lambda function to allow it to write to dynamo and read/delete from the sqs queue.

This is done by defining what actions the lambda function can do, and pointing those actions towards a specific resource ARN.

