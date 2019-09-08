import json
import boto3
sns = boto3.client('sns')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    name_of_s3_object = event['object_name']
    #url = 'https://pennapps-superunique-name-123.s3.amazonaws.com/' + name_of_s3_object
    url = s3.generate_presigned_url('get_object',Params={'Bucket': 'pennapps-superunique-name-123',
                                                            'Key': name_of_s3_object})
                                                    
    sns.publish(TopicArn='arn:aws:sns:us-east-1:998539017710:warningTopic',
    Message="Potential suspicious activity has been recorded:\n See: {}".format(url))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
