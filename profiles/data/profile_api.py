from profiles.data.profile_manager import ProfileManager
from profiles.data.profile_models import *

class ProfileAPI:
    ''' these functions will take and return plain python data
    the ProfileManager works with model objects'''

    #-------------- THESE ARE IMPLEMENTED --------------

    def __init__(self, pm: ProfileManager):
        self.pm = pm

    def delete_all(self):
        return self.pm.delete_all()

    def create(self, data) -> str:
        p = Profile(**data)
        return self.pm.create(p)
    
    def read_all(self) -> list[dict]:
        r = self.pm.read_all()
        return [p.model_dump() for p in r.profiles]

    #============= TODO: IMPLEMENT THESE==============

    #----------- READS -----------

    def read(self,query:dict={}) -> list[dict]:
        '''read profile by query'''
        q = ProfileQuery(**(query or {}))
        r = self.pm.read(q)
        return [p.model_dump() for p in r.profiles]


    def read_by_id(self, id: str) -> dict:
        '''read profile by id'''
        p = self.pm.read_by_id(id)
        if p:
            return p.model_dump(exclude_none=True)
        else:
            return None
    
    def read_by_username(self,username: str) -> list[dict]:
        '''read all profiles by username'''
        r = self.pm.read_by_username(username)
        return [p.model_dump() for p in r.profiles]
    
    def read_by_profile_name(self,profile_name):
        '''read profile by profile_name'''
        p = self.pm.read_by_profile_name(profile_name)
        if p:
            return p.model_dump()
        else:
            return None
                
    #-------------- UPDATES --------------
    def add_skill(self, profile_id: str, skills: list[str]) -> int:
        '''add skills to profile'''
        
        s = ProfileSkills(skills=skills)
        return self.pm.add_skills(profile_id, s)