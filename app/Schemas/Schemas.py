from pydantic import BaseModel, Field, Json, PositiveInt

class RequestRate(BaseModel):
    request_rate : PositiveInt
