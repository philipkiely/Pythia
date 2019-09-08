import json
import time
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import boto3
client_s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("called")
    signature_key = event['video_key']
    s3_response = client_s3.head_object(Bucket='pennapps-superunique-name-123',Key=signature_key)
    video = client_s3.get_object(Bucket='pennapps-superunique-name-123',Key='vid/{}.mp4'.format(s3_response['Metadata']['timestamp']))
    camera_public = client_s3.get_object(Bucket='pennapps-superunique-name-123',Key='public.pem')
    server_private = client_s3.get_object(Bucket='pennapps-superunique-name-123',Key='server_private.pem')
    print(s3_response)
    client_signature = bytes(s3_response['Metadata']['signature'][2:-1], 'utf-8')
    print("camera", client_signature)
    tstamp = int(time.time()) #new
    key = RSA.import_key(camera_public['Body'].read())
    h = SHA256.new(s3_response['Metadata']['previous'].encode('utf-8') + s3_response['Metadata']['timestamp'].encode('utf-8') + video['Body'].read())
    verifier = pss.new(key)
    try:
        verifier.verify(h, client_signature)
        print("verified")
        # Sign it again
        signing_key = RSA.import_key(server_private['Body'].read()) #server private
        h = SHA256.new(str(tstamp).encode('utf-8') + client_signature)
        signature = pss.new(signing_key).sign(h)
        client_s3.put_object(Bucket='pennapps-superunique-name-123', Key='{}_server_signature.txt'.format(signature_key), Body=signature)
        print(signature)
        if tstamp < int(s3_response['Metadata']['timestamp']) + 60: # 1 minute tolerance
            print("The video is authentic.")
        else:
            print("The video may be pre-recorded")
    except (ValueError, TypeError):
        print("The signature is not authentic.")
    return {
        'statusCode': 200,
        'body': json.dumps("hello")
    }
