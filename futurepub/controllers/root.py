from datetime import datetime
from urllib.parse import urlparse
from pecan import expose, redirect, abort, request
from dateutil.parser import parse

import json
import boto3
import uuid


s3 = boto3.client('s3')


class RootController(object):

    @expose(template='index.html')
    def index(self):
        return dict()

    @expose('json')
    def micropub(self, *args, **kwargs):
        # reject non-POST requests
        if request.method != 'POST':
            abort(405, 'This endpoint only accepts HTTP POST requests.')

        # get the microformats2 JSON data
        payload = request.json

        # get the authorization information
        authorization = request.headers.get('Authorization')
        payload['authorization'] = authorization

        # get the destination
        destination = payload.get('properties', {}).get('mp-destination', [None])[0]
        parsed = urlparse(destination)
        if parsed.scheme not in ('http', 'https') or \
           not parsed.netloc:
            abort(400, 'Invalid mp-destination.')

        # figure out when the request wants to be published
        publish_dt = payload.get('properties', {}).get('published', [''])[0]
        try:
            dt = parse(publish_dt)
        except:
            abort(400, 'Invalid publish date.')

        # store the object in S3 for future publishing
        s3.put_object(
            Bucket='futurepub-pending',
            Key='%s~~%s' % (publish_dt, str(uuid.uuid4())[:8]),
            Body=json.dumps(payload)
        )

        return dict(
            result='queued'
        )
