from fastapi import FastAPI
from App.api.endpoints import register
from App.api.endpoints import login
from App.api.endpoints import token
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()


app.include_router(register.router)
app.include_router(login.router)
app.include_router(token.router)


@app.get("/")
async def root():
    return {"message": "Hello Dear !"}