from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analysis import run_analysis
from pydantic import BaseModel

app = FastAPI()

# Allows frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompareRequest(BaseModel):
    section: str
    priceSegment: str

@app.post("/results")
def get_results(request: CompareRequest):
    return run_analysis(request.section, request.priceSegment)
