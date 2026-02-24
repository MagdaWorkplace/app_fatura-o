from pydantic import BaseModel, Field


# Model for JSON body of the post request.

class RequestRegister(BaseModel):
    username: str
    password: str = Field(max_length=72, description="The password need to be 72 charcters or less.")


class RequestLogin(BaseModel):
    username: str
    password: str
