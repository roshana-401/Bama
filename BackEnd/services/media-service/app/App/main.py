from fastapi import FastAPI
from App.api.endpoints import MediaCar
from App.api.endpoints import MediaSpareParts
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(MediaCar.router)
app.include_router(MediaSpareParts.router)
