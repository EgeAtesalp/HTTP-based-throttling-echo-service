from fastapi import FastAPI
from pydantic import BaseModel, Field, Json, PositiveInt
import redis
import time
from app.Middleware.throttle import ThrottleMiddleware




class RequestRate(BaseModel):
    request_rate : PositiveInt




app = FastAPI()


'''
Resolves the client side of the Redis database connection
'''
@app.on_event("startup")
def startup_db_client():
    
    app.r = redis.Redis(host='redis', port=6379, db=0) # <- host = 'localhost' or 'redis'

    #redis if run from the docker container, localhost otherwise
    
    app.r.set('request_rate', 5)
    app.r.set('counter', 0) 
    app.r.set('window', time.time())
    app.add_middleware(ThrottleMiddleware, redis = app.r)



'''
@app.on_event("shutdown")
def shutdown_db_client():
    app.r.client_kill() 
'''


'''
 POST /echo  - Returns as response the JSON body of the request
'''
@app.post("/echo") 
def echo(body: dict):
    return body

'''
GET /rate - Returns as response the request limit of the throttling functionality
'''
@app.get("/rate", response_model=RequestRate)
def get_Rate():

    request_limit : RequestRate =  {"request_rate" : app.r.get('request_rate')}
    return request_limit

'''
POST /rate -  Changes the request limit of the throttling functionality, returns the 
updated request limit
'''
@app.post("/rate", response_model=RequestRate) 
def post_Rate(rate : RequestRate):

    app.r.set('request_rate', rate.request_rate) 
    response : RequestRate =  {"request_rate" :  rate.request_rate}
    return response

