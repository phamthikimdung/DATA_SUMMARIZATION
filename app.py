import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  
import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": ""})

@app.post("/Summarize", response_class=HTMLResponse)
async def summarize(request: Request):
    form_data = await request.form()
    data = form_data["data"]
    maxL = int(form_data["maxL"])
    minL = maxL // 4

    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": data,
        "parameters": {"min_length": minL, "max_length": maxL},
    })[0]

    return templates.TemplateResponse("index.html", {"request": request, "result": output["summary_text"]})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
