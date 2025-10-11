import unittest

try:
    from app import app
    # from accounts.user_login import UserLogin
except:
    from solution.app import app

try:
    from gradescope_utils.autograder_utils.decorators import weight, number
except Exception as e:
    print(e)
    from test_dummy import weight,number

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

        self.admin = app.test_client()
        self.user = app.test_client()
        self.nli = app.test_client()

        self.admin.post('/login',data={
            'username':'admin',
            "password":"admin"
        })

        self.admin.post('/users/create',data={
            'username':'test',
            'password':'test'
        })  

    def setUp(self):

        print(self.id())

    # @unittest.skip
    @weight(1)
    @number("1")    
    def test_not_logged_in(self):
        '''Test that not-logged-in users have limited access (GET)'''

        # not logged in
        client = self.nli

        # try these
        allowed = ['/','/login']
        restricted = ['/users/','/users/asdf','/logout']

        for route in allowed:
            res = client.get(route)
            self.assertEqual(res.status_code,200,f"GET {route} did not return code 200 (OK)")

        for route in restricted:
            res = client.get(route)
            self.assertEqual(res.status_code,401,f"GET {route} did not return code 401 (restricted)")

    # @unittest.skip
    @weight(1)
    @number("2")    
    def test_regular_user(self):
        '''test that logged in regular user can access additional routes, but not admin-only routes'''

        self.user.post('/login',data={
            'username':'test',
            'password':'test'
        })

        res = self.user.get('/users/test')
        self.assertEqual(res.status_code,200,"GET /users/test did not return 200")      

        res = self.user.get('/users/test2')  
        self.assertEqual(res.status_code,404,"GET /users/test2 did not return 404 (not found)")

        res = self.user.get('/users/notfound')
        self.assertEqual(res.status_code,404,"GET /users/test did not return 404 (not found)")

        res = self.user.get('/users/')
        self.assertEqual(res.status_code,403,"GET /users/test did not return 403 (forbidden)")        
        
    @weight(1)
    @number("3")        
    def test_admin(self):
        '''test that admin users can access all routes'''

        res = self.admin.get('/users/')
        self.assertEqual(res.status_code,200, "GET /users/ did not return 200")

if __name__=="__main__":
    unittest.main()




