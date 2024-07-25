from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

class Account(BaseModel):
    subdomain: str
    name: str

class JobInfo(BaseModel):
    shortcode: str
    title: str
    
class Candidate(BaseModel):
    id: str
    name: str
    firstname: str
    lastname: str
    headline: Optional[str] = None
    account: Account
    job: JobInfo
    stage: str
    disqualified: bool
    disqualification_reason: Optional[str] = None
    hired_at: Optional[datetime] = None
    sourced: bool
    profile_url: HttpUrl
    address: Optional[str] = None
    phone: Optional[str] = None
    email: str
    domain: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class CandidatesList(BaseModel):
    candidates: List[Candidate]
