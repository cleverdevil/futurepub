from datetime import datetime
from dateutil.parser import parse

import requests
import boto3
import json

s3 = boto3.client('s3')


def publish(key):
    response = s3.get_object(Bucket='futurepub-pending', Key=key)
    payload = json.loads(response['Body'].read().decode('utf-8'))

    authorization = payload.pop('authorization')
    destination = payload['properties'].pop('mp-destination')[0]

    h = {'Authorization': authorization}
    mp_r = requests.post(destination, json=payload, headers=h)

    if mp_r.status_code in (200, 201):
        s3.delete_object(Bucket='futurepub-pending', Key=key)


def periodic_publish(event, context):
    publish_queue = []
    now = datetime.utcnow()

    pendings = s3.list_objects(Bucket='futurepub-pending').get('Contents', [])
    for pending in pendings:
        pending_key = pending['Key']
        publish_dt_utc = pending_key.split('~~')[0]
        publish_dt_utc = parse(publish_dt_utc)

        if publish_dt_utc <= now:
            publish_queue.append(pending_key)

    for key in publish_queue:
        publish(key)
