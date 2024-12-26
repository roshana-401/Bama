from fastapi import FastAPI
from App.api.endpoints import register
from App.api.endpoints import login
from App.api.endpoints import token
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

origins = ["*","http://127.0.0.1:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(register.router)
app.include_router(login.router)
app.include_router(token.router)


@app.get("/")
async def root():
    return {"message": "Hello Dear !"}