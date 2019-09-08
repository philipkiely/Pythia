import json
import boto3

rek = boto3.client('rekognition')
sqs = boto3.client('sqs')
lmb = boto3.client('lambda')
 
def lambda_handler(event, context):
    print(event)
    sns_message_string = event['Records'][0]['Sns']['Message']
    print(sns_message_string)
    parsed = json.loads(sns_message_string)
    job_id = parsed['JobId']
    status = parsed['Status']
    fileName = "vid/" + parsed["JobTag"] 
    #query = table.get_item(Key={"videoChunkId": fileName})
    #if 'Item' in query.keys():
    #    print("Already done")
    #else:
    if status == "SUCCEEDED":
        getDetectionResults(job_id,fileName)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def getDetectionResults(job_id,fileName):
    maxResults = 100
    paginationToken = ''
 
    response = rek.get_face_search(JobId=job_id,
                                    MaxResults=maxResults,
                                    NextToken=paginationToken)
    for person in response["Persons"]:
        if person["FaceMatches"] != []:
            for match in person["FaceMatches"]:
                if match["Similarity"] > 0.8:
                    #all good, found familiar face
                    print("familiar faces")
                    return
                
    if response["Persons"] != []: 
        print("UNAUTHORIZED AAA")
        response = lmb.invoke(FunctionName='sendNotification',Payload=json.dumps({'object_name':fileName}))
        #if we get here, there are unauthorized folks, so text owner
        
    resp = sqs.receive_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/998539017710/pennappsqueue.fifo')
    
    if "Messages" in resp.keys():
        print("Noticed person but no face. potential intruder")
        response = lmb.invoke(FunctionName='sendNotification',Payload=json.dumps({'object_name':fileName}))
        
    print("Bye")    
    return 

    
