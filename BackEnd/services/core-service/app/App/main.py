from fastapi import FastAPI
from App.api.endpoints import car_compony
from App.api.endpoints import model_car
from App.api.endpoints import province
from App.api.endpoints import city
from App.api.endpoints import sell_car
from App.api.endpoints import sell_spare_part
from App.api.endpoints import save_sell_car
from App.api.endpoints import save_sell_spare_part
from App.api.endpoints import user

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
app.include_router(sell_spare_part.router)
app.include_router(sell_car.router)
app.include_router(save_sell_car.router)
app.include_router(save_sell_spare_part.router)


@app.get("/")
async def root():
    return {"message": "Hello Dear !"}