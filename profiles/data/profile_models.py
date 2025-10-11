from datetime import datetime
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field

# PROFILES

class Profile(BaseModel):
    id: str = Field(alias='_id',default=None)
    username: str
    profile_name: str
    skills: Optional[List[str]] = []

class ProfileCollection(BaseModel):
    profiles:List[Profile]

class ProfileQuery(BaseModel):
    user_id: Optional[str]=None
    username: Optional[str]=None
    profile_name: Optional[str]=None

class ProfileSkills(BaseModel):
    skills: List[str]



    