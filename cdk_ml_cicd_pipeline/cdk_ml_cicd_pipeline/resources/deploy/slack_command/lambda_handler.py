import json
import base64
import re
from urllib.parse import unquote
import boto3
import os

client = boto3.client('stepfunctions')
sf_arn = os.getenv("STATEMACHINEARN"))

def handler(event, context):
    
    input_event = base64.b64decode(event['body'].encode()).decode('utf-8')
    
    try:
        found = re.search('text=(.+?)&', input_event).group(1)
        print(found)
    except AttributeError:
        pass
    
    sf_list = found.split('+')
    
    response = {
        "statusCode": 200,
        "body": json.dumps(found)
    }
    
    client.start_execution(
        **{
          'input' : json.dumps({
                      "component_name": "com.example.ggmlcomponent",
                      "version": sf_list[1],
                      "s3object": unquote(sf_list[0]),
                      "group_name": "gggroup",
                    }),
          'stateMachineArn' : sf_arn 
        #   'stateMachineArn' : 'arn:aws:states:ap-northeast-1:222136011322:stateMachine:dev-MLOps_deploy_edgedeploy_pipeline'
        }
    )

    return "Step Functionsへ \n -- s3object:{0} ,\n -- version:{1}\nを入力として実行しました。".format(unquote(sf_list[0]),sf_list[1])

