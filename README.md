# HTTP-based-throttling-echo-service

HTTP-based throttling echo service

written by Ege Atesalp


## Documentation

POST /echo  - Returns as response the JSON body of the request

GET /rate - Returns as response the request limit of the throttling functionality

POST /rate -  Changes the request limit of the throttling functionality, returns the updated request limit

## Installation

### Local

In root directory

Install the required modules in requirements.txt using the preffered dependency manager

```bash
    # Pull and run the redis container, skip if already running 
    docker-compose up redis

    
    # Run the app from port 8000, listens Redis from 6379 
    # If running locally, change the host parameter in redis.Redis() to 'localhost'
    python main.py

```

### Docker

```bash
    docker-compose up
```

## Testing

In root directory(docker or local)

```bash
    pytest
```
It is normal for the testing to take approximately 65 seconds, since it tests the 60 sliding window of the throttling functionality

## Future Improvements 

<ul>
  <li>Improve asynchronous handling </li>
  -Comment: Especially important for scalability, better leverages ASGI
  <li>Create individual testing</li>
  -Comment: Testing with multiple tests affected the results, specifically because the database values were incosistent inbetween.
  <li>Add functionality to make the middleware (throttling) only handle specific requests (/echo) </li>
</ul>


