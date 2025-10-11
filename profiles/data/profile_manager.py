from .db_manager import DBManager
from profiles.data.profile_models import *    

class ProfileManager:
    '''
    The profile manager takes and returns model objects
    The DBManager works with plain python objects'''

    #================ THESE ARE IMPLEMENTED ================

    def __init__(self, dbm: DBManager):
        '''connect to db server and set self.col'''
    
        self.dbm = dbm
        self.dbm.col.create_index("profile_name" , unique=True)

    def delete_all(self):
        '''delete all profiles'''

        return self.dbm.delete_all()

    def create(self, p: Profile):
        '''create profile'''

        return self.dbm.create(p.model_dump())
    
    def read_all(self) -> ProfileCollection:
        '''read all profiles'''

        r = self.dbm.read_all()
        return ProfileCollection(profiles=r)
    
    #=================IMPLEMENT THESE================

    #-------------------- READS ----------------------

    def read(self,query: ProfileQuery)->ProfileCollection:
        '''read profile by query'''

        # need to exclude None so that you can query by any of the optional fields
        q = query.model_dump(exclude_none=True)

        ''' now do the query'''
        r = self.dbm.read(q)
        return ProfileCollection(profiles=r)

    def read_by_id(self,id: str) -> Profile:
        '''read profile by id'''

        r = self.dbm.read_by_id(id)
        if r:
            return Profile(**r)
        else:
            return None
    
    def read_by_profile_name(self,name:str) -> Profile:
        '''read profile by profile_name'''

        r = self.dbm.read({'profile_name':name})
        if r:
            return Profile(**r[0])
        else:
            return None
    
    def read_by_username(self,uname:str) -> ProfileCollection:
        '''read all profiles by username'''

        r = self.dbm.read({'username':uname})
        return ProfileCollection(profiles=r)
    

    #---------------- UPDATES ----------------------
        
    def add_skills(self, pid, skills: ProfileSkills):
        '''add skills to profile'''

        p = self.read_by_id(pid)
        if not p:
            return 0
        
        current_skills = set(p.skills or [])
        new_skills = set(skills.skills or [])
        updated_skills = list(current_skills.union(new_skills))
        
        if len(updated_skills) == len(current_skills):
            return 0

        return self.dbm.update(pid, {'skills': updated_skills})



