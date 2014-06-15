API Docs
========


### Send an email

This method will enqueue an email to be sent. A task id will be returned which can later be used to check on the status of the email.

```
POST /api/1/email
```

#### Parameters

| Name       | Type   | Description                             |
|------------|--------|-----------------------------------------|
| from_email | string | The address the email will be sent from |
| to_email   | string | The address the email will be sent to   |
| subject    | string | The email's subject                     |
| body       | string | The email's body                        |

#### Response

```
{
  "err": 0,
  "task_id": "095995d6-4268-4685-b16f-d83b96aa85c4",
  "message": "The email has been queued!"
}
```

#### Sample request

```
curl -X POST http://sbezboro.com/uber/api/1/email \
  -d "from_email=email1@example.com" \
  -d "to_email=email2@example.com" \
  -d "subject=This is a subject" \
  -d "body=Look at this amazing email"
```

### Check email task status

```
GET /api/1/email_status/:task_id
```

#### Parameters

| Name    | Type   | Description          |
|---------|--------|----------------------|
| task_id | string | The task id to check |

#### Response

```
{
  "err": 0,
  "status": "pending",
  "task_id": "e95e3e2a-8fa2-48d5-a0dc-900181aeac0b"
}
```

#### Sample request

```
curl http://sbezboro.com/uber/api/1/email_status/e95e3e2a-8fa2-48d5-a0dc-900181aeac0b
```
