from datetime import datetime
import unittest
from bs4 import BeautifulSoup as bs

'''
feel free to change this, or the location of this file, to make the imports work for you.
but remember - that all the imports in your source code must be relative to app.py
'''
from app import app

try:
    from gradescope_utils.autograder_utils.decorators import weight, number
except ModuleNotFoundError as e:
    from test_dummy import weight,number

client = app.test_client()


class TestApp(unittest.TestCase):
    '''tests:
    1. create and view by profile_name
    2. view all profiles
    3. view user profile
    4. add skill
    '''

    @classmethod
    def setUpClass(self):

        res = client.post('/login',data={
            'username':'admin',
            "password":"admin"
        })
        print('logged in')

    def setUp(self):

        print(self.id())

        res = client.post('/profiles/delete/all')
        # print(res.text)

        # res = client.post("/profiles/create",data={
        #     'username':'admin',
        #     'profile_name':'testing123'
        # })   

    def make_profile(self,un,pn):
        res = client.post("/profiles/create",data={
            'username':un,
            'profile_name':pn
        })      
        return res.text

    @number("1")
    @weight(4) 
    def test_create_and_view(self):
        '''POST create, GET redirect to view user
        assert that profile_name and username are shown in a table, 
        in that order'''

        ms = datetime.now().microsecond
        pn = f"profile{ms}"
        un = 'admin'
        text = self.make_profile(un,pn)      

        # get redirect
        soup = bs(text,'lxml')
        ref = soup.find('a').get('href')
        response = client.get(ref)
        text = response.data.decode()

        # print(text)
        soup = bs(text,'lxml')

        # get tds
        tds=soup.find_all('td')
        # print(tds)
        self.assertEqual(tds[0].text,pn)
        self.assertEqual(tds[1].text,un)

    @number("2")
    @weight(4) 
    def test_invalid_username(self):
        '''
        try to create profile with invalid username
        assert redirect back to create form with message "user {username} not found"
        '''

        ms = datetime.now().microsecond
        pn = f"profile{ms}"
        un = 'invalid_user'
        text = self.make_profile(un,pn)  

        # print(text)
        # get redirect
        soup = bs(text,'lxml')
        ref = soup.find('a').get('href')
        res = client.get(ref)
        # text = response.data.decode()  

        # print(res.text) 
        msg = bs(res.text,'lxml').find('li').text
        self.assertEqual(msg.lower(),f"user {un} not found")

    @number("3")
    @weight(4) 
    def test_view_profiles(self):
        '''POST profile, GET profiles
        two columns: profile_name and username
        profile_name column should be links to profiles'''
    
        ms = datetime.now().microsecond
        pn1 = f"profile{ms}"
        un1 = f'admin'
        text = self.make_profile(un1,pn1)  

        # ms = datetime.now().microsecond
        # pn2 = f"profile{ms}"
        # un2 = f'user{ms}'
        # text = self.make_profile(un2,pn2)  

        res = client.get('/profiles/')

        soup = bs(res.text,'lxml')
        tr = soup.find_all('tr')[-1]
        # print(tr)

        tds = tr.find_all('td')
        self.assertEqual(tds[0].find('a').get('href'),f"/profiles/{pn1}")
        self.assertEqual(tds[1].text,un1)

    @number("4")
    @weight(4) 
    def test_view_user_profile(self):
        '''
        POST two profiles
        GET profiles
        assert that last two links go to the profiles just created
        '''

        un1 = f'admin'
        ms = datetime.now().microsecond
        pn1 = f"profile{ms}"
        text = self.make_profile(un1,pn1)  

        ms = datetime.now().microsecond
        pn2 = f"profile{ms}"
        text = self.make_profile(un1,pn2)  

        res = client.get(f'/users/{un1}/profiles')
        # print(res.text)

        soup = bs(res.text,'lxml')
        refs = soup.find_all('a')
        refs = [a.get('href') for a in refs]

        # last two links should be profiles for this user
        self.assertEqual(refs[-2:],[f'/profiles/{pn1}', f'/profiles/{pn2}'])  

    @number("5")
    @weight(4) 
    def test_add_skill(self):
        '''
        GET profile view to get profile_id
        POST to add a new skill
        GET redirect to profile view
        assert that new skill is in ul with name=skills
        '''
        
        un1 = f'admin'
        ms = datetime.now().microsecond
        pn1 = f"profile{ms}"
        text = self.make_profile(un1,pn1)  

        res = client.get(f'/profiles/{pn1}')
        # print(res.text)
        soup = bs(res.text,'lxml')
        pid = soup.find('input',{'name':"profile_id"})['value']
        # print(pid)

        res = client.post(f'/profiles/{pn1}/add-skill',data={
            'profile_id': pid,
            'skill':'backpacking'
        })
        # print(res.text)
        soup = bs(res.text,'lxml')

        # get redirect
        ref = soup.find('a').get('href')
        res = client.get(ref)
        # text = response.data.decode()
        # print(res.text)
        soup = bs(res.text,'lxml')   

        lis = soup.find('ul',{'name':'skills'}).find_all('li')
        
        skills = [li.text for li in lis]
        self.assertIn('backpacking',skills)

if __name__ == '__main__':
    unittest.main()