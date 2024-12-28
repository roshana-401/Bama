from fastapi import FastAPI
from App.api.endpoints import car_compony
from App.api.endpoints import model_car
from App.api.endpoints import province
from App.api.endpoints import city

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


app.include_router(car_compony.router)
app.include_router(model_car.router)
app.include_router(province.router)
app.include_router(city.router)


@app.get("/")
async def root():
    return {"message": "Hello Dear !"}