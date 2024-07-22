from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime

class DepartmentHierarchy(BaseModel):
    id: int
    name: str

class Location(BaseModel):
    location_str: Optional[str] = None  
    country: Optional[str] = None  
    country_code: Optional[str] = None  
    region: Optional[str] = None  
    region_code: Optional[str] = None  
    city: Optional[str] = None  
    zip_code: Optional[str] = None
    telecommuting: bool
    workplace_type: str

class LocationDetail(BaseModel):
    country_code: Optional[str] = None 
    country_name: Optional[str] = None 
    state_code: Optional[str] = None 
    subregion: Optional[str] = None   
    zip_code: Optional[str] = None
    city: Optional[str] = None 
    coords: str
    hidden: bool

class Job(BaseModel):
    id: str
    title: str
    full_title: str
    shortcode: str
    code: Optional[str]
    state: str
    sample: bool
    department: Optional[str]
    department_hierarchy: List[DepartmentHierarchy]
    url: HttpUrl
    application_url: HttpUrl
    shortlink: HttpUrl
    location: Optional[Location]
    locations: Optional[List[LocationDetail]]
    created_at: datetime

class JobsList(BaseModel):
    jobs: List[Job]

class JobDetail(BaseModel):
    id: str
    title: str
    full_title: str
    shortcode: str
    code: Optional[str]
    state: str
    department: Optional[str]
    department_hierarchy: List[DepartmentHierarchy]
    url: HttpUrl
    application_url: HttpUrl
    shortlink: HttpUrl
    location: Optional[Location]
    locations: Optional[List[LocationDetail]]
    created_at: datetime
    full_description: str
    description: str
    requirements: str
    benefits: str
    employment_type: str
    industry: str
    function: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    keywords: Optional[str] = None

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
