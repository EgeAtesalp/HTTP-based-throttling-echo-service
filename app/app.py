
from fastapi import FastAPI


from pydantic import Json
from pydantic import BaseModel, Field, Json, PositiveInt
import redis
import time
from app.Middleware.throttle import ThrottleMiddleware




class RequestRate(BaseModel):
    request_rate : PositiveInt




app = FastAPI()



@app.on_event("startup")
def startup_db_client():
    
    app.r = redis.Redis(host='redis', port=6379, db=0) # change from localhost-redis
    
    app.r.set('request_rate', 5)
    app.r.set('counter', 0) 
    app.r.set('window', time.time())
    app.add_middleware(ThrottleMiddleware, redis = app.r)



'''
@app.on_event("shutdown")
def shutdown_db_client():
    app.r.client_kill() 
'''

@app.post("/echo") 
def echo(body: dict):
    return body


@app.get("/rate", response_model=RequestRate)
def get_Rate():

    request_limit : RequestRate =  {"request_rate" : app.r.get('request_rate')}
    return request_limit


@app.post("/rate", response_model=RequestRate) 
def post_Rate(rate : RequestRate):

    app.r.set('request_rate', rate.request_rate) 
    response : RequestRate =  {"request_rate" :  rate.request_rate}
    return response

