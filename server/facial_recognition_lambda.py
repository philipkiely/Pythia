import json
import boto3
rek = boto3.client('rekognition')
sqs = boto3.client('sqs')
import time

def lambda_handler(event, context):
    print(event)
    sns_message_string = event['Records'][0]['Sns']['Message']
    parsed = json.loads(sns_message_string)
    job_id = parsed['JobId']
    status = parsed['Status']
    fileName = parsed['JobTag']

    if status == "SUCCEEDED":
        try:
            people = getDetectionResults(job_id,fileName)
        except:
            time.sleep(2)
            people = getDetectionResults(job_id,fileName)
             
    return {
        'statusCode': 200,
        'body': people
    }



def getDetectionResults(jot_id,fileName):
    maxResults = 1000
    response = rek.get_label_detection(JobId=jot_id,
                                    MaxResults=maxResults,
                                    SortBy='TIMESTAMP')

    for labelDetection in response['Labels']:
        label=labelDetection['Label']
        
        if label['Name'] in ['Human', 'Person', 'Man', 'Male', 'Woman','Female'] and label['Confidence'] > 0.9:
            print("POTENTIAL INTRUDER!!")
            sqs.send_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/998539017710/pennappsqueue.fifo',MessageBody='Potential intruder', MessageGroupId=fileName)
            return
    
   
