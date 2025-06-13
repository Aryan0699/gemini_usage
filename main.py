from fastapi import FastAPI #framework to build api 
from pydantic import BaseModel #validation ke liye help karega structure define karna 
from typing import List
import os
from dotenv import load_dotenv
from google import generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

app=FastAPI()

# //for cors policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

google_api_key=os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=google_api_key)

model=genai.GenerativeModel("gemini-2.0-flash")

# response=model.generate_content("Hello!")

# print(response.text)


@app.get("/talk_ai")
def response_ai(req:str):
    print(req)
    res=model.generate_content(req)
    print(res.text)
    return {"response":res.text}
    


class Tea(BaseModel):
    id:int
    name:str
    origin:str
#hold collection of above document(based on above schema)
teas:List[Tea]=[]

#decorators pe based hai fastapi to give sperpower to fucntions

@app.get("/") 
def read_root():
    return {"message":"Welcome to chai code"}

@app.get("/teas")
def get_teas():
    return teas

@app.post("/teas")
def add_tea(tea:Tea):
    teas.append(tea)
    return tea

@app.put("/teas/{tea_id}")
def update_tea(tea_id:int,updated_tea:Tea):
    for index,tea in enumerate(teas):
        if tea.id==tea_id:
            teas[index]=update_tea
            return update_tea
    return {"error":"Tea not found"}

@app.delete("/teas/{tea_id}")
def delete_tea(tea_id:int):
    for index,tea in enumerate(teas):
        if tea.id==tea_id:
            deleted=teas.pop(index)
            return deleted
    return {"error":"Tea not found"}