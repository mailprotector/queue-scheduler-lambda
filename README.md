# queue-scheduler-lambda
A lambda that hits an API to queue a job.

### Environment Variables
| variable name    | description                                       |  type  | default | required |
| ---------------- | ------------------------------------------------- | :----: | :-----: | :------: |
| SECRET_CACHE_AGE | cache age in seconds of the secrets manager query | string |   300   |    no    |
| SECRET_NAME      | name of the secret containing the API token       | string |   no    |   yes    |
| TOKEN            | fall-back to token passed in via env var          | string |   no    |    no    |
| URL              | url to API endpoint to send request to            | string |   no    |   yes    |