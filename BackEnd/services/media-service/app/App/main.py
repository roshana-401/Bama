from fastapi import FastAPI
from App.api.endpoints import MediaCar
from App.api.endpoints import MediaSpareParts
from fastapi.middleware.cors import CORSMiddleware
from App.core.db.database import db

app=FastAPI()

# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(MediaCar.router)
app.include_router(MediaSpareParts.router)

@app.get("/")
async def root():
    # استفاده از `find()` برای دریافت AsyncIOMotorCursor
    cursor = db["CarMedia"].find()

    # تبدیل کرسر به لیست و دریافت اسناد
    documents = await cursor.to_list(None)  # یا می‌توانید عددی را به جای None وارد کنید تا تعداد اسناد محدود شود

    # تکرار روی لیست اسناد
    for document in documents:
        print(document)
    return {"message": "Data fetched successfully"}

@app.get("/spare")
async def root():
    # استفاده از `find()` برای دریافت AsyncIOMotorCursor
    cursor = db["SpareParts"].find()

    # تبدیل کرسر به لیست و دریافت اسناد
    documents = await cursor.to_list(None)  # یا می‌توانید عددی را به جای None وارد کنید تا تعداد اسناد محدود شود

    # تکرار روی لیست اسناد
    for document in documents:
        print(document)
    return {"message": "Data fetched successfully"}

@app.post("/")
async def root():
    db["CarMedi"].insert_one({"key": "value"})