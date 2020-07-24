import json
import boto3
import os

client = boto3.client('ses')
#environment variable
sns_topic = os.environ['BOUNCE_SNS_TOPIC']

def lambda_handler(event, context):
    # get list of all emails and domains (Identities)
    identityList = client.list_identities(
    )
    print(identityList['Identities'])
    #check if the identities are configured with BounceTpic
    for identity in identityList['Identities']:
        print("identity=", identity)
        response = client.get_identity_notification_attributes(
            Identities=[
                identity,
            ]
        )
        print("response=", response)
        #Check if the identity has BounceTopic configured already
        bounceTopicExists = "BounceTopic" in response['NotificationAttributes'][identity]
        print(bounceTopicExists)
        #if identity doesn't have a BounceTopic, configure it
        if bounceTopicExists == False:
            bounce_notif = client.set_identity_notification_topic(Identity=identity, NotificationType="Bounce", SnsTopic=sns_topic)
            print(bounce_notif)
    return {
        'statusCode': 200,
        'body': json.dumps('SES Bounce notifications configured succesfully !')
    }
