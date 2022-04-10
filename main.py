# pip install fastapi, uvicorn[standard]
# Run using cmd:  uvicorn main:app --reload
# http://127.0.0.1:8000/docs for API docs (swagger.ui)

from urllib import response
from fastapi import FastAPI
from aggregate import aggregate
from firebase import getGlobalModeldowloadURL
from firebase_init import initializeFirebase

initializeFirebase()
app = FastAPI()

@app.get('/')
def welcome():
    return "Hello"


@app.get('/aggregate/{project_id}')
def projectAggregation(project_id: str): 
    response = aggregate(project_id)
    if response == "success":
        return {"response":"Okay 🥚"}
    else:
        return {"response": "Error somewhere 🤧"}

@app.get('/dowloadGlobalModelFromFirebase/{project_id}')
def dowloadGlobalModelFromFirebase(project_id: str):
    dowloadURL = getGlobalModeldowloadURL(project_id)

    if(len(dowloadURL)== 0):
        return {
            "response" : "Error"
        }
    else : 
        return {
            "response" : dowloadURL
        }
