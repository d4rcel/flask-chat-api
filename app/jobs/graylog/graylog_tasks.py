from celery_holder import celery
import requests
import json

@celery.task(name='send_message_to_sqs_job') 
def send_message_to_sqs_job(kwargs): 
     
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    r = requests.post('https://graylogapi.scoopchat.app/api/send/message/sqs', json=kwargs, headers=headers)
    # r = requests.post('http://127.0.0.1:5001/api/send/message/sqs', json=kwargs, headers=headers)
    # print(r.status_code)
    
    # data = kwargs
    # data['host'] = kwargs.get('environ').get('HTTP_HOST')
    # data['short_message'] = kwargs.get('api')
    
    # headers = {
    #     'Content-Type': 'application/x-www-form-urlencoded',
    # }
    
    # response = requests.post('http://logs.scoopchat.app:12202/gelf', headers=headers, data=json.dumps(data))
    # print(response.status_code)