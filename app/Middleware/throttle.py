from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import redis
import time
from fastapi.responses import JSONResponse



'''
Throttling functionality as a middleware, implements BaseHTTPMiddleware
'''

class ThrottleMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: ASGIApp,
            redis: redis.Redis,
    ):
        super().__init__(app)
        self.redis = redis

    async def dispatch(self, request: Request, call_next):

        current_time : float = time.time()
        window_start : float  =  float(self.redis.get('window'))
        counter : int = int(self.redis.get('counter'))
        request_rate : int = int(self.redis.get('request_rate'))
        diff = current_time - window_start
    

        if (diff > 60):

            self.redis.set('window', current_time )
            counter = 1
            self.redis.set('counter', counter )
            print(f"Limit =  {request_rate}   Counter =  {counter}")
            response = await call_next(request)
            return response
           
          
        elif (counter >= request_rate):
            counter += 1
            self.redis.set('counter', counter)
            print(f"Limit =  {request_rate}   Counter =  {counter}")
            return JSONResponse(status_code=429, content = {"body":"Limit exceeded. Wait a minute and try again."})
           
        else:
            counter += 1
            self.redis.set('counter', counter)
            print(f"Limit =  {request_rate}   Counter =  {counter}")
            response = await call_next(request)
            return response


