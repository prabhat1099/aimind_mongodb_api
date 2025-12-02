from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import pandas as pd 
load_dotenv()

MONGO_URI= os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
my_db = client['aimind07']
my_coll = my_db['customers']

app = FastAPI()

class Customers(BaseModel):
    id : int
    name : str
    age : int
    loc : str

@app.get("/")
def home_page():
    return "Customer Database"    

@app.post("/insert-one")
async def insert_one_data_mycoll(cust:Customers):
    data =cust.model_dump()   #   or cust.dict() in older pydantic
    result = await my_coll.insert_one(data)
    return f"message : record successfully inserted with : {str(result.inserted_id)}"

@app.post("/insert-many")
async def insert_many_data_mycoll(customers: list[Customers]):
    data_list = [ cust.model_dump() for cust in customers]
    #data_list = customers
    results = await my_coll.insert_many(data_list)
    return {"message":"records inserted succesfully","inserted ids ": [str(id_) for id_ in results.inserted_ids]}

@app.get("/all-data")
async def get_all_data_mycoll():
    documents = await my_coll.find().to_list(length=None)  # find() returns cursor so convert to list

    # Convert _id (ObjectId) to string
    for doc in documents:
        doc["_id"] = str(doc["_id"])
    return {"message": "All records fetched successfully",
            "data": documents}    


    



  
