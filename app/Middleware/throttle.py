from starlette.types import ASGIApp, Message, Scope, Receive, Send
from starlette.middleware.base import BaseHTTPMiddleware


class ThrottleMiddleware:
    def __init__(self, app : ASGIApp) -> None :
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] not in  ("http","https"):
            await self.app(scope, receive, send)
            return

        body_size = 0

        async def receive_logging_request_body_size():
            nonlocal body_size

            message = await receive()
            assert message["type"] == "http.request"

            body_size += len(message.get("body", b""))

            if not message.get("more_body", False):
                print(f"Size of request body was: {body_size} bytes")

            return message

        await self.app(scope, receive_logging_request_body_size, send)

class BThrottleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        
        response = await call_next(request)
        response.headers['Custom'] = 'Example'
        return response