from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from apriori_script import recommend_products_script
import os

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

class Input(BaseModel):
    input: str

@app.post("/recommend")
async def fetch_recommend_products(input: str):
    try:
        recommendations = recommend_products_script(input)
        return {"recommendations": recommendations}
    except Exception as e:
        print(e)
        return {"recommendations": []}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", default=8001)))