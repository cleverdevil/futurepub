# Futurepub: Scheduled micropub

## Using Futurepub

Futurepub provides an easy way to schedule a post to be published to any
Micropub endpoint at a future date and time. To use Futurepub, simply treat
Futurepub as a Micropub endpoint via `https://futurepub.cleverdevil.io`.
Futurepub only supports JSON style Micropub requests.

As part of your JSON payload, you must include two properties:
`mp-destinationgq`, which should be the endpoint that you want to publish to,
and `published`, which will be the date/time stamp that specifies when you want
to publish.

For authentication, simply pass the Bearer Token for your target Micropub
endpoint in an `Authorization` HTTP header.

## Sample

If you wanted to publish "Hello, World" content to a Micropub endpoint available
at `https://example.com/micropub` with a Bearer token of `XXXXXXXX` on January
20th, 2040, at 12:00 UTC, you would send the following HTTP request:

```
POST /micropub HTTP/1.1
Host: futurepub.cleverdevil.io
Content-Type: application/json
Authorization: Bearer XXXXXXXX

{
  "type": ["h-entry"],
  "properties": {
    "name": ["Test Post from Futurepub"],
    "content": [{
      "html": "Hello, World!" 
    }],
    "published": [
      "2040-01-20T12:00:00"
    ],
    "mp-destination": [
      "https://example.com/micropub"
    ]
  }
}
```
      
## How Does it Work?

Futurepub does lightweight validation on the data passed to it, and then stores
the JSON payload along with the Bearer token in a secure Amazon S3 bucket. A
scheduled operation then checks the S3 bucket periodically (currently, every
five minutes), and then sends publish operations as needed.
