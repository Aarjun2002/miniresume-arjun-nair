from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List

app = FastAPI()

# In-memory storage
resumes = []

# Data model
class Resume(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    skills: List[str]

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.post("/resume")
def add_resume(resume: Resume):
    # Check duplicate email
    for existing in resumes:
        if existing.email == resume.email:
            raise HTTPException(
                status_code=400,
                detail="Resume with this email already exists"
            )

    resumes.append(resume)
    return {"message": "Resume added successfully"}


# Get all resumes
@app.get("/resumes")
def get_resumes():
    return resumes

@app.get("/")
def root():
    return {"message": "Mini Resume API is running"}
