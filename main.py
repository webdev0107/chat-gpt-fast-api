import os
import openai
from fastapi import FastAPI
from pydantic import BaseModel

class ProductDetails(BaseModel):
    name: str | None = None
    description: str | None = None
    about: str | None = None

class RequestData(BaseModel):
    content_type: str
    action: str | None = "rephrase"
    product_details: ProductDetails
    KeywordList: list


app = FastAPI()
openai.organization = os.getenv("OPENAI_ORG_ID")
openai.api_key = os.getenv("OPENAI_KEY")


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/edit")
async def editText(text: RequestData):
    print(text)
    print(openai.organization)
    print(openai.api_key)
    model = "text-davinci-edit-001"
    input = ""
    if text.content_type == "description":
        input = text.product_details.description
    elif text.content_type == "about":
        input = text.product_details.about
    else:
        input = text.product_details.name

    instruction = "Please complete three grammatically correct sentences, including the words 'Toys', 'Drone', 'Quadcopter', and 'Batteries'."

    res = openai.Edit.create(
        model=model,
        input=input,
        instruction=instruction,
        n=3
    )
    print(res)
    return res
    # return []