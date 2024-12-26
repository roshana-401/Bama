from pydantic import BaseModel,EmailStr,conint,Field

class TokenData(BaseModel):
    Token_Id:str
    
class TokenMassage(BaseModel):
    message:str
    
    