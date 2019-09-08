import json
import boto3
rek = boto3.client('rekognition')
lmb = boto3.client('lambda')
import time

def lambda_handler(event, context):
    print(event)
    sns_message_string = event['Records'][0]['Sns']['Message']
    print(sns_message_string)
    parsed = json.loads(sns_message_string)
    job_id = parsed['JobId']
    status = parsed['Status']
    fileName = "vid/" + parsed["JobTag"] 
    if status == "SUCCEEDED":
        try:
            print("In try")
            getDetectionResults(job_id,fileName)
        except:
            print("in except")
            time.sleep(3)
            getDetectionResults(job_id,fileName)
    else:
        print("not succeeded...")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def getDetectionResults(job_id,fileName):
    print("In detection results")
    response = rek.get_content_moderation(JobId=job_id)
    print(response)
    for labelDetection in response['ModerationLabels']:
        label=labelDetection['ModerationLabel']
        if label in ["Violence", "Graphic Violence Or Gore","Physical Violence","Weapon Violence","Weapons"]:
            response = lmb.invoke(FunctionName='sendNotification',Payload=json.dumps({'object_name':fileName}))
            return
 
